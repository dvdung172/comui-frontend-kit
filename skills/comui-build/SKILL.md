---
name: comui-build
description: Use when implementing a frontend page, feature, or component using a repository's existing stack, design system, and reusable UI. Supports ordinary language requirements with optional design references.
---

# ComUI Build

Implement the requested frontend behavior using the target repo's standards and existing components. This skill is self-contained; starting a build requires no other ComUI skill, audit report or prompt template.

Use the request and conversation as the brief. Infer the active repo and find existing product context before asking for more information. Clarify only missing choices that materially affect behavior, architecture or scope. A screenshot, Figma file or filled specification is optional; state consequential design assumptions when working from text.

## Discover the relevant conventions

Read applicable repo instructions, current stack/configuration, design-system entrypoints and related pages. Respect generated-code boundaries and existing data/API conventions. If `.codegraph/` exists, use its available tool or CLI before code search; record any access failure and fall back to normal inspection without creating an index.

Record pre-existing changes and preserve them. Separate explicit repo requirements from enforced configuration, inferred patterns and your recommendations. Keep the existing framework, real assets and data contracts unless the requested feature calls for a change.

## Compose the feature

Identify the feature's semantic UI blocks, existing reusable implementations, state/data owners and relevant consumers. Cover the loading, empty, error, permission and interaction states that matter to the actual feature.

Choose boundaries by user responsibility and behavior. Compare public props/events, state lifecycle, stable structure, variants and total abstraction cost before sharing components. Similar visuals can still require distinct behavior; a local helper or existing primitive may be sufficient. Define a new component API only to the extent needed for its consumers.

Implement the smallest complete feature within the requested scope. Connect frontend behavior to actual repo data mechanisms; make any unavailable backend assumption explicit. Continue implementation when the user has already requested it, rather than stopping at an architectural proposal or asking for the same approval again.

## Verify the result

Discover the repo's real check commands and run those relevant to the change when available and authorized. For a shared component, inspect affected consumers and meaningful variants. Use focused regression checks for behavior-sensitive work rather than tests that mirror implementation details.

When runtime access is available, exercise the changed route, important states, interactions and relevant viewports. If a design reference is also available, compare equivalent viewport, data, state, theme, fonts and loaded assets. Describe feedback by element/selector, observed difference, source location and a reproducible scenario; repair the cause and recheck affected behavior.

Report changed files, resulting behavior, checks actually performed and remaining acceptance gaps. Keep source, runtime and visual-reference evidence distinct: a successful build alone does not establish visual fidelity or complete accessibility. Record checks as passed, failed, not run or unavailable. Complete independent work if an environmental prerequisite blocks a check, then identify that precise gap.

Finish when the requested behavior is implemented and supported by the available relevant evidence. Use the user's preferred language and output format. A brief handoff is enough for a small change; no prompt sample, fixed report form or separate contract document is required.
