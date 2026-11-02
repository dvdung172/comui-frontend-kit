# Ba skill độc lập

**Bản ghi lịch sử cho bản cô đọng tại commit `1600703`.** Bản hiện tại dùng ánh xạ đầy đủ; xem [đánh giá mới](full-flow-mapping.md). Các quan sát dưới đây không tự chuyển thành bằng chứng cho phiên bản mới.

Ngày: 2026-11-02. Baseline bộ kit trước thay đổi: commit `e75071a`. Các kết quả dưới đây áp dụng cho bản tách skill đi cùng bản ghi này, tách khỏi đánh giá entrypoint cũ.

## Thay đổi và ranh giới

Giữ `comui-frontend-kit` tại gốc repo. Thêm `skills/comui-audit`, `skills/comui-build` và `skills/comui-refactor`; mỗi thư mục chứa hướng dẫn tự đủ và metadata Codex, không tham chiếu file bên ngoài thư mục. Prompt mẫu, mẫu báo cáo và kế hoạch riêng là tùy chọn cả ở entrypoint cũ lẫn mới.

README giải thích cơ chế, ưu nhược điểm, cài đặt và cách dùng bằng yêu cầu tự nhiên. Harness CLI giữ entrypoint cũ để tương thích; không đổi cấu hình model hay mở rộng quyền của harness.

## Kiểm tra đóng gói

- Dùng Ruby YAML parser kiểm tra frontmatter và metadata của bốn entrypoint: tên duy nhất, đủ name/description và metadata tương ứng. Ba metadata mới được tạo bằng công cụ `skill-creator`.
- Kiểm tra liên kết nội bộ của source và các bản chép; các tài nguyên cần cho entrypoint cũ đều tồn tại. Số liên kết ở lượt kiểm tra đầu nằm trong [results.json](independent-skills/results.json); đây là kiểm tra file/link, không phải chất lượng suy luận.
- Kiểm tra cú pháp cả bốn shell block trong README. Thực thi hai block cài mới vào hai thư mục tạm có dấu cách, tương ứng bố trí Claude/Codex: có đủ ba skill mới và entrypoint cũ, mỗi bản có MIT license; không lồng lại các skill mới trong bản cũ.
- Thực thi lại các block cài đặt: toàn bộ file đã có, gồm một file tùy chỉnh thêm, giữ nguyên theo SHA-256. Các block bỏ qua bản cài đã tồn tại, không tự cập nhật chúng.
- Harness cũ: `python3 -B scripts/test_trial.py` đạt **11/11** tại source và tại bản cài được chép theo README; đây là test process giả lập, không gọi model hay chứng minh sandbox của mọi tích hợp.

Không cài hoặc thay cấu hình skill trong project thật. Việc chép file vào đường dẫn đúng chưa chứng minh các selector UI của Claude Code/Codex đã khám phá bản mới.

## Thử hành vi từ yêu cầu tự nhiên

Ba agent riêng nhận bản skill đã chép độc lập và một bản sao fixture cards. Mỗi agent chỉ đọc skill được giao cùng fixture, không xem báo cáo cũ hoặc reference của bộ kit. Không network, browser, dependency mới hay skill/agent bổ sung. Yêu cầu được viết như câu giao việc thông thường, không dùng prompt mẫu hay template.

| Skill | Yêu cầu | Kết quả được đối chiếu |
| --- | --- | --- |
| Audit | “Xem các thẻ sản phẩm và giỏ hàng có chỗ nào nên cải thiện hoặc gom component không; trả lời ngắn” | Đề xuất helper cho hai product variant, giữ riêng cart và public wrappers; xử lý README cũ theo AGENTS; cả sáu file không đổi |
| Build | “Thêm productList(products,onAdd) trả section chứa productCard; rỗng thì p ghi Chưa có sản phẩm; giữ card hiện tại” | Thêm export trong cards.js, có empty state và callback đúng; năm file khác và ba card hiện có giữ nguyên |
| Refactor | “Gom phần dựng productCard và compactProductCard; giữ exports, class, markup, callbacks; đừng đổi giỏ hàng” | Trích helper riêng, giữ hai export; cartCard và năm file khác giữ nguyên; không yêu cầu audit/kế hoạch trước hoặc xác nhận thêm |

Báo cáo agent: [audit](independent-skills/audit.md), [build](independent-skills/build.md), [refactor](independent-skills/refactor.md). Agent chính đọc source/diff, báo cáo và đối chiếu hash trước/sau; nhận xét không phải đánh giá độc lập thống kê.

## Đối chiếu contract

[Check contract](independent-skills/public-contracts.mjs) do agent chính chuẩn bị trước khi các agent triển khai, nằm ngoài fixture mà chúng nhận. Nó kiểm tra DOM/event công khai bằng Node với DOM giả: article/h2/button, textContent với dữ liệu giống HTML, class hai product variant, callback Add và cart ở quantity 0/dương. Nhánh build kiểm tra section, danh sách có dữ liệu, empty state và callback từ card con.

Trước triển khai, check contract cũ đạt; check tính năng build thất bại vì chưa có export productList. Sau triển khai, agent chính chạy lại check trên cả ba bản fixture: **đạt**; `npm run check` hiện hữu cũng đạt 1/1 ở mỗi bản. Việc này bảo vệ các contract đã mô hình hóa, không phải render browser.

Có thể dùng check với một fixture đã được triển khai bởi agent:

```sh
node evaluations/independent-skills/public-contracts.mjs /absolute/path/to/fixture/cards.js
node evaluations/independent-skills/public-contracts.mjs /absolute/path/to/build-fixture/cards.js --build
```

## Giới hạn

Một tình huống nhỏ cho mỗi skill cho thấy các bản chép có thể được dùng độc lập bằng yêu cầu tự nhiên và không cần mẫu có sẵn. Chưa có đối chứng mới để chứng minh cải thiện so với entrypoint cũ, đo token/thời gian, kiểm tra trên nhiều framework hoặc repo sản xuất. Chưa chạy browser, responsive, keyboard/focus, so thiết kế hay gọi ba tên mới qua native Claude/Codex selector. Không diễn giải mock DOM và metadata hợp lệ thành bằng chứng cho các khả năng đó.
