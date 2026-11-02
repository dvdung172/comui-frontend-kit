# Bàn giao Refactor độc lập

Đã thực hiện yêu cầu tự nhiên bằng `comui-refactor`, chỉ trong luồng Refactor. Hai export `productCard` và `compactProductCard` sử dụng chung helper private `createProductCard` trong `refactor/cards.js:3`. Mỗi wrapper truyền đúng class hiện có. Đã bổ sung `refactor/cards.test.js` cho hợp đồng DOM/callback; không thêm dependency hay sửa script package.

## Profile và phạm vi

- Repo fixture: `evaluation/refactor`, JavaScript ES modules, native DOM, Node test runner; không có Git hoặc `.codegraph/`. Snapshot ngày 2026-11-02, đã đọc toàn bộ sáu file ban đầu: `AGENTS.md`, `README.md`, `package.json`, `cards.js`, `cart.js`, `cart.test.js`. Không tìm thấy route/router/style file/caller ngoài ba public exports trong fixture.
- Quy định explicit: `AGENTS.md` yêu cầu ổn định public exports/event, dữ liệu người dùng không đưa vào HTML string, giữ CSS classes; user giới hạn vào hai product cards và giữ giỏ hàng. Enforced check: `package.json#scripts.check` chỉ chạy quantity test.
- README có hướng dẫn cũ gom mọi card vào UniversalCard. Đây không đủ cơ sở cho việc gộp giỏ hàng: trách nhiệm, callback và quantity khác product. Ưu tiên quy định ổn định hợp đồng và scope user; dùng helper private là đề xuất phù hợp của kit, không quy định universal của repo.
- Chỉ có source và mock DOM; README nêu không có screenshot, browser session, backend. Không có design reference/runtime render. Không cài công cụ hoặc khởi động dịch vụ.

## Phân tích và hợp đồng

Map: public `productCard` / `compactProductCard` → product summary + Add action → `createProductCard` → caller sở hữu product/onAdd, DOM instance và listener tạo mới từng lần. Public `cartCard` → cart quantity action → caller sở hữu item/onQuantity, `nextQuantity` xử lý floor về 0; giữ riêng.

Hai product variants có cùng trách nhiệm, DOM `article > h2 + button`, nút `Add`, title gán `textContent`, callback `onAdd(product.id)`; chỉ khác class `card` và `card card--compact`. Không có subscription, async, cleanup hoặc state lifecycle riêng. Helper nhận class private; public API hai arguments, exports và instance isolation giữ nguyên; không thêm boolean flags hay migration caller. Ba export hiện có vẫn là `productCard`, `cartCard`, `compactProductCard`. User không yêu cầu đổi behavior; không phát hiện bug ngoài scope cần sửa. Không có permission/loading/error state trong implementation cần hợp nhất.

## Kiểm tra thực hiện

Mọi command trong thư mục fixture; không có dependency ngoài Node/npm sẵn có.

| Check | Baseline | Sau sửa | Bằng chứng và giới hạn |
| --- | --- | --- | --- |
| `npm run check` | passed 1/1 | quantity test được chạy lại trong lệnh tổng bên dưới | Existing `cart.test.js` xác nhận quantity floor; không chứng minh render |
| `node --test cards.test.js` | passed 4/4 trước sửa source | passed 4/4 trong lệnh tổng | Hai variants giữ tag/order/class/title raw text/Add text/click arguments và independent instances |
| `node --test cards.test.js cart.test.js` | không chạy lệnh tổng ở baseline; từng suite đã passed | passed 5/5 | Regression oracle dựa trên hợp đồng public, không gọi helper private |
| `node --check cards.js` | not run | passed | Syntax hợp lệ |
| Browser/render/a11y/responsive/reference comparison | unavailable | unavailable | Không có browser/design/styles/viewports fixture; mock DOM không chứng minh visual hay real browser interaction |

Baseline `cards.js` SHA256: `1960967c15e9bf09564a4ae2f96ce23d1a5f011aa8c9eb87b1b795e8884b0c67`; sau sửa: `9fab311f73f0fb3a2fa6a456460704df4226c0beac8617ae59c08fea2b665055`. Trước chỉnh source đã tạo và chạy test hồi quy, tất cả passed; test không bị thay đổi sau refactor.

`cart.js` giữ SHA256 `c3c6a0972a22bbfb8d0547721127274268f8e7f5df0a6f482597a70f762f607c`; `cart.test.js` giữ `fb2d8d3c4e018e85f1aebed6fc3dda9cd3e996150f16e0e3c43e03a6df117944`. Toàn bộ block `cartCard` trong `cards.js` giữ nguyên khi apply patch. Hash của AGENTS/README/package cũng giữ nguyên. Thay đổi là helper/product wrappers và test mới.

## Coverage đầy đủ của luồng

| Stage/step | Status | Bằng chứng/đánh giá |
| --- | --- | --- |
| `shared` | done | Đọc SKILL, core, workflow và đủ ba operational references từ thư mục skill độc lập; scope và authorization áp dụng; không gọi flow/skill khác |
| `baseline` | done | Profile sáu file, SHA256 source trước sửa, rules và conflict README, map consumers, npm check + focused contract baseline |
| `refactor.1` | done | Không cần prior audit/plan; suy ra thay đổi nhỏ helper private sau baseline observable 1+4 tests passed |
| `refactor.2` | done | Ghi hợp đồng DOM/classes/exports/events/state; regression độc lập hai variants; không có route/permission trong fixture |
| `refactor.3` | done | Một extraction coherent chỉ cho products; kiểm tra purpose/behavior/state/structure/variation/coupling/cost; cả hai variants và cart check sau sửa |
| `refactor.4` | done | Đánh giá bug ngoài scope: không phát hiện bug cần behavior change; cart giữ riêng, hướng dẫn UniversalCard cũ không được áp đặt |
| `refactor.5` | done | Hợp đồng và hash được ghi, 5 tests + syntax passed sau sửa; không có intentional behavior change, runtime/visual chưa xác minh |
| `completion` | done | Patch yêu cầu đã triển khai và checks có sẵn được thực hiện; ghi giới hạn mock DOM/runtime; không có required blocked action trong scope source fixture |

Implementation hoàn tất theo phạm vi fixture và bằng chứng source/mock DOM. Chưa xác minh browser/visual; nếu triển khai vào ứng dụng thật, bước tiếp theo là render hai variants và kích hoạt Add bằng browser ở viewport của repo.
