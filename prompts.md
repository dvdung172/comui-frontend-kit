# Prompt khởi động

Thay các giá trị trong dấu `<...>` trước khi gửi. Đặt `Kit` và `Repo` thành đường dẫn mà công cụ AI thực sự đọc được. Quy trình chung nằm trong [SKILL.md](SKILL.md); các prompt chỉ chọn công việc và phạm vi.

## 1. Audit source và đề xuất refactor

```text
Kit: <path-to-comui-frontend-kit>
Repo: <path-to-repository>
Scope: <routes, packages, components, or frontend area>
Output language: Vietnamese

Read Kit/SKILL.md and follow audit mode for Repo and Scope.
Review the existing frontend against its applicable repo standards and identify
useful component reuse/refactor opportunities. This request authorizes an audit
report only. Use source evidence; record runtime and design-reference access
separately. Deliver the scoped audit and ordered refactor plan using the kit's
audit template, with the checks actually run and remaining gaps.
```

## 2. Xây mới frontend

```text
Kit: <path-to-comui-frontend-kit>
Repo: <path-to-repository>
Scope: <target feature, route, or components>
Requirements and acceptance criteria: <desired behavior and UI states>
Optional reference: <accessible design, screenshot, or none>
Output language: Vietnamese

Read Kit/SKILL.md and follow build mode. Implement Requirements within Scope
using Repo's existing stack, standards and reusable UI. A design reference is
optional; state consequential assumptions. Complete the feature and relevant
verification within the granted scope. Report changed files, behavior, evidence
and any unmet acceptance criteria.
```

## 3. Thực hiện refactor đã giao

```text
Kit: <path-to-comui-frontend-kit>
Repo: <path-to-repository>
Assigned plan: <current plan path or exact steps>
Scope: <files/components and allowed changes>
Contracts to preserve: <public APIs, events, routes, state and UI behavior>
Output language: Vietnamese

Read Kit/SKILL.md and follow refactor mode. This request authorizes implementation
of Assigned plan within Scope. Reconcile the plan with the current source, then
execute it and verify Contracts to preserve. Complete the assigned work without
requesting the same approval again. Report changes, checks, unresolved risks and
any remaining verification; surface consequential scope changes before making them.
```
