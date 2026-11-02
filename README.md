# ComUI Frontend Kit

Bộ Markdown cho AI xây frontend và rà soát source để đề xuất refactor, lấy cảm hứng từ ComUICoder. Ưu tiên chuẩn repo, giữ nguyên hành vi khi refactor và gắn kết luận với bằng chứng.

## Bắt đầu

Để gọi nhanh trong Codex, dùng `$comui-frontend-kit`. Xem [cài đặt và harness thử nghiệm](references/codex.md) để chạy audit read-only, lưu bằng chứng và đánh giá kết quả.

Giữ nguyên cả thư mục này. Chọn một yêu cầu trong [prompts.md](prompts.md), thay đường dẫn và phạm vi rồi gửi cho AI có quyền đọc repo của bạn. Ví dụ:

```text
Đọc <đường-dẫn-kit>/SKILL.md và dùng luồng audit.
Repo: <đường-dẫn-dự-án>.
Phạm vi: các trang sản phẩm và giỏ hàng cùng component liên quan.
Rà soát source, ưu tiên chuẩn repo và đề xuất refactor.
Xuất báo cáo bằng tiếng Việt. Chỉ audit, chưa sửa source.
```

Với công cụ hỗ trợ skill, đặt **toàn bộ thư mục** vào vị trí skill mà công cụ của bạn hỗ trợ. `SKILL.md` trỏ đến cùng bộ Markdown; không cần adapter riêng. Với công cụ không hỗ trợ skill, yêu cầu đọc tệp đó bằng đường dẫn là đủ nếu công cụ có khả năng đọc file. Nếu chỉ dùng chat, cung cấp các tệp được luồng yêu cầu cùng source liên quan; ghi rõ phần repo chưa cung cấp.

Sau khi có bản public, cài trực tiếp vào Claude Code của một project hoặc thư mục skill cá nhân của Codex:

```sh
# Claude Code, chỉ cho project hiện tại
git clone https://github.com/dvdung172/comui-frontend-kit.git .claude/skills/comui-frontend-kit

# Codex, dùng ở mọi project của tài khoản máy này
git clone https://github.com/dvdung172/comui-frontend-kit.git ~/.agents/skills/comui-frontend-kit
```

Trong Claude Code gọi `/comui-frontend-kit`; trong Codex gọi `$comui-frontend-kit`.

## Chọn công việc

| Bạn cần | Luồng | Đầu ra chính |
| --- | --- | --- |
| Khảo sát source, tìm cơ hội cải thiện | Audit | Phát hiện có bằng chứng và kế hoạch refactor |
| Xây trang, feature hoặc component mới | Build | Mã frontend và bằng chứng kiểm tra |
| Thực hiện kế hoạch refactor đã giao | Refactor | Thay đổi trong phạm vi và kiểm chứng giữ hành vi |

Quy trình nằm ở [workflow.md](references/workflow.md). Luồng audit mặc định không sửa source. Một yêu cầu thực hiện refactor rõ ràng cho phép AI làm trong phạm vi đã giao; bộ khung không thêm bước duyệt lặp lại.

## Tài nguyên

- [Nạp chuẩn repo](references/repo-profile.md): phân biệt quy định, mẫu suy ra và khuyến nghị.
- [Phân tích component](references/component-analysis.md): phân rã, tái sử dụng, state và phạm vi ảnh hưởng.
- [Kiểm chứng](references/verification.md): source, runtime, reference và giới hạn kết luận.
- [Phân tích ComUICoder](references/comuicoder-analysis.md): bằng chứng nghiên cứu và phần mở rộng của bộ khung.
- Mẫu [hồ sơ repo](templates/repo-profile.md), [audit và kế hoạch](templates/audit-and-refactor.md), [hợp đồng component](templates/component-contract.md).
- [Ví dụ audit](examples/audit-example.md): trường hợp nên tái sử dụng và trường hợp nên giữ riêng.
- [Kết quả kiểm tra gói](evaluations/validation.md): phạm vi đã thử và giới hạn.

## Cách dùng vừa đủ

Với việc nhỏ, nhúng hồ sơ, hợp đồng và kiểm chứng vào một báo cáo. Với việc lớn, tách tài liệu theo phạm vi cần bàn giao. AI chỉ nạp phần cần cho nhiệm vụ; không bắt sinh mọi mẫu hoặc gọi nhiều agent.

Chỉ có source vẫn audit được. Khi có môi trường chạy hoặc thiết kế tham chiếu, mở rộng kiểm tra theo dữ liệu thực sự truy cập được. Bộ khung không tự cung cấp browser, model, quyền ghi file hoặc khả năng đọc Figma.

Đây là bộ hướng dẫn do tác giả bộ khung thiết kế, không phải bản triển khai chính thức của WebPAI và chưa có bằng chứng đạt các kết quả benchmark của ComUICoder. Đọc và dùng tài liệu không cần dependency. Harness tùy chọn dùng Python standard library và Codex CLI đã cài.
