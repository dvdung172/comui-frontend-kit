# ComUICoder → bộ khung làm việc cho AI frontend

Ngày đối chiếu: 2026-11-01. Đọc bài arXiv v1 và mã công khai trên nhánh `main`; chưa cài hoặc chạy pipeline upstream. Liên kết `main` có thể thay đổi. Đây là phân tích để thiết kế quy trình, không phải tái lập thực nghiệm.

## Bằng chứng từ bài báo

ComUICoder nghiên cứu chuyển thiết kế thành UI nhiều trang. Phương pháp gồm phân khối ngữ nghĩa kết hợp UIED, nhóm khối theo hình ảnh/cấu trúc, sinh component rồi phản hồi theo phần tử. ComUIBench có 40 website và 150 trang. [Bài báo, §3–4](https://arxiv.org/html/2602.19276v1#S3)

Bảng 3 ghi reuse 59,96%, repetitive 2,10%. Tuy nhiên, DCGen có SSIM 0,7128 so với 0,7021; LayoutCoder có TreeBLEU 0,3974 so với 0,3958. Vì vậy, tuyên bố đứng đầu mọi chỉ số trong phần diễn giải không khớp bảng. Đây là kết quả tác giả báo cáo trên benchmark, không chứng minh hiệu quả audit/refactor dự án. [Bảng 3](https://arxiv.org/html/2602.19276v1#S6)

## Mã tham khảo thực sự làm gì

| Nguồn | Quan sát tĩnh | Ý nghĩa khi chuyển sang dự án |
| --- | --- | --- |
| [ComponentDetector.py](https://github.com/WebPAI/ComUICoder/blob/main/ComUICoder/ComponentDetector.py) | `process_page()` chia ảnh dài, gọi nhận diện và điều chỉnh bounding box | Cần tách quan sát UI thành đơn vị có ý nghĩa trước khi quyết định component |
| [MergeTools.py](https://github.com/WebPAI/ComUICoder/blob/main/ComUICoder/MergeTools.py) | `compute_group_merge()` sử dụng tín hiệu thị giác, kích thước, graph và gom nhóm | Nhóm tương đồng hỗ trợ tìm ứng viên; phải bổ sung xét hành vi từ source |
| [Prompts.py](https://github.com/WebPAI/ComUICoder/blob/main/ComUICoder/Prompts.py) | Có prompt sinh component Vue dùng chung, dữ liệu theo instance, khung trang có placeholder và sửa mã | Học cách tách layout/component/instance; thay các ràng buộc Vue và placeholder theo repo |
| [FeedBacker.py](https://github.com/WebPAI/ComUICoder/blob/main/ComUICoder/FeedBacker.py), [report_generation.py](https://github.com/WebPAI/ComUICoder/blob/main/ComUICoder/report_generation.py) | Ghép phần tử, phát hiện thiếu/thừa/sai lệch và tạo chỉ dẫn có loại lỗi, định danh, mức độ | Báo cáo cần chỉ đúng đối tượng, bằng chứng và thao tác đề xuất |
| [main.py](https://github.com/WebPAI/ComUICoder/blob/main/ComUICoder/main.py) | Entry point nhận ảnh; có điều kiện chọn website đầu tiên, trang sửa thứ ba và hai component | Các lựa chọn thử nghiệm này cần được thay bằng phạm vi nhiệm vụ thực tế |

Các quan sát trên là đọc source, không phải xác nhận pipeline chạy thành công hoặc đánh giá toàn bộ chất lượng upstream.

## Thiết kế mở rộng của bộ khung này

Các quyết định sau là đề xuất riêng để phục vụ yêu cầu audit/refactor; chưa có thí nghiệm chứng minh chúng cải thiện kết quả trên nhiều repo.

| Ý tưởng áp dụng | Quyết định cụ thể | Artifact để kiểm tra |
| --- | --- | --- |
| Hiểu UI trước khi sinh/sửa mã | Lập bản đồ route → trách nhiệm UI → implementation → state/data owner; đọc caller liên quan | Hồ sơ scope và bản đồ component |
| Tìm phần có thể dùng chung | Kiểm tra mục đích, events, state lifecycle, biến thể và chi phí API | Quyết định reuse/primitive/giữ riêng có lý do |
| Component hóa có hợp đồng | Tách dữ liệu instance khỏi cấu trúc ổn định; bảo toàn public API và state owner | Hợp đồng component và kế hoạch migration |
| Phản hồi cụ thể | Gắn phát hiện với file/symbol hoặc element, quy tắc áp dụng, tác động và phép kiểm chứng | Báo cáo audit, kế hoạch refactor và evidence |

Phân khối ảnh và thiết kế kiến trúc mã là hai quyết định có liên quan nhưng khác nhau. Một khối UI được quan sát như một đơn vị vẫn có thể được triển khai bằng nhiều component lồng nhau. Quy tắc phân khối của upstream không trở thành lệnh cấm composition.

Độ giống hình thức không đủ để quyết định gom. Ví dụ, product card và cart card có thể dùng cùng style nhưng phát event và quản lý trạng thái khác nhau. Có thể chia sẻ primitive trình bày trong khi giữ riêng hành vi. Ngược lại, hai product card chỉ khác dữ liệu và mật độ hiển thị có thể hợp nhất qua một API nhỏ nếu phù hợp quy ước dự án.

Luồng source-only không tạo bounding box giả và không suy ra pixel fidelity. Khi có app chạy và reference phù hợp, bổ sung vòng quan sát → xác định sai lệch → sửa đúng source → kiểm tra lại consumer. Khi thiếu chúng, vẫn đánh giá cấu trúc và lập kế hoạch với giới hạn bằng chứng được ghi rõ.

Ưu tiên công việc theo tác động người dùng, phạm vi consumer và rủi ro hồi quy. Không nhập nguyên ngưỡng vision, số lượng top-K hay mục tiêu reuse của nghiên cứu làm tiêu chuẩn chất lượng mặc định. Một component dùng chung có API rối có thể tốn công bảo trì hơn vài implementation độc lập.

## Điều cần kiểm chứng khi dùng thật

Đánh giá trên nhiệm vụ đại diện của repo: độ đúng của phát hiện, đề xuất có được chấp nhận không, giữ hành vi sau refactor, số lần sửa lại và chi phí sử dụng thực tế. Khi cần so sánh, cố định yêu cầu, revision, model và môi trường giữa quy trình cũ và bộ khung; ghi mọi can thiệp.

Kiểm tra cấu trúc Markdown và một fixture chỉ cho thấy khả năng đọc/nạp và một số hành vi. Chúng không chứng minh tương thích mọi công cụ AI, tăng tốc hay tiết kiệm token. Xem [kết quả kiểm tra gói](../evaluations/validation.md) để biết chính xác phần đã thử.
