---
name: comui-refactor
description: Use when implementing a scoped frontend refactor, consolidating compatible UI duplication, or changing component boundaries while preserving public behavior and repository conventions. A prior audit or formal plan is optional.
---

# ComUI Refactor

Perform the requested frontend refactor and verify the affected public contracts. This skill is self-contained; the user can describe the change naturally without first running another skill or filling a plan template.

Use an assigned plan when one exists; otherwise derive the smallest coherent change from the request and source. Locate context in the current repo and conversation. Ask only about missing choices that materially change behavior, architecture or scope. A request for assessment alone remains an audit; use implementation authorization already present in the conversation.

## Establish what must stay stable

Read applicable repo instructions, relevant configuration, implementations and callers. If the repo has `.codegraph/`, use its available tool or CLI before code search; if it fails, state the limitation and use normal inspection. Keep indexing outside this refactor unless requested.

Record the source revision and pre-existing changes; preserve unrelated work. Reconcile any plan with current source. Distinguish explicit/enforced repo rules, inferred conventions and your recommendations rather than imposing another project's architecture.

Identify affected exports, props/events, routes, state transitions, data/API contracts, permissions, keyboard/focus behavior and meaningful visual variants. Establish an observable baseline for behavior-sensitive contracts using existing tests or a focused scenario. Missing runtime access limits the resulting claim, not the ability to inspect source.

## Refactor around responsibilities

Map the relevant UI blocks to components, state/data owners and consumers. For each proposed extraction, compare responsibility, public behavior, lifecycle, stable structure, meaningful variants and total cost including wrappers, conditionals, migration and tests. Share an existing primitive/helper or keep implementations separate when a larger abstraction would couple unrelated behavior.

Apply one coherent scoped change at a time. Preserve public interfaces unless their change is expressly part of the request, and inspect affected callers/variants. Retain repo conventions and real assets. A formal component contract or written migration plan is optional when the change can be communicated clearly in the implementation and handoff.

Describe an unrelated discovered bug separately from structural cleanup. A behavior-changing fix outside the granted scope needs its own decision; it should not enter unnoticed through an extraction. Resolve routine implementation choices using the repo's conventions and continue authorized work without another approval loop.

## Verify preserved behavior

Run relevant existing repo checks when authorized and available. Use a focused regression check for meaningful risks; its expected outcome should describe the public contract rather than duplicate the new internals. Compare baseline and changed behavior for affected consumers, including permission and loading/empty/error states where relevant.

Exercise runtime scenarios and viewports when access exists. Compare visuals only when comparable renders and a reference/baseline are available. Keep source evidence, runtime evidence and visual comparisons separate; never equate fewer lines or a green build with preserved UI behavior. After further edits, recheck affected claims.

Report the implemented change, affected contracts, checks and remaining uncertainty in the user's preferred language and format. Mark each check passed, failed, not run or unavailable; identify pre-existing failures and any blocked prerequisite. Finish with the assigned change completed and evidence about preservation, rather than a proposal when implementation was requested. Templates and sample prompts are optional.
