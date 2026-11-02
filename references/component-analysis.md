# Component analysis

## Map meaningful responsibilities

Create a compact map: route/entrypoint → semantic block → source component → state/data owner → relevant consumers. A block is a coherent user-facing responsibility such as navigation, a product summary or a form section. The visual block is a useful observation unit; code may contain nested components, shared primitives and hooks beneath it.

Use actual framework mechanisms: props/events/slots, children/context, composition functions, stores or equivalent. Follow existing boundaries and design-system conventions. For new UI, map required loading/empty/error, permission and interaction states where they matter. For existing UI, inspect the states it really implements before recommending a new contract.

## Evaluate candidate groups

Candidate evidence may include repeated markup, matching layouts, shared data shapes or duplicated changes. Check each candidate against:

| Dimension | Questions to answer from source or requirements |
| --- | --- |
| Purpose | Do the blocks serve the same user responsibility? |
| Public behavior | Are callbacks/events, navigation, validation, keyboard behavior and permission rules compatible? |
| State ownership | Who owns data, subscriptions, asynchronous work, side effects and cleanup? Would merging couple independent lifecycles? |
| Shared structure | Which DOM/layout parts are stable, and which differ for a reason? |
| Variation | Can differences be explicit data, slots or a small meaningful variant, without unrelated boolean flags? |
| Change coupling | Would changing one consumer unexpectedly affect another? |
| Cost | Does the common API reduce total complexity, including wrappers, conditional code, tests and migration? |

Similarity produces a candidate, not a merge decision. Possible outcomes are reuse an existing component, extract a shared component, share only a primitive/helper/token, keep separate or investigate further. Explain the selected outcome with actual consumers; do not require a fixed number of matching instances.

When extraction is justified, use [the component contract template](../templates/component-contract.md). Specify the shared responsibility, instance-specific fields, events, state owner, variants and migration path. Preserve public interfaces unless their change is explicitly part of the task. Do not migrate frameworks or replace existing assets with placeholders to follow upstream prompts.

## Review the connected implementation

Inspect responsibility boundaries, dependency direction, duplicated logic, state location, effects, styling scope and existing test seams. Investigate accessibility, responsive behavior and performance using concrete evidence. Examples of bounded source observations are an unlabeled icon button, a fixed width that may overflow, or repeated subscriptions without cleanup. State the observation separately from any runtime consequence that has not been reproduced.

Large files and duplicated markup can be clues; neither is automatically a bug. Avoid extraction based only on line count, maximizing reuse, reducing file size or applying a personal naming preference. A local reusable pattern may be the right choice even when another framework convention is popular.

## Prioritize useful work

Order recommendations by demonstrated impact, reach across consumers, regression risk and the effort needed to verify them. Explain priority in words. Distinguish an observed defect from a standards violation and a maintainability opportunity. An accessibility defect affecting a primary action can outrank a large visual inconsistency; visual area alone does not set priority.

For each proposed step give the smallest coherent change, affected callers, contracts to preserve, expected benefit and check. Check shared-component changes against all affected variants/callers within scope, recording anything not covered. Connect observed element-level feedback to an identified element or selector, the source implementation and a reproducible scenario. Avoid vague instructions such as “make the page cleaner.”
