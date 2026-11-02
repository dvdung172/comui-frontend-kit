# Rà soát component sản phẩm và giỏ hàng

**Nên cân nhắc gom phần dựng hai thẻ sản phẩm vào một helper nội bộ; giữ riêng thẻ giỏ hàng.** Đây là cơ hội bảo trì, chưa có lỗi chức năng hoặc vi phạm chuẩn được xác nhận. Chỉ rà soát source, không triển khai refactor.

## Phạm vi, nguồn và chuẩn repo

Repo: `evaluation/audit`. Snapshot UTC 2026-11-02 03:26:02; không có Git hoặc `.codegraph/`. Đã đọc đầy đủ sáu file trong repo: AGENTS.md, README.md, package.json, cards.js, cart.js, cart.test.js. Không có router, trang sử dụng, stylesheet, design system, backend, ảnh tham chiếu hay browser session để mở rộng kiểm tra. Các exports là entrypoint có thể xác định được; callers bên ngoài fixture chưa được bao phủ.

- **Chỉ dẫn rõ ràng:** AGENTS.md:3–5 yêu cầu giữ public exports/event, để dữ liệu người dùng ngoài HTML strings, dùng CSS class hiện có, một trách nhiệm rõ ràng và audit chỉ xuất báo cáo. Áp dụng cho toàn bộ phạm vi.
- **Hướng dẫn tài liệu có mâu thuẫn:** README.md:3 đề nghị cũ gom mọi thẻ thành UniversalCard. AGENTS.md và hành vi hiện tại yêu cầu bảo toàn trách nhiệm/event, nên không đủ căn cứ áp dụng universal card chỉ vì giống markup. Không cần chặn rà soát để giải quyết thêm lựa chọn này.
- **Kiểm tra có thực:** package.json:1 khai báo `check = node --test cart.test.js`. Test hiện tại chỉ kiểm tra phép tính số lượng. Không có lint/typecheck/build.
- **Mẫu suy ra từ source:** cả ba exports tạo DOM trực tiếp, dùng textContent, class `card`, một heading và button. Đây là mẫu của fixture này, không suy rộng toàn dự án.
- **Khuyến nghị của kit:** cân nhắc helper nhỏ nếu thực sự giảm số nơi phải cập nhật cùng cấu trúc; không coi việc đạt tỷ lệ reuse hay giảm dòng là tiêu chí bắt buộc.

## Bản đồ trách nhiệm và dữ liệu

| Entrypoint / khối | Triển khai | State, dữ liệu và sự kiện | Consumer xác định được |
| --- | --- | --- | --- |
| Thẻ sản phẩm thường | cards.js:3 `productCard` | Nhận product; heading dùng product.title; click `Add` gọi onAdd(product.id); không tự sửa dữ liệu | Public export; không có caller trong fixture |
| Thẻ sản phẩm gọn | cards.js:27 `compactProductCard` | Cùng đầu vào và sự kiện Add; class thêm card--compact | Public export; không có caller trong fixture |
| Thẻ giỏ hàng | cards.js:15 `cartCard` | Nhận item và quantity; click `Remove one` tính nextQuantity(item.quantity, -1) rồi gọi onQuantity(id, quantity) | Public export; import cart.js:1 |
| Quy tắc số lượng | cart.js:1 `nextQuantity` | Hàm thuần, chặn kết quả dưới 0 | cartCard và cart.test.js:4 |

Cả ba nhận dữ liệu từ caller, không fetch, không subscription, không permission/state loading/empty/error nội bộ. Dữ liệu vẫn do caller sở hữu. Closure đọc thuộc tính object khi click: khi triển khai sau này không nên tự đổi sang snapshot dữ liệu trong lúc tạo card. Không có callback cleanup hoặc lifecycle bất đồng bộ để đánh giá thêm từ source này.

## Kết luận và đánh đổi

### 1. Cơ hội bảo trì: chia sẻ cấu trúc hai thẻ sản phẩm

Bằng chứng cards.js:3–12 và :27–36: cả hai phục vụ thêm sản phẩm, cấu trúc article → h2/button và callback giống nhau; khác biệt hiện tại chỉ class compact. Khi chỉnh cấu trúc hoặc action Add, người bảo trì đang phải cập nhật hai hàm. Chưa quan sát được lỗi hoặc thay đổi bị bỏ sót; mức ưu tiên thấp đến vừa nếu đang có nhu cầu cập nhật cả hai biến thể.

Có thể thêm helper **private** phục vụ riêng thẻ sản phẩm. Giữ nguyên hai exports để caller không phải di chuyển, wrapper thường/gọn truyền class tương ứng. Không cần tạo API variant công khai mới hoặc boolean cho hành vi giỏ hàng. Lợi ích là có một nơi quản lý phần product; chi phí gồm helper, hai wrapper và kiểm tra hai biến thể. Vì chỉ có hai hàm nhỏ, **giữ nguyên cũng hợp lý** nếu cấu trúc sắp phân kỳ hoặc chưa có việc thay đổi chung. Không nên refactor chỉ để bỏ vài dòng lặp.

Hợp đồng cần giữ: tên/signature exports, trả về article; DOM thứ tự h2 rồi button; class `card`/`card card--compact`; textContent cho title, nhãn `Add`; một click gọi một lần onAdd với đúng id. Không thêm state riêng, không sửa object product và không chuyển user data sang innerHTML.

### 2. Giữ riêng cartCard

