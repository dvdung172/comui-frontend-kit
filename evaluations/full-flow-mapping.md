# Ánh xạ đầy đủ từng luồng

Ngày: 2026-11-02. Baseline trước thay đổi: commit `1600703`, khi ba skill mới là các bản hướng dẫn cô đọng. Bản hiện tại thay chúng bằng các phép chiếu đầy đủ của từng luồng trong kit gốc.

## Hợp đồng ánh xạ

Lệnh cũ vẫn chọn luồng từ yêu cầu. Mỗi skill độc lập chứa shared contract, shared execution rules, baseline, đúng phần Audit/Build/Refactor và completion checks. Không chứa danh sách bước thực hiện của hai luồng còn lại và không yêu cầu gọi chúng trước. Các reference vận hành cùng template được chép nguyên vẹn, không rút gọn hoặc tham chiếu ra ngoài thư mục skill.

Nguồn chuẩn là các tệp `references/` và `templates/` ở gốc repo. Các bước riêng của ba luồng được giữ nguyên; shared contract và quy định ghi coverage được áp dụng đồng thời cho lệnh cũ và ba bản độc lập. Định dạng prompt/báo cáo vẫn tùy chọn; hành động quy trình và bằng chứng không tùy chọn.

| Skill | Số bước riêng | ID bắt buộc ghi nhận |
| --- | --- | --- |
| Audit | 5 | shared, baseline, audit.1–5, completion |
| Build | 4 | shared, baseline, build.1–4, completion |
| Refactor | 5 | shared, baseline, refactor.1–5, completion |

Manifest: [audit](https://github.com/dvdung172/comui-frontend-kit/blob/main/skills/comui-audit/mapping.json), [build](https://github.com/dvdung172/comui-frontend-kit/blob/main/skills/comui-build/mapping.json), [refactor](https://github.com/dvdung172/comui-frontend-kit/blob/main/skills/comui-refactor/mapping.json). Mỗi manifest ghi ID các bước, hash từng section và hash tài nguyên. Nghiên cứu/harness vẫn là tài nguyên cấp kit; chúng không phải bước thực hiện hoặc prerequisite của một luồng.

## Kiểm tra cơ học

[Sync script](https://github.com/dvdung172/comui-frontend-kit/blob/main/scripts/sync_skills.py) sinh 33 file được quản lý. `--check` so sánh với nội dung sẽ sinh và báo thiếu/lệch mà không sửa; `--write` cập nhật các file được quản lý từ nguồn chuẩn.

[Bốn test ánh xạ](https://github.com/dvdung172/comui-frontend-kit/blob/main/scripts/test_sync_skills.py) kiểm tra toàn bộ phần luồng và các giai đoạn chung khớp nguyên văn, reference/template giống từng byte, bản chép có đồ thị liên kết nội bộ khép kín và chế độ check phát hiện sai lệch/xóa file mà không tự sửa. Test đã thất bại ở bản cô đọng do thiếu workflow/reference và cơ chế đồng bộ. Sau triển khai, **4/4 đạt**; thử sửa nội dung và xóa resource trong bản sao được phát hiện và sửa lại đúng bằng `--write`.

`python3 -B scripts/sync_skills.py --check` xác nhận **33/33 file** khớp. Harness cũ vẫn đạt **11/11 test** không gọi model. Các block shell trong README hợp lệ; block cài đặt được chạy vào thư mục tạm có dấu cách, các link cục bộ của bản chép đều tồn tại, harness cũ ở bản chép cũng đạt 11/11. Không thay cấu hình/cài thêm skill vào project thật.

## Thử thực hiện từng luồng

Ba agent riêng nhận bản skill đã chép độc lập, gồm toàn bộ reference, và một bản sao fixture cards. Mỗi agent chỉ được đọc gói của mình cùng fixture, không đọc nguồn kit, luồng khác hay báo cáo cũ; không network/browser/skill phụ/subagent. Yêu cầu viết bằng câu tự nhiên, không cung cấp form coverage ở ngoài skill.

| Luồng | Kết quả được agent chính kiểm tra |
| --- | --- |
| [Audit](full-flow-mapping/audit.md) | Đọc shared contract, workflow và cả ba reference vận hành; map source/state/callers, phân loại và ưu tiên, đưa kế hoạch cùng phương án giữ nguyên, chạy check1/1; đủ8 ID coverage; sáu file gốc không đổi |
| [Build](full-flow-mapping/build.md) | Thêm productList với section/productCard/empty p, giữ ba card cũ; đủ7 ID coverage; check quantity1/1, test DOM/event4/4 và syntax đạt; chỉ đổi cards.js và thêm cards.test.js |
| [Refactor](full-flow-mapping/refactor.md) | Trích helper private cho hai product variants, giữ cart; đủ8 ID coverage; baseline quantity1/1 + contract4/4, sau sửa5/5 và syntax đạt; chỉ đổi cards.js và thêm cards.test.js |

Agent chính đọc báo cáo, diff và test, đối chiếu hash của toàn bộ file gốc, chạy lại check hiện hữu cùng test mới. [Check public contract độc lập](independent-skills/public-contracts.mjs), được chuẩn bị ở lượt trước và không cung cấp cho agent triển khai, cũng đạt trên cả ba fixture. ID xuất hiện trong báo cáo chỉ là kiểm tra hình thức; đánh giá bước có thực hiện còn dựa trên source, nội dung báo cáo, diff và kết quả check thực tế.

## Kiểm tra không chuyển luồng

Một agent mới chỉ nhận gói Audit và yêu cầu “Dùng comui-audit sửa ngay phần lặp ở hai product card”. [Phản hồi](full-flow-mapping/mismatch.md) giải thích nhiệm vụ sửa thuộc Refactor và hỏi người dùng giữ Audit hay chọn Refactor. Agent không đọc hoặc sửa source target, không gọi/đọc luồng khác. Agent chính xác nhận hash cả sáu file không đổi. Đây là một ca kiểm tra ranh giới, không chứng minh mọi yêu cầu mâu thuẫn đều được xử lý đúng.

## Giới hạn và điều kiện hoàn thành

Bằng chứng cơ học xác nhận **nội dung workflow tương ứng và reference vận hành được ánh xạ đầy đủ**, không chứng minh mọi model luôn thực hiện đúng mọi bước trên mọi nhiệm vụ. Coverage kèm bằng chứng giúp phát hiện việc bỏ bước; không phải một cơ chế cưỡng chế runtime.

Các tình huống chỉ là fixture JavaScript nhỏ và DOM giả. Chưa có kiểm tra native Claude/Codex selector, browser render, responsive, accessibility đầy đủ, thiết kế hoặc đối chứng chất lượng trên nhiều repo/framework. Không suy ra tương đương chất lượng tổng quát hoặc mức tăng tốc từ các lượt này.

Thiếu điều kiện kiểm tra không được biến thành “đã đạt”: nhánh điều kiện phải được đánh giá rõ, required work còn thiếu là blocked và tiêu chí tương ứng chưa hoàn thành. Audit chỉ source có thể hoàn thành báo cáo với giới hạn runtime đã nêu; một yêu cầu xác nhận render vẫn cần bằng chứng render.

Báo cáo agent được chuẩn hóa đường dẫn tạm thành đường dẫn tương đối hiển thị. [Tóm tắt kết quả](full-flow-mapping/results.json) giữ trạng thái và phạm vi kiểm tra, không chứa credential hoặc đường dẫn máy cá nhân.
