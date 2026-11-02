---
name: comui-frontend-kit
description: Use when building frontend pages or components, auditing existing frontend source, or implementing an assigned UI refactor within a repository's own standards. Relevant when component boundaries, reuse across pages, or precise UI feedback matter.
---

# ComUI Frontend Kit

Read the complete [shared contract](references/core.md) and [workflow](references/workflow.md). Select Audit, Build or Refactor from the user's request, then execute the shared stages, every numbered step of that flow and the completion checks. Account for each stage/step with evidence or an explicit applicability/blocking reason in the chosen output form.

This original entrypoint remains available alongside `comui-audit`, `comui-build` and `comui-refactor`. Each independent skill contains the same shared contract, the complete corresponding flow and full operational references, generated from this kit. It fixes the flow instead of selecting one. No prior ComUI skill, prompt template, audit report or written plan is required.

Load supporting material when needed:

| Need | Resource |
| --- | --- |
| Discover applicable repo standards and checks | [repo-profile.md](references/repo-profile.md) |
| Map UI responsibilities, evaluate reuse or define contracts | [component-analysis.md](references/component-analysis.md) |
| Establish a baseline, verify a change or report missing evidence | [verification.md](references/verification.md) |
| Optionally structure an audit and ordered refactor plan | [audit-and-refactor.md](templates/audit-and-refactor.md) |
| Capture a substantial reusable profile | [repo-profile template](templates/repo-profile.md) |
| Specify a proposed component API | [component-contract.md](templates/component-contract.md) |
| Understand research provenance and limits | [comuicoder-analysis.md](references/comuicoder-analysis.md) |
| Run a bounded Codex audit trial and review its evidence | [Codex quick start](references/codex.md) |

Templates are optional presentation aids; workflow execution and evidence requirements remain mandatory. The shared contract defines scope, natural-language input and evidence boundaries for all four entrypoints.
