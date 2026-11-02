# Workflow

## Route the request

| Request | Mode | Completion |
| --- | --- | --- |
| Review, audit, assess or propose a refactor | Audit | Evidence-backed findings, scoped coverage and an actionable plan |
| Implement a new frontend feature, page or component | Build | Requested behavior implemented and relevant checks reported |
| Apply an assigned refactor or approved plan | Refactor | Scoped changes with evidence about preserved behavior |

Honor the user's current scope and existing authorization. An audit authorizes a report, not source edits. Build/refactor requests authorize their specified implementation; continue without asking for the same approval again. Resolve small implementation choices using the repo's conventions. Ask only when missing information materially changes behavior, architecture or scope and cannot be found in the repo. Continue independent work while waiting.

A requested report can be returned in chat or saved to the agreed destination. Record pre-existing changes before implementation and preserve them. Local checks may create ordinary temporary output; assess a script before running it if its side effects are unclear. Installation, service startup and external data access follow the user's authorization and host tool permissions, not an implied requirement of this kit.

## Establish the baseline

Read [repo-profile.md](repo-profile.md). Establish the repo root, requested routes/components, source snapshot, applicable rules, available checks and available evidence. Use a revision plus dirty-file scope, or a dated file snapshot when Git is absent. Inspect related callers and shared styles where needed to support conclusions.

For a broad task, enumerate the areas to cover and note any sampling. For a narrow change, keep the map to the relevant dependency neighborhood. Evidence from an old profile is a pointer: recheck the sources affected by the current task.

## Audit

1. Map routes/entrypoints to semantic blocks, implementations, shared primitives, state owners and data dependencies. Read [component-analysis.md](component-analysis.md).
2. Investigate concrete issues and candidate component groups. Follow call sites and relevant variants before judging an abstraction. Separate confirmed defects, confirmed standards violations, refactor opportunities and open questions.
3. Prioritize using observed impact and scope. State how the issue affects a user, a caller or future changes; keep preference-only suggestions optional.
4. Propose small ordered changes with contracts to preserve, affected consumers and a verification path. Include a keep-as-is option when abstraction adds more complexity than it removes.
5. Use [verification.md](verification.md) for checks supported by the available environment. Report what was observed and what still needs validation.

Use [the audit template](../templates/audit-and-refactor.md). Embed [profile](../templates/repo-profile.md) and [component contract](../templates/component-contract.md) details only as needed. There is no finding quota and no requirement to create separate documents for small jobs.

An audit is complete when its agreed scope is reviewed or explicitly marked uncovered, important conclusions have traceable evidence, and recommendations have verification steps. Completion of a report does not mean runtime behavior was verified.

## Build

1. Establish the requested behavior, UI states and acceptance criteria. Locate existing components, design tokens and conventions before creating new ones. Text-only requirements are sufficient to start; state design assumptions and ask only about consequential gaps.
2. Use [component-analysis.md](component-analysis.md) to map semantic blocks, choose existing implementations and define genuinely new contracts. Screenshots support decomposition; they do not determine the entire component API.
3. Implement the smallest complete feature within the current stack. Compose reusable components and page layout, preserving real assets and data contracts. Keep backend assumptions explicit at frontend boundaries.
4. Verify relevant behavior, states, consumers and rendering using [verification.md](verification.md). Repair specific observed failures and recheck affected areas.

Deliver changed files, resulting behavior, checks actually performed and remaining limitations. Do not describe an unexecuted check as passed.

## Refactor

1. Read the assigned plan and current source; reconcile stale file names, contracts and changes. Establish the observable baseline before modifying behavior-sensitive code.
2. Record the routes, public exports, props/events, state transitions, permissions and visual behavior that must remain stable. Choose a focused regression check when risk warrants it.
3. Apply one coherent change at a time. Use [component-analysis.md](component-analysis.md) for extractions and [verification.md](verification.md) for affected consumers and variants.
4. If a discovered bug requires a behavior change beyond the task, describe it separately. Stay within scope rather than hiding the fix inside a structural refactor.
5. Report evidence about preserved contracts, any intentional authorized behavior change and unresolved verification. If the code changed after a check, recheck the affected scope.

Do not stop with a proposal when implementation was requested and can be completed. Do not escalate a source-only review into implementation. If an environmental limitation prevents a required check, complete independent work and state exactly what remains unverified.