cards.js:15–24 giống khung DOM nhưng trách nhiệm là giảm số lượng, khác rõ callback onQuantity(id, quantity), nhãn và quy tắc clamping cart.js:1. UniversalCard phải biết thêm hành vi quantity hoặc cấu hình action nhiều nhánh; việc thay đổi sản phẩm có thể vô tình ảnh hưởng giỏ hàng. Chưa có bằng chứng số consumer hoặc lợi ích đủ lớn để trả chi phí này.

Chỉ giữ class `card` đang dùng chung. Không đề xuất CSS/token mới vì stylesheet không được cung cấp. Nếu sau này thật sự có thay đổi shell đồng thời ở nhiều consumer, có thể đánh giá một primitive trình bày rất nhỏ riêng, nhưng hiện tại chưa cần. Giữ nguyên public API giỏ hàng, `Remove one`, callback hai tham số và clamping tại 0.

### Các quan sát có giới hạn

Chưa thấy lỗi hoặc vi phạm chuẩn được chứng minh trong sáu file. Source cho thấy button có nhãn text và dùng button native; điều đó không xác nhận toàn bộ truy cập bàn phím hay accessibility. Không có CSS để kết luận responsive/overflow; không có số đo để kết luận performance. Không có loading/error/permission code để bắt buộc bổ sung các state đó trong refactor này.

## Các bước đề xuất theo thứ tự

1. Nếu cần giảm chi phí cập nhật product, trước hết bổ sung kiểm tra DOM/event cho hai exports với các hợp đồng trên; chạy trên bản hiện tại để có baseline. Kiểm tra cả title chứa markup, class thường/gọn, đúng id và số lần gọi callback. Chưa thêm test hoặc sửa source trong audit này.
2. Chỉ trích xuất helper private cho product; giữ nguyên public wrappers. Consumer bị ảnh hưởng là hai exports cùng các callers bên ngoài chưa có trong fixture. Đọc callers thật trước khi áp dụng vào repo lớn. Nếu biến thể có chủ đích phân kỳ, chọn giữ nguyên thay vì tạo abstraction.
3. Chạy lại kiểm tra DOM/event và `npm run check`; bổ sung scenario cartCard quantity 0/1 cho callback hai tham số nếu thực hiện refactor có chạm shell chung. Khi có ứng dụng chạy, xác nhận cả hai thẻ sản phẩm và giỏ hàng ở route/state thực tế; dùng breakpoint repo quy định. Không yêu cầu browser làm điều kiện hoàn tất audit chỉ source.

## Kiểm chứng và giới hạn

- **passed:** `npm run check`, cwd repo nêu trên, snapshot này; Node test 1/1, exit 0. Xác nhận nextQuantity(1,-2)=0 và nextQuantity(2,1)=3. Đây là kết quả baseline, không chứng minh event/DOM hoặc trình bày đúng.
- **passed:** SHA-256 sáu file trước và sau kiểm tra trùng khớp; audit không sửa source.
- **not run:** test DOM/event, vì repo chưa có bài kiểm tra đó và audit không thêm hạ tầng; phương án kiểm tra ở bước 1.
- **unavailable:** runtime UI/browser và design reference theo README.md:5; chưa kiểm chứng render, tương tác UI thật, fidelity, responsive, accessibility toàn phần hay hiệu năng. Cần ứng dụng chạy và reference tương ứng cho các kết luận đó.

SHA-256:
- `AGENTS.md`: `64c669caf5ed64e60168074da1fe2171b03b8a887bf9e686abe5bc54d96555b9`
- `README.md`: `7abb328b0db682a07f100fb11e0a7bc69bbd267d637cfe10336ad404557c7703`
- `cards.js`: `1960967c15e9bf09564a4ae2f96ce23d1a5f011aa8c9eb87b1b795e8884b0c67`
- `cart.js`: `c3c6a0972a22bbfb8d0547721127274268f8e7f5df0a6f482597a70f762f607c`
- `cart.test.js`: `fb2d8d3c4e018e85f1aebed6fc3dda9cd3e996150f16e0e3c43e03a6df117944`
- `package.json`: `771fd3582352206dbe1a6053177dcb4abce221b7a46a809efe76c9388819dc06`

## Bao phủ quy trình Audit

| Stage | Trạng thái | Bằng chứng / đánh giá |
| --- | --- | --- |
| shared | done | Đọc shared contract/workflow của gói installed; giữ Audit, chỉ báo cáo; yêu cầu tự nhiên đủ ngữ cảnh |
| baseline | done | Mục phạm vi/chuẩn, snapshot sáu file, không CodeGraph/Git, check script và giới hạn môi trường |
| audit.1 | done | Bản đồ ba public exports và nextQuantity, state owner/callers đã xác định; callers ngoài fixture ghi chưa bao phủ |
| audit.2 | done | Đối chiếu ba nhóm, trách nhiệm/event/state/structure/variation/coupling/cost; phân biệt cơ hội refactor với lỗi/vi phạm chưa tìm thấy |
| audit.3 | done | Mức ưu tiên dựa chi phí cập nhật hai product consumers; chưa có lỗi người dùng được tái hiện |
| audit.4 | done | Ba bước nhỏ, hợp đồng công khai, consumers, phương án giữ nguyên và đường kiểm chứng |
| audit.5 | done | Check sẵn có 1/1; nguồn không đổi; DOM/runtime/reference được ghi rõ chưa chạy hoặc unavailable |
| completion | done | Toàn bộ source được yêu cầu đã rà soát, kết luận có locator và kế hoạch kiểm chứng; hoàn tất báo cáo source-only, không tuyên bố hành vi UI đã được xác minh |
