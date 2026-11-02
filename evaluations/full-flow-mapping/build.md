# Bàn giao thử nghiệm comui-build độc lập

Đã thêm `productList(products, onAdd)` ở `build/cards.js:15` và kiểm tra theo hợp đồng yêu cầu. Chỉ thực thi Build; không gọi Audit, Refactor hay skill khác. Đã đọc trọn `SKILL.md`, `references/core.md`, `references/workflow.md`, `references/repo-profile.md`, `references/component-analysis.md` và `references/verification.md` trong thư mục skill cài độc lập. Không đọc kit nguồn hoặc tài nguyên của luồng khác.

## Phạm vi và baseline

Repo fixture: `evaluation/build`. Không có Git, `.codegraph/`, dependency cài thêm, router, CSS, design tokens, backend hoặc browser. Đã đọc toàn bộ sáu file gốc, gồm hướng dẫn, manifest, các export và test. Không có callers khác trong fixture. Snapshot theo file ngày 2026-11-02:

| File gốc | SHA-256 trước |
| --- | --- |
| AGENTS.md | 64c669caf5ed64e60168074da1fe2171b03b8a887bf9e686abe5bc54d96555b9 |
| README.md | 7abb328b0db682a07f100fb11e0a7bc69bbd267d637cfe10336ad404557c7703 |
| cards.js | 1960967c15e9bf09564a4ae2f96ce23d1a5f011aa8c9eb87b1b795e8884b0c67 |
| cart.js | c3c6a0972a22bbfb8d0547721127274268f8e7f5df0a6f482597a70f762f607c |
| cart.test.js | fb2d8d3c4e018e85f1aebed6fc3dda9cd3e996150f16e0e3c43e03a6df117944 |
| package.json | 771fd3582352206dbe1a6053177dcb4abce221b7a46a809efe76c9388819dc06 |

Không có thay đổi có trước nào trong fixture được ghi nhận trong quá trình làm việc; do không có Git, bảng hash là baseline thay cho lịch sử. Sau triển khai, năm file gốc ngoài cards.js giữ nguyên hash. cards.js có hash `1f2504206e39fa813dcd2dbd22bfaa0af2d989321a99d337e9431d433f5bf23d`; file test mới `cards.test.js` có hash `376b7201b5983dfbb19f862f41b3087c6001a07ee37bf282645c6e443a50126d`.

## Chuẩn và quyết định

- **Explicit:** AGENTS.md yêu cầu giữ public exports/hành vi event, dùng class hiện có, tránh đưa dữ liệu người dùng vào HTML string và mỗi component một trách nhiệm. Hướng dẫn README về UniversalCard được đánh dấu là cũ; không phù hợp để thay API ổn định trong nhiệm vụ này.
- **Enforced:** manifest dùng ES module; `npm run check` chạy test quantity hiện có. Không có lint/typecheck/build script.
- **Inferred:** source tạo DOM bằng `document.createElement`, gán dữ liệu bằng `textContent`, truyền callback từ consumer. Áp dụng đúng phạm vi cards.js đã đọc.
- **Kit recommendation:** compose từ productCard để dùng lại cấu trúc và event có sẵn; không thêm lớp abstraction hoặc class CSS chưa tồn tại.

Bản đồ trách nhiệm: entrypoint `productList` → khối danh sách/empty → `productCard` cho mỗi phần tử → data và callback do caller sở hữu. ProductCard tạo article.card, tiêu đề h2 và nút Add; cartCard giữ luồng quantity qua nextQuantity. compactProductCard vẫn là biến thể hiện tại. Không có lifecycle, subscription hoặc state bất đồng bộ.

Danh sách dùng productCard vì trùng đúng trách nhiệm và hợp đồng hiển thị sản phẩm; giữ nguyên id/callback, thứ tự đầu vào và textContent. Không gộp cartCard với productCard vì event quantity có trách nhiệm khác. Không sửa compactProductCard vì không thuộc thay đổi yêu cầu. API mới không thêm variant hoặc boolean flags; không di chuyển framework, asset hay backend contract.

## Hành vi và triển khai

