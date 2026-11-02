# ComUI Frontend Kit

Bộ skill giúp AI rà soát, xây mới và refactor frontend theo chuẩn sẵn có của từng repository. Dùng với Claude Code, Codex hoặc công cụ AI có khả năng đọc hướng dẫn Markdown và source code.

## Giới thiệu

### Vấn đề

Làm frontend trong một dự án có sẵn đòi hỏi hiểu cách repo tổ chức component, quản lý state, gọi API và kiểm chứng thay đổi. Một component mới có thể trùng phần đã có; hai khối UI nhìn giống nhau có thể mang hành vi khác nhau; một lần gom code có thể làm đổi callback, quyền truy cập hoặc trạng thái giao diện.

ComUI Frontend Kit cung cấp quy trình để AI xem xét các yếu tố đó trước khi kết luận hoặc sửa mã. Kết quả cần bám source và chuẩn của dự án, đồng thời cho biết phần nào đã được kiểm tra và phần nào còn thiếu bằng chứng.

### Hướng giải quyết

Bộ kit tổ chức công việc thành ba nhiệm vụ: **Audit**, **Build** và **Refactor**. Mỗi nhiệm vụ có một skill độc lập; lệnh chung `comui-frontend-kit` vẫn được giữ để chọn luồng từ yêu cầu.

Các skill cùng áp dụng những nguyên tắc sau:

- **Đọc chuẩn repo trước khi đề xuất.** Xem hướng dẫn, cấu hình và code liên quan; phân biệt quy định rõ ràng, quy tắc được công cụ kiểm tra, convention suy ra và khuyến nghị của AI.
- **Phân rã theo trách nhiệm UI.** Liên hệ route/entrypoint với khối giao diện, component, nơi sở hữu state/data và các nơi sử dụng.
- **Quyết định reuse từ hành vi.** So sánh trách nhiệm, API/event, vòng đời state, biến thể và chi phí thay đổi trước khi dùng lại hoặc trích component. Giữ riêng là một kết quả hợp lệ.
- **Kiểm chứng theo bằng chứng có thật.** Phân biệt nhận xét từ source, quan sát khi chạy ứng dụng và so sánh với thiết kế; chỉ ghi một check là đạt khi đã thực hiện và có kết quả.

Ba skill độc lập được ánh xạ **1–1** từ phần hướng dẫn chung và đúng luồng tương ứng của `comui-frontend-kit`, kèm đầy đủ reference vận hành. Chúng được [sinh và kiểm tra từ một nguồn chung](scripts/sync_skills.py), không phải các bản hướng dẫn rút gọn. Mỗi skill chỉ thực hiện nhiệm vụ của mình, không tự chạy luồng khác hay yêu cầu chạy skill khác trước.

### Quy trình trong skill

Mỗi nhiệm vụ bắt đầu bằng việc đọc hướng dẫn chung và lập mốc ban đầu: xác định phạm vi, phiên bản source, thay đổi có trước, chuẩn áp dụng, caller liên quan và các check có thể chạy. Nếu repo có `.codegraph/`, skill yêu cầu dùng CodeGraph trước để hiểu hoặc định vị code; khi không truy cập được, ghi nhận giới hạn và dùng cách đọc source thông thường.

Sau đó, AI thực hiện đầy đủ các bước của luồng được chọn:

| Luồng | Các bước chính | Kết quả |
| --- | --- | --- |
| [Audit — 5 bước](skills/comui-audit/references/workflow.md) | Lập bản đồ UI/source → điều tra vấn đề và nhóm component → đánh giá ưu tiên → đề xuất thay đổi có thứ tự → chạy check phù hợp và ghi giới hạn | Báo cáo có bằng chứng, quyết định reuse và kế hoạch; không triển khai sửa source |
| [Build — 4 bước](skills/comui-build/references/workflow.md) | Làm rõ hành vi/trạng thái cần có → chọn component và xác định hợp đồng → triển khai trong stack hiện tại → kiểm tra, sửa lỗi quan sát được và kiểm tra lại | Feature, trang hoặc component đã triển khai cùng kết quả kiểm chứng |
| [Refactor — 5 bước](skills/comui-refactor/references/workflow.md) | Đối chiếu yêu cầu/kế hoạch với source và baseline → xác định hành vi cần giữ → thực hiện thay đổi có phạm vi → tách riêng bug ngoài phạm vi → kiểm chứng và báo cáo các hợp đồng được giữ | Mã đã refactor cùng bằng chứng về hành vi và giao diện công khai |

