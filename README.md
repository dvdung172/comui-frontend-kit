# ComUI Frontend Kit

Bộ skill cho AI làm frontend theo chuẩn sẵn có của từng repo, lấy cảm hứng từ ComUICoder. Dùng để rà soát source, xây UI và refactor component dựa trên trách nhiệm, hành vi và bằng chứng kiểm chứng.

**Giao việc bằng ngôn ngữ tự nhiên. Không cần điền prompt mẫu, chạy audit trước hay tạo đủ các mẫu tài liệu.** AI đọc ngữ cảnh hiện có và chỉ hỏi thêm khi thiếu thông tin ảnh hưởng đáng kể đến công việc.

## Chọn skill

| Skill | Khi dùng | Kết quả |
| --- | --- | --- |
| [`comui-audit`](skills/comui-audit/SKILL.md) | Rà soát source, tìm vấn đề hoặc cơ hội tái sử dụng | Phát hiện có bằng chứng và đề xuất refactor; không tự sửa source |
| [`comui-build`](skills/comui-build/SKILL.md) | Xây trang, feature hoặc component | Triển khai theo stack, design system và data contract của repo |
| [`comui-refactor`](skills/comui-refactor/SKILL.md) | Thực hiện thay đổi cấu trúc UI | Mã đã refactor cùng bằng chứng về các hành vi cần giữ |
| [`comui-frontend-kit`](SKILL.md) | Giữ cách gọi cũ hoặc xử lý công việc kết hợp | Tự chọn luồng phù hợp với yêu cầu; giữ bộ reference chi tiết |

Ba skill mới **độc lập**: có thể cài một hoặc nhiều skill, không cần lệnh cũ hay repo bộ kit ở thời điểm sử dụng. Mỗi thư mục chứa `SKILL.md` và metadata Codex; hướng dẫn cốt lõi nằm ngay trong skill. Lệnh cũ vẫn tự hoạt động, không bắt buộc gọi chuyển tiếp sang skill mới.

## Sử dụng

Trong Claude Code, gọi `/tên-skill` rồi viết yêu cầu của bạn. Ví dụ ngắn:

```text
/comui-audit xem phần giỏ hàng có chỗ nào nên gom component không
/comui-build thêm trạng thái rỗng cho danh sách sản phẩm
/comui-refactor gom phần dựng hai product card, giữ callback và class hiện tại
/comui-frontend-kit xem giúp cấu trúc frontend và đề xuất việc nên làm trước
```

Trong Codex, thay `/` bằng `$`, chẳng hạn `$comui-audit xem phần giỏ hàng có chỗ nào nên gom component không`. Những câu trên chỉ là ví dụ, không phải cú pháp đầu vào bắt buộc. Công cụ hỗ trợ tự chọn skill cũng có thể nạp skill phù hợp từ mô tả; mức độ tự chọn phụ thuộc công cụ và phiên làm việc. Có thể gọi tên trực tiếp để chọn rõ.

Nếu đã xác định phạm vi hoặc hành vi cần giữ, nói ngay trong yêu cầu. Nếu chưa, skill sẽ tìm ngữ cảnh trong workspace và thu hẹp phạm vi khi cần. `comui-refactor` nhận cả yêu cầu trực tiếp lẫn kế hoạch có sẵn; một báo cáo audit trước đó là tùy chọn.

Với AI có quyền đọc file nhưng không hỗ trợ skill, yêu cầu đọc `SKILL.md` của skill tương ứng rồi giao việc bình thường. Nếu chỉ dùng chat, cung cấp hướng dẫn và source liên quan, đồng thời nêu phần repo chưa được cung cấp.

## Cơ chế hoạt động

Đây là hướng dẫn Markdown mà agent đọc khi được gọi hoặc được công cụ lựa chọn. Model, khả năng đọc/sửa source, terminal, browser và quyền truy cập do công cụ AI cung cấp; bộ kit không chạy một model hay pipeline riêng.

