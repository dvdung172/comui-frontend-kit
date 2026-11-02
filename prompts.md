# Ví dụ yêu cầu — tùy chọn

Gọi skill rồi viết yêu cầu bằng ngôn ngữ tự nhiên. Không cần giữ đúng câu chữ, điền đủ các trường hay dùng một mẫu báo cáo. Skill sử dụng workspace và cuộc trò chuyện hiện tại; chỉ hỏi thêm khi thiếu thông tin quan trọng không tìm được trong repo.

Các ví dụ dùng cú pháp Claude Code `/tên-skill`; với Codex dùng `$tên-skill`. Không có thứ tự chạy bắt buộc giữa các skill. Lệnh cũ `comui-frontend-kit` vẫn nhận các yêu cầu tương tự và chọn luồng phù hợp.

## Audit

```text
/comui-audit xem phần danh sách sản phẩm có chỗ nào nên tái sử dụng component không
```

Nếu muốn làm rõ phạm vi, bổ sung tự nhiên: “xem cả caller, ưu tiên chuẩn repo; chỉ báo cáo, chưa sửa source”. Kết quả có thể trả trực tiếp trong chat; [mẫu audit](templates/audit-and-refactor.md) chỉ là gợi ý tổ chức nội dung.

## Build

```text
/comui-build thêm trạng thái rỗng cho danh sách sản phẩm, dùng component đang có trong repo
```

Có thể đưa thêm thiết kế, trạng thái cần hỗ trợ hoặc tiêu chí chấp nhận khi đã biết. Chỉ có mô tả bằng lời vẫn dùng được; skill sẽ làm rõ lựa chọn quan trọng và nêu giả định thiết kế liên quan.

## Refactor

```text
/comui-refactor gom phần dựng hai product card, giữ callback và class hiện tại
```

Không cần có một báo cáo audit hoặc kế hoạch riêng trước đó. Nếu đã có kế hoạch, chỉ cần dẫn đến tài liệu hoặc nói các bước muốn thực hiện; skill đối chiếu với source hiện tại trước khi sửa.

## Lệnh cũ

```text
/comui-frontend-kit rà soát cấu trúc UI của giỏ hàng và đề xuất việc nên làm trước
```

Giữ cùng phạm vi và quyền thực hiện: yêu cầu rà soát tạo báo cáo/đề xuất; yêu cầu triển khai cho phép thay đổi đã giao. Các tài liệu [workflow](references/workflow.md) và [kiểm chứng](references/verification.md) giải thích chi tiết cho lệnh cũ.
