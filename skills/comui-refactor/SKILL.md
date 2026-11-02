---
name: comui-refactor
description: Use when implementing a scoped frontend refactor or consolidating compatible UI duplication while preserving public behavior. Executes the full Refactor flow only; a prior audit or written plan is optional.
---

# ComUI Refactor

Fixed flow: **Refactor**. This package is the complete Refactor projection of `comui-frontend-kit`, including the shared stages and full operational references. It is generated from the canonical kit and works as a standalone installed folder.

Read the complete [shared contract](references/core.md) and [workflow](references/workflow.md) before working. Execute the shared rules, baseline, every numbered Refactor step and completion checks. Read the operational references when the workflow names them; their requirements are not replaced by this entrypoint. Account for every stage/step with evidence or an explicit applicability/blocking reason.

Remain in Refactor. Do not start another ComUI flow, call another ComUI skill or require a prior ComUI task. If the request belongs to a different flow, explain the mismatch and ask the user to choose before taking out-of-flow action. Natural-language requests are sufficient; prompt examples, a prior audit, a written plan and fixed report forms are optional.

| Need | Full local resource |
| --- | --- |
| Establish repo standards, source snapshot, scope and checks | [Repo profile](references/repo-profile.md) |
| Map UI blocks, state/consumers and evaluate reuse | [Component analysis](references/component-analysis.md) |
| Establish evidence, perform checks and report gaps | [Verification](references/verification.md) |
| Optionally capture a reusable profile | [Profile template](templates/repo-profile.md) |
| Optionally describe a component API | [Contract template](templates/component-contract.md) |

The optional templates do not select or launch a workflow. Follow the user's language and requested presentation while fulfilling all applicable steps of Refactor.
