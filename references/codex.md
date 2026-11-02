# Dùng nhanh trong Codex

## Gọi skill

```text
$comui-frontend-kit audit frontend của repo hiện tại, ưu tiên chuẩn repo.
Xuất phát hiện có bằng chứng và kế hoạch refactor; chưa sửa source.
```

Hoặc giao triển khai rõ phạm vi:

```text
$comui-frontend-kit thực hiện refactor theo kế hoạch <đường-dẫn-kế-hoạch>.
Giữ nguyên public API và hành vi; kiểm chứng các caller bị ảnh hưởng.
```

Skill có tên hiển thị **ComUI Frontend**, với prompt mặc định chọn audit. Các luồng chính vẫn nằm trong [workflow.md](workflow.md); metadata không tạo quyền ghi hoặc thay đổi cấu hình Codex.

## Cài để phát triển/thử nghiệm

Đặt toàn bộ thư mục `comui-frontend-kit` vào `~/.agents/skills/`, hoặc tạo symlink cùng tên trỏ tới gói đang phát triển. Không tạo hai bản cùng tên ở nhiều scope. Không ghi đè một thư mục skill hiện hữu chưa rõ nguồn.

Codex hỗ trợ symlink khi khám phá skill; skill mới/cập nhật được tự phát hiện. Nếu selector chưa hiện, thử lượt tiếp theo hoặc khởi động lại Codex. Đây là cơ chế được mô tả trong [tài liệu OpenAI](https://learn.chatgpt.com/docs/build-skills); khả năng nhìn thấy trong một cửa sổ đang mở vẫn cần xác minh thực tế.

Symlink giữ một nguồn để chỉnh sửa: chuyển/xóa thư mục nguồn sẽ làm hỏng bản cài. Để gỡ bản cài phát triển, chỉ bỏ symlink sau khi kiểm tra đích; không xóa thư mục nguồn hoặc skill khác. Không cần đổi global `AGENTS.md`, thêm hook hay sửa `config.toml`.

## Harness audit

Harness dùng Python standard library và `codex` CLI đã cài, kế thừa đăng nhập/config/model hiện hành. Nó không đọc hoặc in credential, không yêu cầu API key mới và không có cơ chế gọi model riêng.

Từ thư mục kit, xem lệnh trước khi chạy:

```bash
python3 -B scripts/trial.py --dry-run
```

Chạy một lượt trên fixture đi kèm:

```bash
python3 -B scripts/trial.py
```

Chạy audit trên repo thật với phạm vi rõ:

```bash
python3 -B scripts/trial.py --repo "/path/to/project" \
  --scope "product pages, cart and related components" \
  --output "/path/outside-project/comui-run-001"
```

`--output` phải là thư mục mới ngoài repo đang audit. Nếu bỏ qua, harness tạo thư mục tạm và in đường dẫn. Mặc định timeout 300 giây; có thể đặt `--timeout`. Một lượt thật dùng quota/tài nguyên của cấu hình Codex hiện hành; dry-run và unit test không gọi model.

Nếu model mặc định của CLI bị tài khoản từ chối, dùng `--model <model-được-tài-khoản-hỗ-trợ>` cho riêng lượt thử. Catalog chỉ là gợi ý: trong phiên tích hợp, backend từ chối cả model mặc định và hai model thử từ catalog. Không có thay đổi model/config toàn cục. Model được yêu cầu được ghi trong `run.json`, tách khỏi model hiệu lực chưa được xác nhận độc lập. Nếu còn `model_not_found`, giữ nguyên bằng chứng lỗi, xác minh model/quyền tài khoản CLI trước lượt tiếp; vẫn có thể gọi skill trực tiếp trong app khi phiên app hoạt động.

Harness cố định `--sandbox read-only`, `--ask-for-approval never`, `--ephemeral` và JSONL. Nó không thực hiện build/refactor tự động; hãy giao hai công việc đó qua skill tương tác. Không bật bỏ sandbox khi một check bị chặn. Chi tiết lệnh được xác minh từ CLI của môi trường; xem [non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode).

Read-only sandbox giới hạn thao tác filesystem qua shell. Harness kế thừa cấu hình Codex, kể cả các tích hợp có sẵn; nó yêu cầu model chỉ dùng shell/check local và không gọi MCP/network, nhưng chưa có cơ chế riêng cưỡng chế quyền của MCP bên ngoài. Không diễn giải cờ read-only thành sandbox cho mọi dịch vụ đã kết nối.

## Đọc kết quả

Mỗi lượt giữ `prompt.txt`, `report.md` khi model có trả lời, `events.jsonl`, `stderr.log`, `run.json` và `review.md`.

- `run.json`: trạng thái thực thi, return code, thời gian, usage thật nếu CLI cung cấp, snapshot trước/sau và file thay đổi. Model được kế thừa cấu hình; harness chưa xác nhận độc lập model hiệu lực.
- `review.md`: rubric để người dùng hoặc reviewer độc lập chấm **pass/fail/unknown** cùng bằng chứng. Mặc định `not reviewed`.
- `completed` chỉ có nghĩa process thành công, không có error event, có báo cáo không rỗng và snapshot source không đổi. Chất lượng nội dung phải được đánh giá riêng.

Snapshot loại trừ thư mục dependency/build/VCS, `.env*`, file đuôi khóa credential, symlink, file không thông thường như FIFO/socket và file lớn hơn 16 MiB. Danh sách chính xác được ghi trong `run.json`; “source không đổi” chỉ áp dụng phần được hash, không phải chứng nhận toàn bộ ổ đĩa. Snapshot là bằng chứng bổ sung cho filesystem và không tự rollback.

Với fixture cards, kiểm tra report có nhận diện đúng hai product variant có thể share implementation, giữ cart behavior riêng, bảo toàn callback/exports, xử lý README cũ theo chuẩn repo và ghi rõ chưa kiểm chứng browser. Không dùng tìm keyword để tự chấm chất lượng. Với dự án thật, lấy tiêu chí chấp nhận độc lập trước khi thử.

Log có thể chứa nội dung source mà Codex đã đọc; giữ ở nơi phù hợp với dữ liệu dự án. Các file tạm của lượt thử không tự được dọn để tránh mất bằng chứng.

## Kiểm tra harness không gọi model

```bash
python3 -B scripts/test_trial.py
```

Các test dùng process giả lập cho thành công, lỗi, timeout, report thiếu, mutation và usage. Kết quả thử CLI thật được lưu riêng trong [bản ghi tích hợp](../evaluations/codex-integration.md).