1. **Hiểu nhiệm vụ và chuẩn repo.** Agent đọc yêu cầu, hướng dẫn áp dụng, config và code liên quan. Phân biệt quy định rõ ràng, quy tắc được công cụ cưỡng chế, convention suy ra và khuyến nghị. Repo có `.codegraph/` thì dùng CodeGraph trước khi tìm code; khi không truy cập được, ghi nhận giới hạn và dùng cách đọc thông thường.
2. **Phân tích theo trách nhiệm UI.** Liên hệ route/entrypoint → khối giao diện có ý nghĩa → component → chủ sở hữu state/data → các nơi sử dụng. Có screenshot hoặc thiết kế thì dùng thêm; chỉ có source vẫn phân tích được.
3. **Quyết định tái sử dụng.** So sánh trách nhiệm, API/event, state, vòng đời, biến thể và chi phí chuyển đổi. Chọn dùng component có sẵn, trích component/helper, giữ riêng hoặc điều tra thêm. Giao diện giống nhau chưa đủ để gom thành một component chung.
4. **Làm đúng công việc đã giao.** Audit trả nhận xét và đề xuất; build/refactor thực hiện thay đổi trong phạm vi được yêu cầu. Refactor ghi nhận các contract cần giữ thay vì âm thầm đổi hành vi.
5. **Kiểm chứng và phản hồi cụ thể.** Dùng check thực sự tồn tại trong repo; khi có runtime, kiểm tra các trạng thái và tương tác liên quan. Nếu so thiết kế, giữ điều kiện so sánh tương đương. Phản hồi chỉ rõ phần tử/selector, source và kịch bản thay vì yêu cầu chung chung như “làm đẹp hơn”.
6. **Bàn giao theo quy mô.** Nêu kết quả, bằng chứng, check đã chạy và phần chưa kiểm chứng. Trả lời ngắn hoặc lập tài liệu tùy yêu cầu; không bắt dùng một form cố định.

Agent nạp phần hướng dẫn của skill được chọn. Lệnh cũ đọc thêm reference theo nhu cầu; ba skill mới chứa hướng dẫn riêng và không cần đọc toàn bộ bộ kit. Prompt, hợp đồng component và mẫu báo cáo là tài liệu tham khảo tùy chọn.

## Ưu điểm và giới hạn

| Ưu điểm | Giá trị thực tế |
| --- | --- |
| Ưu tiên chuẩn repo | Giảm đề xuất đổi framework, cấu trúc hoặc cách đặt tên chỉ theo sở thích của AI |
| Tách audit, build và refactor | Gọi đúng công việc; nhận xét source không tự trở thành yêu cầu sửa mã |
| Reuse xét cả hành vi và state | Giúp tránh component tổng quát với nhiều cờ và các lifecycle bị ghép không cần thiết |
| Chỉ có source vẫn dùng được | Bắt đầu rà soát mà chưa cần môi trường chạy hoặc file thiết kế |
| Markdown và ba skill tự chứa hướng dẫn | Có thể cài riêng, chuyển công cụ và dùng yêu cầu tự nhiên |
| Tách các loại bằng chứng | Biết kết luận nào đến từ source, chạy thực tế hoặc so sánh thiết kế |

| Nhược điểm / giới hạn | Hệ quả khi dùng |
| --- | --- |
| Phụ thuộc năng lực model và công cụ | Cài skill không bảo đảm agent làm đúng mọi hướng dẫn hay phát hiện mọi lỗi |
| Chuẩn repo có thể thiếu hoặc xung đột | Agent vẫn cần suy luận, ghi rõ giả định hoặc hỏi lại ở quyết định quan trọng |
| Source không chứng minh toàn bộ UI | Render, tương tác, responsive, accessibility và hiệu năng cần kiểm tra tương ứng |
| Thay đổi component dùng chung có phạm vi ảnh hưởng rộng | Cần kiểm tra các consumer/variant liên quan; một build xanh chưa đủ |
| Chưa có benchmark trên nhiều dự án thực tế | Chưa thể khẳng định tăng tốc, tiết kiệm token hay cải thiện chất lượng theo một tỷ lệ |
| Bộ kit không cấp thêm quyền hay kết nối | Browser, Figma, backend, dữ liệu và quyền chạy check vẫn cần có trong môi trường AI |

## Cài đặt

Chỉ đọc/dùng skill không cần dependency. Các bước sau cần Git để tải repo và shell để chép file. Python và Codex CLI chỉ cần cho harness thử nghiệm tùy chọn.

### Tải bộ kit

Clone vào một thư mục lưu source thông thường, bên ngoài thư mục mà công cụ quét skill:

```sh
git clone https://github.com/dvdung172/comui-frontend-kit.git
cd comui-frontend-kit
```

### Chọn nơi cài

Chọn **một** scope phù hợp và đặt `COMUI_SKILLS_DIR` thành đường dẫn tương ứng:

| Công cụ / phạm vi | Thư mục đích |
| --- | --- |
| Claude Code, một project | `/path/to/project/.claude/skills` |
| Claude Code, cá nhân | `$HOME/.claude/skills` |
| Codex, một project | `/path/to/project/.agents/skills` |
| Codex, cá nhân | `$HOME/.agents/skills` |

Ví dụ cài cá nhân cho Codex, hoặc đổi dòng gán thành đích trong bảng:

```sh
COMUI_SKILLS_DIR="$HOME/.agents/skills"
```

