# Kiểm tra ComUI Frontend Kit v1

Ngày: 2026-11-01. Đây là kiểm tra cấu trúc tài liệu và thử hành vi có giới hạn trong phiên tạo gói; không phải benchmark hay chứng nhận tương thích nhiều nhà cung cấp AI.

Các số lượng tệp và lượt kiểm tra dưới đây ghi lại **bản Markdown v1 trước tích hợp**. Bản mở rộng skill/harness có thêm metadata, script và fixture; xem [kiểm tra tích hợp Codex](codex-integration.md) cho trạng thái hiện hành.

## Kịch bản và phương pháp

Fixture source-only dùng JavaScript ESM và DOM thuần, gồm sáu file: `AGENTS.md`, `README.md`, `package.json`, `cards.js`, `cart.js`, `cart.test.js`. Có hai product card gần như trùng nhau, một cart card với callback/state khác, quy định giữ public API/events và README cũ khuyên gom mọi card. Script `npm run check` chạy một test logic chặn số lượng âm. Không có CSS, app chạy, backend hoặc ảnh/Figma.

Một agent độc lập audit trước khi có kit; một agent mới đọc kit và audit cùng fixture. Cả hai chỉ được đọc fixture và chạy check có sẵn, không sửa source, dùng network hoặc cài dependency. Tình huống là giả lập, không phải nhiệm vụ sản xuất; hai lượt dùng cùng model phiên, không phải kiểm thử qua hai công cụ AI khác nhau.

## Kết quả audit đã quan sát

| Tiêu chí | Không có kit | Có kit |
| --- | --- | --- |
| Đề xuất chia sẻ hai product implementation, giữ wrappers | Có | Có |
| Giữ cart behavior riêng | Có | Có |
| Nhận diện hướng dẫn UniversalCard cũ và bảo toàn events | Có | Có |
| Phân biệt source và kiểm chứng runtime | Có | Có |
| Ghi snapshot source | Không ghi | Có ghi snapshot theo thời điểm đọc, không có Git |
| Nêu loại quy tắc và phân biệt cơ hội refactor với bug | Có phân biệt bug tiềm ẩn, chưa có phân loại quy tắc tường minh | Có nêu quy định tường minh và khuyến nghị kit |
| Bàn giao trình tự baseline → extract → kiểm tra | Các đề nghị trong văn xuôi, chưa có trình tự riêng | Có trình tự cụ thể |
| Check thật | `npm run check`: 1 test đạt | `npm run check`: 1 test đạt |

Baseline đã làm đúng các quyết định tái sử dụng và giới hạn quan trọng. Khoảng trống quan sát được trước khi viết skill là snapshot và cấu trúc bàn giao, không phải một lỗi ép gom component. Kết quả này không chứng minh kit làm agent suy luận tốt hơn, cũng không phải so sánh có ý nghĩa thống kê. Lượt có kit có cấu trúc tốt hơn trên tình huống này nhưng không xuất đầy đủ mọi mục template; kit cho phép rút gọn theo quy mô.

Fingerprint SHA-256 của sáu file fixture được đối chiếu sau các lượt audit: không thay đổi. Các fixture thử nghiệm đi kèm trong `evaluations/fixtures/`; raw output tạm thời không thuộc gói phát hành.

## Kiểm tra thực hiện theo mode

| Kịch bản | Trạng thái |
| --- | --- |
| Audit source-only, có quy ước mâu thuẫn và component khác hành vi | Hoàn tất như trên |
| Refactor được giao rõ trên bản sao cô lập | Đã extract helper product nội bộ, giữ public wrappers và cart riêng; không hỏi lại quyền thực hiện |
| Build frontend từ văn bản, không có reference | Đã tạo task list DOM thuần với thêm task, complete/uncomplete, ba bộ lọc và empty state; không hỏi lại quyền thực hiện |

Hai kịch bản thực hiện được một agent khác chạy trong thư mục tạm ngoài kit, không sửa kit hay fixture audit gốc. Agent đọc `SKILL.md`, workflow, repo-profile, component-analysis và verification. Không dùng network hoặc cài dependency.

| Kiểm tra thực sự chạy | Kết quả |
| --- | --- |
| Refactor: `npm run check` trước/sau | 1/1 đạt ở cả hai thời điểm |
| Refactor: `node --test cards.test.js` trước/sau | 4/4 đạt; checks bảo vệ public exports, DOM/classes/text và callback với dữ liệu thay đổi |
| Build: `node --test app.test.cjs` | 5/5 đạt; blank input, literal text, add, complete/uncomplete, filters và focus/state giả lập |
| Build: `node --check app.js` | Đạt syntax check |

Agent chính đọc các check và chạy lại cả ba lệnh test sau triển khai cùng syntax check: tổng cộng 10/10 test đạt. Đây là checks trên fixture và DOM giả lập; không phải test tự động về hiệu quả chung của bộ tài liệu. Việc dùng native form/radio/checkbox hỗ trợ thiết kế cho keyboard nhưng chưa chứng minh tương tác bàn phím thực tế.

## Kiểm tra cấu trúc

- Entrypoint có 31 dòng, với hai field frontmatter `name` và `description` dạng scalar đơn giản.
- Kiểm tra frontmatter bằng Python standard library: đạt cấu trúc hai field, tên trùng thư mục, tên hợp lệ và độ dài description.
- Validator đi kèm `skill-creator` đã được gọi nhưng **không chạy được** vì môi trường thiếu `PyYAML`; không cài thêm dependency. Kiểm tra thủ công/standard library không thay thế mọi kiểm tra của validator đó.
- Kiểm tra bằng Python standard library: 13 tệp Markdown, 39 liên kết nội bộ có đích tồn tại và nằm trong gói, code fences cân bằng. Kiểm tra được chạy lại sau cập nhật cuối.

## Rà soát độc lập

Một agent mới đọc toàn bộ 13 tệp cùng thiết kế/kế hoạch, không sửa file. Không phát hiện vấn đề quan trọng cần sửa trong quy trình và cách đóng gói. Agent đã kiểm tra năm tình huống thiết kế: chuẩn mâu thuẫn, UI tương tự nhưng khác hành vi, thiếu runtime/reference, đã có quyền refactor và build từ văn bản.

Rà soát này không xác minh nghiên cứu upstream qua network, không đánh giá browser và không chứng nhận hiệu quả chung. Tại lúc agent đọc, hai lượt thực hiện mode còn đang thu kết quả; kết quả thực thi được agent chính kiểm tra riêng như bảng trên. Giới hạn này được giữ nguyên thay vì diễn giải thành mọi mặt đều đã qua review.

## Giới hạn và bước tiếp theo

Chưa chạy trong browser thật, chưa xác nhận visual fidelity, khả năng truy cập toàn diện, responsive, Figma hay môi trường ứng dụng thật. Chưa đo thời gian, token hoặc chất lượng trên nhiều repo. Một số bài thử dùng DOM giả lập chỉ bảo vệ các contract được mô hình hóa; chúng không mô phỏng layout hay đầy đủ hành vi trình duyệt.

Khi áp dụng vào dự án thật, dùng một phạm vi audit nhỏ, xem lại độ đúng của phát hiện và kiểm tra baseline trước refactor. Nếu cần chứng minh lợi ích, thực hiện đối chứng trên nhiệm vụ thật cùng revision, yêu cầu, môi trường và model; không suy ra hiệu quả từ việc tài liệu có đủ mục.
