# Component contract — {{name}}

- Existing implementation / proposed location:
- Responsibility and consumers:
- Decision: reuse existing / extract / share primitive or helper / keep separate / investigate.
- Evidence for the decision:

## Shared structure and allowed differences

| Shared responsibility | Instance-specific data | Structural/behavioral differences | How represented |
| --- | --- | --- | --- |

## Public contract

| Prop / event / slot / children / equivalent | Type or shape | Owner / caller | Defaults and invariants | Compatibility |
| --- | --- | --- | --- | --- |

State, effects, asynchronous work and cleanup ownership:

Navigation, permission, keyboard/focus and accessibility semantics:

Relevant loading/empty/error and visual variants:

## Migration and proof

- Consumers/call sites and migration order:
- Behavior and interfaces that remain stable:
- Existing implementation to retain, or retire only when unused:
- Baseline observation/check:
- Regression and render checks for affected consumers:
- Unverified assumptions / reasons to keep separate:

Use only fields relevant to the component. Decision criteria live in [component-analysis.md](../references/component-analysis.md).
