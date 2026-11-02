# Handoff: comui-refactor độc lập

Đã thực hiện trực tiếp yêu cầu tự nhiên, chỉ đọc SKILL.md đã cài riêng và fixture. Không cần audit trước, plan mẫu hoặc lời xác nhận bổ sung; không gọi skill/agent khác.

Trong `cards.js`, hai public exports `productCard` và `compactProductCard` gọi helper riêng `createProductCard(product, onAdd, className)`. Helper dùng `textContent`, giữ article → h2 + button, chữ Add, hai CSS class tương ứng và callback click `onAdd(product.id)`. Không áp dụng đề xuất UniversalCard cũ trong README vì gom cart sẽ vượt scope và làm lẫn trách nhiệm callback.

`cartCard` giữ nguyên từng ký tự; SHA256 của năm file còn lại không đổi. Fixture không có `.git` hoặc `.codegraph`, nên baseline ghi bằng hash (cards.js trước: `1960967c15e9bf09564a4ae2f96ce23d1a5f011aa8c9eb87b1b795e8884b0c67`, sau: `f9d315fccb062e0a56a42151fde6287773c77f80783e0ace991d6650ab0099c4`).

Kiểm chứng thực tế:

- Passed trước và sau: `npm run check`, 1/1 test quantity.
- Passed trước và sau: focused check bằng Node/mock DOM cho danh sách public exports, markup, class, text (bao gồm chuỗi HTML làm dữ liệu), không callback khi dựng, callback đúng payload sau click cho cả hai product variants.
- Passed trước và sau: check cart riêng, Remove one + callback `(id, 0)` khi quantity=0.
- Passed sau: hash các file ngoài cards.js và đối chiếu nguyên văn thân cartCard.
- Unavailable: browser, ảnh tham chiếu và backend trong fixture. Chưa xác minh layout trực quan hoặc keyboard/focus trong trình duyệt; mock DOM chỉ chứng minh các contracts được kiểm tra.

Không có điểm vướng do skill: hướng dẫn độc lập đủ để xác định baseline, triển khai refactor nhỏ và nêu giới hạn bằng chứng; không bắt dùng prompt hoặc template.
