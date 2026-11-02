# Evidence and verification

## Match claims to available evidence

| Evidence | Supports | Still requires additional evidence |
| --- | --- | --- |
| Source and configuration | Observed structure, code paths, public contracts, explicit standards | Actual rendering, complete interactions, measured performance |
| Running application | The routes, states, data and viewports actually exercised | Unvisited states, exhaustive accessibility or every browser |
| Design/reference plus comparable render | Specific visual differences at the same route/state/viewport | Other breakpoints and unspecified design behavior |

Record runtime access and reference access separately. A design screenshot without a running app cannot verify the app's current rendering. A running app without a design reference can verify behavior and observed layout, but not faithful reproduction of an unknown design.

For text-only builds, use agreed behavior, repo conventions and explicit design assumptions as acceptance criteria. For source-only audits, state limitations and identify the smallest next check for each consequential uncertain claim. Avoid blocking source analysis merely because a browser or design file is unavailable.

## Use checks that answer the change

Discover actual commands and prerequisites through [repo profiling](repo-profile.md). Run the relevant existing lint/typecheck/build/tests when authorized and available; record a pre-existing failure before attributing it to the change. Static checks do not prove visual or interaction correctness.

For behavior-sensitive refactors, compare an observable baseline with the changed implementation. Prefer a focused regression check that exercises the affected public contract, caller or state transition. Keep its oracle independent of the new implementation; a test that simply mirrors new internals is weak evidence. Pure renames or low-impact documentation changes do not require new tests by default.

For shared UI, cover the affected consumers and meaningful variants, including loading/empty/error and permission states when relevant. Use the repo's target breakpoints; record sampled viewports and uncovered ones rather than claiming every device was checked.

When reference images are available, compare consistent viewport, data, state, theme, fonts and asset-loading conditions. Describe a visual issue with the target element/selector, expected versus observed result and source location. Use measured values only when actually measured. Prefer a concrete root-cause repair in layout or styling over arbitrary pixel adjustments that damage other states.

## Record each result

Use `passed`, `failed`, `not run` or `unavailable` for checks:

- Command or manual scenario, working directory, source snapshot and prerequisites.
- Relevant route/state/viewport and reference identity, if used.
- Observed result, concise evidence locator and limitations.
- Whether the failure existed at baseline and the next action for any gap.

`Not run` means the check was not executed; `unavailable` identifies a missing capability or prerequisite. Neither means failure of the product nor success of the check. Inferences should name their supporting source and the experiment needed to confirm them; do not assign invented confidence percentages.

After further edits, prior evidence remains valid only for unaffected scope. Recheck the affected contract or scenario and report the source snapshot actually verified. Preserve user changes and distinguish implementation completion from verification completion. A report may be complete with runtime unverified; an implemented patch with missing required checks must be labeled accordingly.

## Stop refinement for a reason

Finish when the task's acceptance criteria are met with the available evidence. Fix and recheck concrete failures. If a required check is blocked, state the unmet criterion and prerequisite, complete independent work and hand over the remaining verification. Do not loop through speculative redesigns or use reuse rate, fewer lines, screenshot similarity or a green build alone as proof of successful refactoring.