Khi bàn giao, AI phải ghi nhận `shared`, `baseline`, từng bước của luồng và `completion`, kèm bằng chứng hoặc lý do cụ thể. Bước hoàn thành dùng `done`; nhánh điều kiện không phát sinh dùng `not applicable` kèm lý do; việc bắt buộc còn thiếu dùng `blocked` cùng điều kiện cần bổ sung. Không được bỏ bước rồi tuyên bố đã hoàn tất.

Cách viết yêu cầu và định dạng báo cáo có thể linh hoạt. Các bước quy trình vẫn phải được thực hiện đầy đủ; prompt mẫu và mẫu tài liệu chỉ là trợ giúp tùy chọn.

### Phạm vi áp dụng

Bộ kit là hướng dẫn cho agent, không tự cung cấp model, browser, Figma, backend hay quyền đọc/sửa file. Có source là đủ để bắt đầu audit; xác nhận render, tương tác, responsive hoặc độ khớp thiết kế cần môi trường và bằng chứng tương ứng. Nếu thiếu một điều kiện bắt buộc của nhiệm vụ, skill phải ghi rõ phần chưa hoàn thành.

Bộ kit lấy cảm hứng từ phân rã ngữ nghĩa, tái sử dụng component và phản hồi theo phần tử trong [ComUICoder](https://arxiv.org/abs/2602.19276), tham khảo [repo WebPAI](https://github.com/WebPAI/ComUICoder). Đây là bộ hướng dẫn độc lập, không phải bản triển khai chính thức hoặc cam kết đạt benchmark của bài báo. Xem [phân tích nguồn nghiên cứu](references/comuicoder-analysis.md) và [kết quả kiểm tra ánh xạ](evaluations/full-flow-mapping.md).

## Hướng dẫn sử dụng

### Chọn skill theo nhiệm vụ

| Skill | Khi sử dụng |
| --- | --- |
| [`comui-audit`](skills/comui-audit/SKILL.md) | Muốn rà soát source, tìm vấn đề, đánh giá reuse hoặc nhận đề xuất refactor |
| [`comui-build`](skills/comui-build/SKILL.md) | Muốn triển khai một trang, feature, component hoặc trạng thái UI mới |
| [`comui-refactor`](skills/comui-refactor/SKILL.md) | Muốn thực hiện thay đổi cấu trúc frontend và giữ các hành vi đã xác định |
| [`comui-frontend-kit`](SKILL.md) | Muốn dùng lệnh chung để AI chọn luồng phù hợp từ yêu cầu |

Có thể dùng riêng một skill. Refactor nhận cả yêu cầu trực tiếp lẫn kế hoạch có sẵn; không bắt buộc phải có báo cáo audit trước. Nếu yêu cầu thuộc nhiệm vụ khác với skill đang gọi, skill sẽ nêu sự không khớp và hỏi bạn chọn lại thay vì âm thầm đổi luồng.

### Giao việc bằng ngôn ngữ tự nhiên

Mở công cụ AI trong project cần làm việc. Với **Claude Code**, gọi `/tên-skill` rồi viết yêu cầu:

```text
/comui-audit xem phần giỏ hàng có chỗ nào nên gom component không
/comui-build thêm trạng thái rỗng cho danh sách sản phẩm, dùng component đang có
/comui-refactor gom phần dựng hai product card, giữ callback và class hiện tại
/comui-frontend-kit rà soát cấu trúc frontend và đề xuất việc nên làm trước
```

Với **Codex**, dùng `$tên-skill`, ví dụ:

```text
$comui-refactor gom phần dựng hai product card, giữ callback và class hiện tại
```

Đây là ví dụ, không phải prompt bắt buộc. Bạn có thể nói thêm phạm vi, hành vi cần giữ, thiết kế hoặc tiêu chí chấp nhận khi đã biết. AI sẽ tìm ngữ cảnh trong repo và chỉ hỏi thêm ở những lựa chọn quan trọng chưa thể xác định.

Với công cụ chưa hỗ trợ skill nhưng đọc được file, yêu cầu đọc `SKILL.md` trong thư mục skill tương ứng rồi giao việc bình thường. Các reference nằm cùng thư mục phải được cung cấp đầy đủ.

### Đọc kết quả

Kết quả cần cho biết phạm vi đã xử lý, bằng chứng, quyết định về component và coverage từng bước. Với Build/Refactor, cần có thêm thay đổi đã thực hiện, hành vi liên quan và check đã chạy. Check dùng trạng thái `passed`, `failed`, `not run` hoặc `unavailable`.

Một báo cáo audit chỉ từ source có thể hoàn thành với giới hạn UI được nêu rõ. Một nhiệm vụ yêu cầu xác nhận render vẫn cần bằng chứng render. Khi xem kết quả, đối chiếu coverage với bằng chứng thực tế; việc có hướng dẫn đầy đủ không bảo đảm mọi model luôn thực thi đúng.

## Cài đặt

Các bước dưới đây dành cho Claude Code và Codex chạy local. Dùng skill không cần dependency bổ sung; Git và shell được dùng để tải và chép file. [Harness Codex tùy chọn](references/codex.md) mới cần Python và Codex CLI.

### 1. Tải bộ kit

Clone repo vào một thư mục lưu source thông thường, bên ngoài nơi công cụ quét skill:

```sh
git clone https://github.com/dvdung172/comui-frontend-kit.git
cd comui-frontend-kit
```

### 2. Chọn thư mục cài

Chọn một phạm vi phù hợp:

| Công cụ | Dùng trong một project | Dùng cho tài khoản máy hiện tại |
| --- | --- | --- |
| Claude Code | `/path/to/project/.claude/skills` | `$HOME/.claude/skills` |
| Codex | `/path/to/project/.agents/skills` | `$HOME/.agents/skills` |

Đặt `COMUI_SKILLS_DIR` thành thư mục đã chọn. Ví dụ cài cá nhân cho Claude Code:

```sh
COMUI_SKILLS_DIR="$HOME/.claude/skills"
```

Nếu cài theo project, thay bằng đường dẫn tuyệt đối thật của project. Các vị trí cài được mô tả trong [tài liệu Claude Code](https://code.claude.com/docs/en/skills) và [tài liệu Codex](https://learn.chatgpt.com/docs/build-skills).

### 3. Cài các skill độc lập

Chạy từ thư mục repo bộ kit vừa clone. Có thể bỏ tên skill không cần dùng khỏi danh sách:

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

Giữ nguyên toàn bộ thư mục đã chép, gồm `SKILL.md`, `references/`, `templates/`, `mapping.json` và metadata. Sau khi cài bằng bản chép, skill không phụ thuộc vị trí repo bộ kit nữa.

### 4. Cài lệnh chung nếu cần

Nếu đã có `comui-frontend-kit`, tiếp tục dùng bản cài đó. Để cài mới lệnh chung, chạy thêm:

```sh
COMUI_LEGACY_DIR="$COMUI_SKILLS_DIR/comui-frontend-kit"
if [ -e "$COMUI_LEGACY_DIR" ] || [ -L "$COMUI_LEGACY_DIR" ]; then
  printf 'Bỏ qua vì đã tồn tại: %s\n' "$COMUI_LEGACY_DIR"
else
  mkdir -p "$COMUI_LEGACY_DIR"
  cp SKILL.md prompts.md LICENSE "$COMUI_LEGACY_DIR/"
  cp -R agents references templates examples evaluations "$COMUI_LEGACY_DIR/"
  mkdir -p "$COMUI_LEGACY_DIR/scripts"
  cp scripts/trial.py scripts/test_trial.py "$COMUI_LEGACY_DIR/scripts/"
fi
```

Lệnh chung cần các tài nguyên đi kèm, vì vậy không chỉ chép riêng `SKILL.md`. Có thể cài lệnh chung cùng ba skill độc lập hoặc chỉ cài những skill cần dùng.

### 5. Kiểm tra và cập nhật

Mở phiên Claude Code/Codex trong project và gọi một tên skill đã cài. Nếu chưa thấy tên, kiểm tra thư mục đích, sự tồn tại của `SKILL.md` và mở lại phiên theo cơ chế của công cụ. Không cần sửa `AGENTS.md`, `CLAUDE.md`, hook hay cấu hình model để dùng bộ skill.

Các lệnh cài ở trên **bỏ qua thư mục đã tồn tại**. Để cập nhật, tải thay đổi tại repo nguồn bằng `git pull --ff-only`, so sánh với bản đang cài, giữ lại chỉnh sửa riêng rồi thay đầy đủ thư mục skill cần cập nhật. Cập nhật repo nguồn không tự cập nhật các bản đã chép. Nếu dùng bản cài symlink từ trước, nguồn của symlink phải tiếp tục tồn tại.

Giấy phép: [MIT](LICENSE).
