# Tích hợp skill/harness vào Codex

Ngày: 2026-11-01. Kết quả: **đã cài, Codex phát hiện đúng skill và audit qua agent hiện tại thành công**. Harness CLI có 11 test đạt; thực nghiệm CLI thật đang bị giới hạn bởi backend tài khoản từ chối model.

## Bản cài

- Tên gọi: `$comui-frontend-kit`; tên hiển thị: **ComUI Frontend**.
- Vị trí cá nhân: `~/.agents/skills/comui-frontend-kit`.
- Kiểu cài phát triển: symlink tới toàn bộ gói workspace; không sao chép nhiều bộ quy tắc.
- Metadata được sinh bằng công cụ `skill-creator`, có display name, short description và default prompt audit. Giữ implicit invocation theo mặc định; không thêm policy hoặc branding ngoài yêu cầu.
- Không sửa global AGENTS, `config.toml`, đăng nhập hay các skill khác.

Codex CLI `0.140.0` được kiểm tra tại máy này. Lần gọi `skills/list` qua app-server với `forceReload: true` trả đúng **một** skill cùng tên, `scope: user`, `enabled: true`, metadata đúng và không có lỗi parser cho skill. Xem [bằng chứng discovery](codex-native-discovery.json). Đây là khám phá native; chưa click kiểm tra selector trong một cửa sổ UI đang mở.

## Harness và kiểm tra cơ học

[trial.py](../scripts/trial.py) là wrapper standard-library cho audit read-only: prompt, report, event JSONL, stderr, thời gian, usage nếu có, source hashes và rubric review riêng. Nó dùng auth/config hiện hành; `--model` chỉ override cho một lượt.

[Bộ test](../scripts/test_trial.py) ban đầu thất bại vì chưa có harness. Sau triển khai, chín test đạt. Review độc lập phát hiện snapshot có thể đọc FIFO và treo ngoài timeout; regression test đã tái hiện timeout. Đã sửa bằng kiểm tra regular file trước đọc. Khi bổ sung `--model`, test cũng ghi nhận tính năng còn thiếu trước khi triển khai. Kết quả cuối: **11/11 test đạt**.

Các test bảo vệ: read-only/approval flags, đường dẫn chứa dấu cách, loại trừ dữ liệu không cần hash/symlink, output ngoài repo và không ghi đè, lưu evidence/usage, nonzero exit, timeout và partial logs, report thiếu, source mutation không rollback, error event, model chỉ định riêng và FIFO không block.

Review không phát hiện vấn đề quan trọng khác; việc cưỡng chế quyền của MCP kế thừa và hành vi sandbox thật không được test bằng các process giả lập. Tài liệu đã nêu rõ giới hạn đó. Không diễn giải unit test thành chứng minh mọi tích hợp đều chỉ đọc.

## Các lượt CLI thật

| Lượt | Model yêu cầu | Kết quả | Thời gian CLI | Source hash |
| --- | --- | --- | --- | --- |
| 1 | Kế thừa config: `gpt-6.1-sol` | Backend `400 model_not_found`, không hỗ trợ với ChatGPT account | 5,676 giây | Không đổi |
| 2 | `gpt-5.5`, default trong catalog cục bộ | Backend từ chối cùng loại lỗi | 5,153 giây | Không đổi |
| 3 | `gpt-5.3-codex`, cũng có trong catalog | Backend từ chối cùng loại lỗi | 5,263 giây | Không đổi |

Xem [tóm tắt lỗi thật](codex-cli-attempts.json). Các lượt đều được harness đánh dấu `failed`, không có `report.md` và usage là `null`; không tính thành bài audit đạt. Không suy ra model thực sự khả dụng chỉ từ catalog và không tiếp tục thử model nối tiếp. Lần đầu gọi app-server trong sandbox cũng bị chặn SQLite tại `~/.codex`; sau khi chạy với quyền được cho phép, discovery thành công.

Các raw evidence được giữ ở thư mục tạm trên máy thử và không nằm trong gói public; bản tóm tắt ở trên đủ để hiểu kết quả mà không phụ thuộc các tệp đó.

## Lượt sử dụng skill đã cài trong agent Codex

Agent mới nhận yêu cầu gọi skill bằng tên và audit fixture đi kèm, không được xem báo cáo/evaluation trước đó. Nó đã phân giải bản cài cá nhân, đọc các reference cần thiết, audit source và chạy check hiện hữu. [Báo cáo audit](installed-skill-audit.md).

Đánh giá nội dung do agent chính thực hiện trên source và report; không phải reviewer hoàn toàn độc lập hoặc bằng chứng thống kê:

| Tiêu chí | Kết quả quan sát |
| --- | --- |
| Nạp skill cá nhân | Đúng đường dẫn symlink đã cài |
| Chuẩn repo và xung đột | Nêu AGENTS, nhận diện README cũ và giữ contract |
| Đề xuất reuse | Hai product variant share implementation, giữ wrappers |
| Khác biệt hành vi/state | Giữ cart card và callback quantity riêng |
| Báo cáo truy nguyên | Có symbols, vị trí, snapshot hashes, loại nhận xét và kế hoạch |
| Kiểm chứng và giới hạn | `npm run check`: 1/1 đạt; nói rõ chưa browser/render |
| Source preservation | Đối chiếu sáu file với fixture gốc: không đổi |

Lượt này không đo usage của agent và không chứng minh hiệu quả trên dự án sản xuất. Nó xác nhận workflow có thể được dùng qua skill cá nhân ở phiên Codex hiện tại, tách khỏi lỗi tài khoản/model trên CLI.

## Cách thử tiếp

Trong chat Codex, gọi `$comui-frontend-kit audit frontend repo hiện tại; chỉ báo cáo và kế hoạch, chưa sửa source.` Skill mới có thể cần lượt tiếp theo hoặc restart nếu UI chưa cập nhật.

Để chạy lại CLI, trước tiên xác minh model thực sự được backend tài khoản CLI hỗ trợ; sau đó truyền `--model` vào harness. Không có cấu hình tài khoản/model nào được thay đổi trong lần tích hợp này. Với repo thật, bắt đầu bằng một vùng UI nhỏ và dùng [rubric trong hướng dẫn](../references/codex.md) để đánh giá phát hiện trước khi thực hiện refactor.
