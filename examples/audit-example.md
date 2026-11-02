# Ví dụ audit: product card và cart card

**Dữ liệu giả lập để minh họa định dạng.** Tên file, vị trí và snapshot bên dưới thuộc một repo tưởng tượng; đây không phải báo cáo chạy trên dự án thật và không có lệnh nào được thực thi trong ví dụ này.

## Phạm vi và kết quả

- Repo giả lập `storefront-demo`, snapshot `demo-v1`.
- Mode: audit, không sửa source.
- Đã cung cấp: `AGENTS.md`, `README.md`, `package.json`, `src/cards.ts`, `src/cart.ts`, `tests/cart.test.ts`.
- Chưa cung cấp: route/caller bên ngoài, CSS, runtime, ảnh hoặc reference.
- Quy định giả lập: giữ nguyên exports/callbacks, dùng class sẵn có, gán dữ liệu người dùng qua `textContent`.
- README cũ khuyên dùng một `UniversalCard`. Đề xuất dưới đây không giả định chỉ dẫn này đủ để thay đổi hợp đồng sự kiện; cần giữ các contract hiện hành.

Bản đồ từ source được cung cấp:

| Trách nhiệm UI | Implementation | State/data | Hành vi |
| --- | --- | --- | --- |
| Hiển thị sản phẩm | `productCard(product, onAdd)` | Caller sở hữu product | Click gọi `onAdd(product.id)` |
| Hiển thị sản phẩm dạng gọn | `compactProductCard(product, onAdd)` | Cùng hợp đồng product | Như product card; thêm class `card--compact` |
| Điều chỉnh giỏ hàng | `cartCard(item, onQuantity)` | Caller sở hữu quantity | Click gọi `onQuantity(id, nextQuantity(quantity, -1))` |

## F-01 — Hai implementation product card lặp cùng logic

- **Loại:** cơ hội refactor, không phải bug chức năng.
- **Vị trí:** `src/cards.ts`, symbols `productCard` và `compactProductCard`, snapshot `demo-v1`.
- **Bằng chứng source giả lập:** cả hai tạo cùng article, title, button và callback `onAdd`; chỉ khác class compact.
- **Căn cứ:** khuyến nghị của bộ khung về chia sẻ cấu trúc ổn định; hợp đồng exports/callbacks là quy định repo giả lập. Không có quy tắc bắt buộc mọi card phải gom.
- **Tác động/ưu tiên:** cơ hội bảo trì mức vừa; một thay đổi product card hiện phải sửa hai chỗ. Chưa đo số lỗi hoặc thời gian tiết kiệm.
- **Đề xuất:** một hàm dựng product card nội bộ nhận variant nhỏ theo quy ước repo; giữ nguyên hai public exports làm wrapper tương thích.
- **Phạm vi ảnh hưởng:** hai product exports; cần tìm caller thật trước khi triển khai.
- **Giữ nguyên:** class, thứ tự phần tử, nội dung, số lần và đối số callback, cách đưa text vào DOM.
- **Kiểm chứng:** so sánh DOM và hành vi click của cả hai public exports trước/sau; kiểm tra caller/variant thực tế khi có repo đầy đủ. Chưa chạy.
- **Đánh đổi:** thêm một hàm nội bộ; chỉ có lợi nếu API vẫn đơn giản hơn phần lặp.

## Q-01 — Button có thể có hành vi submit khi đặt trong form

- **Loại:** câu hỏi cần điều tra.
- **Vị trí:** `src/cards.ts`, các lệnh `document.createElement('button')` trong ba hàm.
- **Bằng chứng source giả lập:** chưa gán thuộc tính `type`; không có caller để biết card có nằm trong form không.
- **Căn cứ:** kiểm tra hành vi tích hợp, không có quy định repo buộc thay đổi thuộc tính này.
- **Tác động/ưu tiên:** chưa xếp là lỗi đã xác nhận; cần kiểm tra nếu card được dùng trong form.
- **Đề xuất:** tìm caller và thử click trong ngữ cảnh thật. Nếu hành vi sai được xác nhận, ghi thành bug fix riêng; không âm thầm đổi hành vi trong refactor F-01.
- **Kiểm chứng:** kịch bản click và quan sát submit/navigation trong form; runtime hiện chưa có.

## Quyết định tái sử dụng

| Ứng viên | Phần chung | Khác biệt phải giữ | Quyết định |
| --- | --- | --- | --- |
| Hai product card | DOM, dữ liệu, callback | Class mật độ hiển thị | Đề xuất share implementation nội bộ, giữ exports |
| Product card và cart card | Khung article và class | Mục đích, callback, quantity/state | Giữ hành vi riêng; cân nhắc primitive trình bày chỉ khi đủ lợi ích |

Hợp đồng ngắn cho phần product: `product` giữ shape hiện hành; `onAdd(id)` được gọi một lần/click; caller sở hữu dữ liệu; public wrappers giữ tên và chữ ký; variant chỉ chọn class thường/gọn. Không đưa `onQuantity` hay state giỏ hàng vào API này.

## Kế hoạch refactor

| Bước | Thay đổi | Phụ thuộc / lợi ích | Kiểm chứng / rủi ro |
| --- | --- | --- | --- |
| 1 | Tìm caller hai product exports, xác lập baseline | Cần repo đầy đủ; tránh bỏ sót tích hợp | Ghi DOM, callbacks, variants; chưa làm được từ dữ liệu ví dụ |
| 2 | Thêm kiểm tra contract khi môi trường phù hợp | Sau bước 1; bảo vệ đường hành vi bị chạm | Chạy trước refactor, không chỉ assert tên helper mới |
| 3 | Extract hàm nội bộ trong `src/cards.ts`, giữ wrappers | Sau baseline; một nơi sửa logic product | Chạy lại checks và consumer; rủi ro đổi class/callback |
| 4 | Quan sát các route/viewport liên quan | Sau triển khai; xác minh layout | Runtime/reference cần có; không khẳng định pixel fidelity |

## Kiểm tra và bàn giao

| Kiểm tra | Trạng thái trong ví dụ | Giới hạn |
| --- | --- | --- |
| Đọc source giả lập | Quan sát phục vụ minh họa | Không bao phủ repo thật |
| Lệnh check của repo | `not run` | Ví dụ không chạy lệnh |
| Contract DOM/callback | `not run` | Cần fixture/môi trường test phù hợp |
| Runtime/responsive | `unavailable` | Chưa có app chạy/CSS |
| Đối chiếu thiết kế | `unavailable` | Chưa có reference |

Audit minh họa hoàn tất trong phạm vi source giả lập; phần runtime chưa được kiểm chứng. Source chưa sửa. Bước tiếp theo là giao rõ việc thực hiện F-01 trên repo thật, sau khi xác định caller và baseline.
