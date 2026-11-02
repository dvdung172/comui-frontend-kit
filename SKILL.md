---
name: comui-frontend-kit
description: Use when building frontend pages or components, auditing existing frontend source, or implementing an assigned UI refactor within a repository's own standards. Relevant when component boundaries, reuse across pages, or precise UI feedback matter.
---

# ComUI Frontend Kit

Use the target repo's standards and evidence to improve frontend structure and behavior. The kit is self-contained; no other skill or provider-specific tool is required.

This original entrypoint remains available alongside the independent `comui-audit`, `comui-build` and `comui-refactor` skills. Use the user's natural request and conversation to choose the work; calling another skill, filling a prompt template or providing a prior audit/plan is not a prerequisite. Infer available context from the workspace and ask only about consequential missing choices. Adapt output to the user rather than requiring a fixed report form.

Read [workflow.md](references/workflow.md) first and choose audit, build or refactor from the user's request. Read the corresponding section and follow its completion criteria.

Essential boundaries:

- An audit produces a report and plan; source edits require an implementation request. Existing authorization for build/refactor remains valid within its scope.
- Record source snapshot, reviewed scope and uncovered areas. Distinguish explicit/enforced rules, inferred conventions and kit recommendations.
- Similar UI creates reuse candidates. Evaluate responsibility, public behavior, state ownership and abstraction cost before merging.
- Separate source evidence, runtime observations and reference comparisons. State the checks actually performed and what remains unverified.

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

Scale output to the task. Embed relevant template fields in one report for small work. Follow the user's language. Source-only review is useful; missing runtime or design references limit only the claims that depend on them.
