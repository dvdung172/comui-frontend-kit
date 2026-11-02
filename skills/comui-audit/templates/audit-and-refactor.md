# Frontend audit — {{scope}}

## Scope and result

- Goal / mode:
- Repo and source snapshot:
- Inspected routes/files/symbols:
- Coverage gaps and sampling:
- Applicable standards and their sources:
- Runtime/reference availability:
- Summary of confirmed issues and proposed work:

Embed relevant [profile fields](repo-profile.md) here, or link a separate profile when needed.

## Findings

Repeat only for supported findings; zero findings is valid.

### {{ID}} — {{concrete issue}}

- **Category:** observed defect / confirmed standards violation / refactor opportunity / open question.
- **Location:** file + symbol + current lines when available; include relevant callers.
- **Evidence:** what was directly observed and its locator; label any inference and its missing check.
- **Rule/basis:** explicit instruction / enforced configuration / inferred convention / kit recommendation, with source and scope.
- **Impact and priority:** who or what is affected and why this comes before other work.
- **Proposal:** smallest useful change, or keep as-is with reason.
- **Affected contracts/consumers:** behavior, state, API and visual variants to preserve.
- **Verification:** a check that would establish the claim or preserved behavior; current status.
- **Tradeoff/risk:** migration cost, added complexity or remaining uncertainty.

## Reuse decisions

| Candidate blocks + source locators | Shared responsibility | Differences to preserve | Outcome + reason | Affected callers / contract |
| --- | --- | --- | --- | --- |

Add a [component contract](component-contract.md) only when the proposed API needs one.

## Ordered refactor plan

| Step | Change + files/symbols | Depends on | Benefit | Contracts preserved / migration | Verification | Risk |
| --- | --- | --- | --- | --- | --- | --- |

Record any separate behavior-changing bug fix outside the structural refactor scope.

## Checks actually performed

| Command/scenario | Source snapshot + environment/state | Status | Observed evidence | Limits / next action |
| --- | --- | --- | --- | --- |

Status definitions: [verification.md](../references/verification.md).

## Handoff

- Audit coverage completed / uncovered:
- Source modifications, if separately authorized:
- Unresolved decisions and unverified claims:
- Suggested next implementation step:
