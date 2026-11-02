# Audit qua skill cá nhân đã cài

Ngày: 2026-11-01. Đây là nội dung audit của một agent Codex mới trong phiên app, gọi skill đã cài bằng tên. Liên kết được chuyển sang đường dẫn tương đối để báo cáo đi cùng gói. Agent không được đọc kết quả đánh giá hoặc báo cáo trước đó.

Audit chỉ từ mã nguồn; chưa thấy lỗi chức năng được xác nhận. Refactor đáng làm nhất là gom phần dựng hai thẻ sản phẩm, giữ thẻ giỏ hàng riêng.

## Phạm vi và snapshot

Đã đọc toàn bộ sáu tệp fixture: hướng dẫn, README, manifest, hai mô-đun nguồn và test. Không có Git hoặc `.codegraph/`. Snapshot agent ghi lúc `2026-11-01T09:05:14Z`; SHA-256 rút gọn: `cards.js` → `1960967c15e9`, `cart.js` → `c3c6a0972a22`, `cart.test.js` → `fb2d8d3c4e01`.

Luồng hiện có: bên gọi cung cấp dữ liệu và callback → các hàm tạo DOM. `cards.js` không giữ state riêng; `cartCard` dùng hàm thuần `nextQuantity`. Fixture không cung cấp route, bên gọi bên ngoài hoặc CSS.

## Chuẩn áp dụng

[AGENTS.md](fixtures/cards/AGENTS.md) yêu cầu giữ public exports và hành vi sự kiện, không chèn dữ liệu người dùng vào chuỗi HTML, dùng class hiện có và phân trách nhiệm rõ ràng. Nguồn hiện dùng `textContent`, đáp ứng quy tắc dữ liệu.

[README.md](fixtures/cards/README.md) ghi hướng dẫn cũ gom mọi thẻ thành `UniversalCard`. Không nên áp dụng máy móc: chỉ dẫn hiện hành và hợp đồng callback cho thấy thẻ sản phẩm và giỏ hàng có trách nhiệm khác nhau.

## Phát hiện và quyết định tái sử dụng

| Phát hiện | Bằng chứng và tác động | Đề xuất |
| --- | --- | --- |
| Cơ hội refactor: hai thẻ sản phẩm lặp cấu trúc | [cards.js](fixtures/cards/cards.js), `productCard` dòng 3 và `compactProductCard` dòng 27 chỉ khác class; sửa markup/nút phải sửa hai nơi | Helper nội bộ dựng thẻ sản phẩm; giữ nguyên hai export và class hiện hành. Khuyến nghị bảo trì, không phải vi phạm chuẩn |
| Giữ `cartCard` riêng | `cartCard` dòng 15 phát `onQuantity(id, nextQuantity(quantity, -1))`, khác `onAdd(id)` của sản phẩm | Giữ phép tính lượng trong `cart.js`; chưa cần trích thêm khung thẻ chung |
| Khoảng trống kiểm chứng UI | [cart.test.js](fixtures/cards/cart.test.js) chỉ kiểm tra phép tính lượng, chưa kiểm tra export, DOM hoặc click | Bổ sung kiểm tra hợp đồng trước refactor; test hiện tại chưa bảo đảm UI được giữ nguyên |

## Thứ tự refactor đề xuất

1. Ghi nhận và kiểm tra hợp đồng ba export: DOM `article > h2 + button`, class, nhãn nút, title dạng văn bản và đối số callback khi click.
2. Trích helper sản phẩm nội bộ; giữ chữ ký `productCard(product, onAdd)` và `compactProductCard(product, onAdd)`, không thêm state hoặc export. Rủi ro chính là đổi class hoặc callback ngoài ý muốn.
3. Chạy lại kiểm tra hợp đồng và check hiện có. Khi có ứng dụng chạy được, kiểm tra hai biến thể sản phẩm cùng thao tác giảm lượng, gồm lượng bằng `0`. Giữ nguyên hành vi giỏ hàng trong refactor cấu trúc.

## Kiểm tra thực tế và giới hạn

Agent chạy `npm run check` tại fixture: **passed**, 1 test, 0 lỗi; script chỉ chạy `node --test cart.test.js`. Không cài đặt, khởi động dịch vụ hoặc sửa tệp.

Chưa chạy trình duyệt, responsive, bàn phím hoặc so sánh thiết kế. Không có screenshot, backend, CSS hay phiên trình duyệt để xác nhận các mặt này.

Skill đã phân giải: `~/.agents/skills/comui-frontend-kit/SKILL.md`, trỏ tới source gói trong workspace. Lượt này chứng minh sử dụng hướng dẫn qua bản cài trong môi trường agent hiện tại, không phải lượt `codex exec` thành công hoặc kiểm thử selector UI bằng computer use.
