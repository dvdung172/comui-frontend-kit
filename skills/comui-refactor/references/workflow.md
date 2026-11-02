# Workflow

## Shared execution rules

Read [core.md](core.md). Execute the shared stages and every numbered step of the selected flow. Fixed-flow skills keep that flow for the task; they do not start another ComUI flow or call another ComUI skill to fulfill a prerequisite. If the request belongs to another flow, explain the mismatch and ask the user to choose before taking out-of-flow action.

Honor the user's current scope and existing authorization. An audit authorizes a report, not source edits. Build/refactor requests authorize their specified implementation; continue without asking for the same approval again. Resolve small implementation choices using the repo's conventions. Ask only when missing information materially changes behavior, architecture or scope and cannot be found in the repo. Continue independent work while waiting.

Accept natural language and use the workspace/conversation to infer available context. Prompt examples, document templates and a prior audit are optional. Choose an output format suited to the user's request; preserve the necessary evidence even when a fixed form is not used.

A requested report can be returned in chat or saved to the agreed destination. Record pre-existing changes before implementation and preserve them. Local checks may create ordinary temporary output; assess a script before running it if its side effects are unclear. Installation, service startup and external data access follow the user's authorization and host tool permissions, not an implied requirement of this kit.

## Establish the baseline

Read [repo-profile.md](repo-profile.md). Establish the repo root, requested routes/components, source snapshot, applicable rules, available checks and available evidence. Use a revision plus dirty-file scope, or a dated file snapshot when Git is absent. Inspect related callers and shared styles where needed to support conclusions.

For a broad task, enumerate the areas to cover and note any sampling. For a narrow change, keep the map to the relevant dependency neighborhood. Evidence from an old profile is a pointer: recheck the sources affected by the current task.

## Refactor

1. Use an assigned plan when available; otherwise derive a scoped approach from the requested change and current source. Reconcile stale file names, contracts and changes. Establish the observable baseline before modifying behavior-sensitive code. A separate written plan is optional.
2. Record the routes, public exports, props/events, state transitions, permissions and visual behavior that must remain stable. Choose a focused regression check when risk warrants it.
3. Apply one coherent change at a time. Use [component-analysis.md](component-analysis.md) for extractions and [verification.md](verification.md) for affected consumers and variants.
4. If a discovered bug requires a behavior change beyond the task, describe it separately. Stay within scope rather than hiding the fix inside a structural refactor.
5. Report evidence about preserved contracts, any intentional authorized behavior change and unresolved verification. If the code changed after a check, recheck the affected scope.

## Completion and blocked checks

Account for `shared`, `baseline`, every numbered step as `<selected-flow>.<step-number>` and `completion`. Use the lower-case flow name in step IDs. Keep a concise coverage record in the chosen output form, with status and an evidence locator or reason for each stage/step. No prompt template or fixed report form is required.

Use `done` when the step's actions and decisions have been performed; `not applicable` only for a conditional action whose triggering condition is absent, with the reason; and `blocked` for required work that cannot be performed, naming the prerequisite and remaining action. Assess conditional actions explicitly rather than silently omitting them. Lack of time, missing effort or an inconvenient check does not make required work inapplicable. A check's result remains `passed`, `failed`, `not run` or `unavailable` as defined in [verification.md](verification.md).

All applicable workflow actions must be performed before claiming that flow complete. Required blocked work remains incomplete; finish independent in-flow work and report the gap rather than substituting another flow. A source-only audit report can be complete when available checks are performed and runtime/reference limitations are recorded; this does not mean UI behavior was verified. If the requested acceptance criteria require runtime or visual verification, missing that evidence remains an unmet criterion.

Within the selected flow, do not stop with a proposal when implementation was requested and can be completed. Do not escalate a source-only review into implementation. If an environmental limitation prevents a required check, complete independent work and state exactly what remains unverified.
