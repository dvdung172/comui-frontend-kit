# Establish the repo's standards

## Discover before prescribing

Read the instructions applicable to the target files, project documentation, package/build manifests, formatter/linter/typechecker configuration, test setup, CI and existing design-system components. Follow the host's instruction precedence. If `.codegraph/` exists at the repo root, use CodeGraph first to understand or locate code; use its available MCP tool or CLI. If no index exists, use normal search. Do not create an index as an incidental audit step.

Start from entrypoints and representative modules relevant to the task. Expand to callers, styles and tests that a conclusion depends on. A handful of examples establishes a hypothesis about a convention, not proof of repo-wide consistency. Note monorepo package boundaries and more-specific local rules.

## Classify each rule

| Kind | Evidence | How to use it |
| --- | --- | --- |
| Explicit instruction | Applicable project guidance, ADR or documented API contract | Apply within its authority and scope |
| Enforced configuration | Actual lint/typecheck/build/test rule | State what it enforces; inspect conflicts with written guidance |
| Inferred convention | Concrete implementations and call sites | Label as inferred; explain representativeness and exceptions |
| Kit recommendation | Contextual maintainability, accessibility, responsive or verification concern | Give a concrete benefit/risk; do not invent a repo requirement |

A running configuration can differ from an instruction that describes intended architecture. Record both rather than silently treating either as obsolete. Resolve a conflict from instruction scope, documented decisions and current user direction where possible. If it still changes a material decision, ask a focused question and continue unaffected analysis. Do not recommend a repo-wide rewrite merely to resolve a local ambiguity.

For example, a README encouraging universal cards and a current rule requiring stable public events do not prove a universal-card abstraction is safe. Inspect actual contracts and describe the tradeoff.

## Capture the useful profile

Optionally use [the profile template](../templates/repo-profile.md), or include the relevant context directly in the working notes or report. Capture only information another agent needs for this task:

- Root, source snapshot and inspected scope, including uncovered routes/packages.
- Stack, routing/layout structure, component/design-system entrypoints and generated/vendor boundaries.
- Standards with file/symbol locators, classification and scope.
- State/data ownership, API boundaries, relevant permissions and UI state conventions.
- Check commands that actually exist, their working directories, prerequisites and known side effects.
- Runtime/reference availability and conflicts or assumptions that affect the task.

Use file plus symbol as the durable locator; add current line numbers for review convenience. Record a revision or snapshot to avoid presenting stale line numbers as current. Do not read secrets to fill a profile. A missing check script is missing capability, not an invitation to invent a command or add tooling during an audit.

Profiles are task aids, not a mandatory onboarding ceremony. Reuse a current profile and refresh affected facts. Save a separate profile only when the task benefits from it; small audits can include these fields in the report.