`cards.js:15` export `productList(products, onAdd)` nhận mảng sản phẩm cùng dạng dữ liệu của productCard và callback `onAdd(id)`. Hàm trả section; mảng có phần tử thì append từng productCard theo thứ tự; mảng rỗng thì append một p chứa chính xác `Chưa có sản phẩm`. Hàm không mutate mảng. Callback tiếp tục do caller quản lý. Không yêu cầu thay kiểu đầu vào null/undefined, fetch, loading/error, permission hay navigation; các trạng thái đó không có trigger trong hợp đồng đồng bộ này. Không thêm visual design assumptions ngoài native section/p và class card hiện có.

Thay đổi gồm `cards.js` và test mới `cards.test.js`. Các export productCard, cartCard, compactProductCard giữ nguyên code/body, public callback và class CSS. Không thay callers vì fixture không có consumer ứng dụng.

## Kiểm chứng

Tất cả command chạy tại `evaluation/build`, dùng Node sẵn có; không cài dependency hay khởi động service.

| Check | Kết quả | Bằng chứng và giới hạn |
| --- | --- | --- |
| `npm run check` trước sửa | passed | 1/1 test quantity; baseline không có lỗi |
| `node --test cards.test.js` trước implementation mới | failed | 2 test card cũ pass; 2 test list mới fail đúng vì productList chưa tồn tại |
| `npm run check` sau sửa | passed | 1/1 test quantity |
| `node --test cards.test.js` sau sửa | passed | 4/4 test: product/compact card structure, class, text và add event; cart quantity callback; list thứ tự/article.card/text/callback/input không mutate; empty section/p/text |
| `node --check cards.js` sau sửa | passed | Parse ES module thành công |
| Native browser rendering, responsive, keyboard/a11y, visual reference | unavailable | Không browser/design/runtime ứng dụng trong fixture; DOM test double chỉ xác minh construction và callback, không chứng minh native rendering/visual hoặc accessibility |

Oracle của test dựa vào yêu cầu công khai section/article/p/text/event cùng hành vi baseline, không suy ra expected bằng implementation mới. Hai test list mới đã được quan sát fail trước khi thêm hàm. Đã kiểm tra mọi consumer/variant có trong fixture: product, compact, cart và list mới. Không có lỗi cụ thể còn lại để sửa. Kiểm tra tiếp nếu tích hợp app thật: render section và cả empty/populated state trong browser, click Add và kiểm tra layout/breakpoint thực tế theo stylesheet của ứng dụng; hiện không có tuyên bố về những điều đó.

## Bao phủ đầy đủ luồng

| ID | Trạng thái | Evidence locator hoặc lý do |
| --- | --- | --- |
| shared | done | Đọc đầy đủ core/workflow; thực thi Build được user giao; phạm vi/hashes/chuẩn/evidence trong báo cáo này; không chuyển luồng |
| baseline | done | Đọc cả6 file gốc và manifest; bảng SHA trước/sau; AGENTS/README; npm check baseline; không có CodeGraph/Git/router/style/consumer khác |
| build.1 | done | Acceptance: section chứa productCard từng item hoặc p empty chính xác; giữ card cũ; điều tra DOM/class/callback sẵn có; synchronous states đã nêu |
| build.2 | done | Đọc component-analysis đầy đủ; bản đồ entrypoint→block→component→owner→consumer; quyết định reuse productCard, giữ cart riêng; API list mới và chi phí abstraction đã nêu |
| build.3 | done | cards.js:15-27 triển khai list nhỏ nhất, compose export hiện có; public card bodies giữ nguyên; input/user text/callback không đổi |
| build.4 | done | Đọc verification đầy đủ; baseline1/1; kiểm tra mới red rồi green4/4; existing check1/1; parse pass; hash giữ file khác; native browser/reference thiếu đã phân loại unavailable, không thuộc acceptance bắt buộc của fixture |
| completion | done | Changed files, resulting behavior, checks, source snapshot và limitations trong báo cáo này; hợp đồng có thể kiểm tra tại fixture đã đạt; không tuyên bố hoàn tất kiểm chứng visual/browser |

Không dùng template bắt buộc hoặc prompt mẫu. Những điều kiện không áp dụng đã đánh giá rõ: không async loading/error/permission, không backend, không migration, không screenshot/viewport compare. Báo cáo hoàn tất và patch đạt các tiêu chí hành vi kiểm tra được trong fixture; native rendering chưa được xác minh.
