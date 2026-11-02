---
name: comui-build
description: Use when implementing a frontend page, feature, or component using a repository's existing stack, design system, and reusable UI. Executes the full Build flow only; a prior audit is not required.
---

# ComUI Build

Fixed flow: **Build**. This package is the complete Build projection of `comui-frontend-kit`, including the shared stages and full operational references. It is generated from the canonical kit and works as a standalone installed folder.

Read the complete [shared contract](references/core.md) and [workflow](references/workflow.md) before working. Execute the shared rules, baseline, every numbered Build step and completion checks. Read the operational references when the workflow names them; their requirements are not replaced by this entrypoint. Account for every stage/step with evidence or an explicit applicability/blocking reason.

Remain in Build. Do not start another ComUI flow, call another ComUI skill or require a prior ComUI task. If the request belongs to a different flow, explain the mismatch and ask the user to choose before taking out-of-flow action. Natural-language requests are sufficient; prompt examples, a prior audit, a written plan and fixed report forms are optional.

| Need | Full local resource |
| --- | --- |
| Establish repo standards, source snapshot, scope and checks | [Repo profile](references/repo-profile.md) |
| Map UI blocks, state/consumers and evaluate reuse | [Component analysis](references/component-analysis.md) |
| Establish evidence, perform checks and report gaps | [Verification](references/verification.md) |
| Optionally capture a reusable profile | [Profile template](templates/repo-profile.md) |
| Optionally describe a component API | [Contract template](templates/component-contract.md) |

The optional templates do not select or launch a workflow. Follow the user's language and requested presentation while fulfilling all applicable steps of Build.