Đường dẫn project phải là đường dẫn thật của repo muốn dùng. Scope được mô tả trong [tài liệu Claude Code](https://code.claude.com/docs/en/skills) và [tài liệu Codex](https://learn.chatgpt.com/docs/build-skills).

### Chép ba skill mới

Chạy từ thư mục bộ kit vừa clone. Có thể bỏ các tên không muốn cài khỏi danh sách trong vòng lặp:

```sh
mkdir -p "$COMUI_SKILLS_DIR"
for skill in comui-audit comui-build comui-refactor; do
  if [ -e "$COMUI_SKILLS_DIR/$skill" ] || [ -L "$COMUI_SKILLS_DIR/$skill" ]; then
    printf 'Bỏ qua vì đã tồn tại: %s\n' "$COMUI_SKILLS_DIR/$skill"
  else
    cp -R "skills/$skill" "$COMUI_SKILLS_DIR/$skill" &&
      cp LICENSE "$COMUI_SKILLS_DIR/$skill/LICENSE"
  fi
done
```

Mỗi skill được chép nguyên thư mục và kèm license. Các đường dẫn đã tồn tại được giữ nguyên. Đây là cài mới; để cập nhật bản chép, tải thay đổi ở repo nguồn, so sánh với bản đang cài và thay đúng thư mục sau khi giữ lại chỉnh sửa riêng. `git pull --ff-only` ở repo nguồn không tự cập nhật các bản chép.

### Giữ hoặc cài thêm lệnh cũ

Bản cài `comui-frontend-kit` hiện tại tiếp tục dùng được; không cần đổi lệnh hay gỡ bản cũ. Nếu bản cũ là symlink, nguồn vẫn phải tồn tại. Nếu là một Git clone riêng, cập nhật tại clone đó; tránh cài thêm các bản trùng tên ở nhiều scope.

Để cài mới lệnh cũ từ source vừa clone, dùng một thư mục đích chưa tồn tại:

```sh
COMUI_LEGACY_DIR="$COMUI_SKILLS_DIR/comui-frontend-kit"
if [ -e "$COMUI_LEGACY_DIR" ] || [ -L "$COMUI_LEGACY_DIR" ]; then
  printf 'Bỏ qua vì đã tồn tại: %s\n' "$COMUI_LEGACY_DIR"
else
  mkdir -p "$COMUI_LEGACY_DIR"
  cp SKILL.md prompts.md LICENSE "$COMUI_LEGACY_DIR/"
  cp -R agents references templates examples evaluations scripts "$COMUI_LEGACY_DIR/"
fi
```

Lệnh cũ dùng các reference đi kèm nên phải giữ cả các thư mục được chép. Cách cài này không lồng ba skill mới vào thư mục skill cũ. Không cần sửa `AGENTS.md`, `CLAUDE.md`, hook hay cấu hình model để sử dụng các skill.

Mở phiên AI trong project muốn làm việc rồi gọi skill. Nếu danh sách skill chưa cập nhật, kiểm tra vị trí `SKILL.md`, tên skill và mở lại phiên theo cơ chế công cụ. Thấy tên skill trong danh sách xác nhận việc khám phá; chất lượng thực hiện vẫn cần đánh giá riêng.

## Thử nghiệm, tài liệu và nguồn gốc

[Harness Codex](references/codex.md) là wrapper tùy chọn để chạy audit qua **lệnh cũ**, lưu log, snapshot và rubric đánh giá. Nó có prompt nội bộ cho lượt thử được kiểm soát; người dùng skill tương tác không phải viết theo prompt đó. Harness không tự build/refactor, không tự chấm chất lượng và kế thừa auth/model hiện có của Codex CLI.

- [Workflow chi tiết của lệnh cũ](references/workflow.md), [chuẩn repo](references/repo-profile.md), [phân tích component](references/component-analysis.md), [kiểm chứng](references/verification.md).
- [Ví dụ yêu cầu tùy chọn](prompts.md), [mẫu audit](templates/audit-and-refactor.md), [mẫu hồ sơ repo](templates/repo-profile.md), [mẫu component contract](templates/component-contract.md).
- [Ví dụ audit](examples/audit-example.md), [kết quả đánh giá ban đầu](evaluations/validation.md) và [thay đổi tách skill](evaluations/independent-skills.md). Kết quả cũ được ghi cho entrypoint cũ, không tự coi là bằng chứng cho ba skill mới.
- [Phân tích ComUICoder](references/comuicoder-analysis.md), [paper](https://arxiv.org/abs/2602.19276) và [repo WebPAI](https://github.com/WebPAI/ComUICoder).

Bộ kit áp dụng ý tưởng phân rã ngữ nghĩa, tái sử dụng component và phản hồi theo phần tử vào công việc frontend. Đây là bộ hướng dẫn độc lập, không phải bản triển khai chính thức của WebPAI và không tái hiện pipeline hay bảo đảm kết quả benchmark của ComUICoder.

Giấy phép: [MIT](LICENSE).
