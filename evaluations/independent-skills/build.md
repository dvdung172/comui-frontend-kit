# Handoff comui-build độc lập

Đã thêm export `productList(products, onAdd)` vào `build/cards.js`. Hàm trả `section` chứa card cho từng sản phẩm bằng cách tái sử dụng `productCard`; khi mảng rỗng, section chứa một `p` có nội dung “Chưa có sản phẩm”. Callback vẫn nhận đúng ID sản phẩm. Không thêm CSS class chưa tồn tại. Nội dung sản phẩm tiếp tục đi qua `textContent`.

Giữ nguyên toàn bộ mã của ba card hiện tại và năm file khác trong fixture (đã kiểm tra trước/sau). Fixture không có Git hoặc `.codegraph/`, nên không có diff Git hay CodeGraph để dùng. README cũ gợi ý UniversalCard; yêu cầu hiện tại và AGENTS ưu tiên trách nhiệm rõ ràng, không cần hợp nhất các card cho tính năng này.

Kiểm tra đã chạy:
- `npm run check`: đạt 1/1 test quantity hiện có.
- Kiểm tra Node với DOM giả trong bộ nhớ: đạt phần tử section, thứ tự/nội dung card, mảng rỗng và thông điệp chính xác, callback onAdd, dữ liệu title dùng textContent, callback của productCard/compactProductCard/cartCard hiện có.
- Không chạy browser, kiểm chứng thị giác hoặc accessibility; môi trường fixture không cung cấp browser/design/backend.

Skill không gây vướng. Chỉ đọc bản `installed/comui-build/SKILL.md` và fixture build; không cần gọi skill audit, không cần prompt mẫu hoặc báo cáo trước triển khai, không đọc bộ kit nguồn, không network/dependency/subagent. Yêu cầu tự nhiên đủ để triển khai trực tiếp.
