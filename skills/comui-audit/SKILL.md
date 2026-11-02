---
name: comui-audit
description: Use when reviewing existing frontend source, assessing component reuse, or proposing a UI refactor against a repository's own standards. Produces findings and a plan without implementing source changes.
---

# ComUI Audit

Audit the requested frontend area using the repo's own standards and traceable evidence. This skill is self-contained; it needs no other ComUI skill, prior audit or prompt template.

Accept ordinary language. Infer the repo and scope from the current workspace and conversation. Locate available context before asking about a missing detail; ask only when the answer materially changes the review. Adapt the report to the user's language, requested format and task size.

## Establish the review boundary

Read applicable repo instructions, relevant configuration and representative implementations. If the repo has `.codegraph/`, use its available CodeGraph tool or CLI before searching code; if unavailable, record the limitation and use normal inspection. Creating an index is outside an ordinary audit.

Record the source revision and relevant dirty files, or a dated snapshot when Git is absent. Identify reviewed routes/components, relevant callers and coverage gaps. Distinguish explicit instructions, enforced configuration, inferred conventions and your recommendations. Resolve conflicts using instruction scope and current user direction; an observed pattern alone does not establish a repo-wide standard.

## Investigate components and behavior

Map the relevant entrypoints to semantic UI blocks, implementations, state/data owners and consumers. Expand the map only as needed to support a finding.

For a reuse candidate, compare responsibility, public API/events, state lifecycle, permissions, shared structure, meaningful variants and migration cost. Similar appearance or repeated markup is a starting point. Reuse an existing component, extract a focused component/helper, keep separate, or investigate further according to the actual contracts. A universal component with unrelated flags can cost more than duplication.

Follow relevant callers and tests before concluding. Classify supported findings as observed defects, confirmed standards violations, refactor opportunities or open questions. Explain who is affected and prioritize by impact, reach, regression risk and verification effort. Zero findings is a valid result.

## Deliver evidence and a usable next step

For each consequential finding, provide a file/symbol locator, observed evidence, applicable rule or rationale, impact, smallest useful change, affected contracts and a verification path. An ordered plan can be a few sentences for a small task; a fixed report template or separate document is optional.

Keep source observations, runtime observations and design comparisons distinct. Source can support a potential layout or accessibility issue; actual rendering, interactions and measured performance need the corresponding evidence. State runtime and design-reference availability separately. Missing browser access does not block useful source review.

Run relevant existing local checks when authorized and available; assess side effects first. Report checks as passed, failed, not run or unavailable with the evidence and remaining gap. An audit request authorizes a report and proposal; implementation needs a request to change source. Do not turn audit findings into unsolicited fixes.

Finish when the requested scope is reviewed or explicitly marked uncovered, important conclusions are traceable, and recommendations name the next useful check. Return the result in chat unless the user requests a saved report. Prompt samples and report forms are optional aids, never prerequisites.
