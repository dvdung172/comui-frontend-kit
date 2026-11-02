# Shared ComUI contract

Use the target repo's standards and evidence to improve frontend structure and behavior. Each installed entrypoint is self-contained; no other ComUI skill or provider-specific tool is required.

Use the user's natural request and conversation as context. Infer available facts from the workspace and ask only about consequential missing choices. Prompt examples, a prior audit, a separate written plan and document templates are optional. Optional presentation does not make workflow steps optional.

The original entrypoint selects a flow from the request. A fixed-flow entrypoint executes only its named flow; if the request requires a different flow, explain the mismatch and ask the user to choose before taking out-of-flow action. Do not silently switch flows, invoke another ComUI skill or start the other flows as prerequisites. Component investigation within Build or Refactor is part of that flow; it does not require running the Audit workflow.

- An audit produces a report and plan; it does not implement the proposal. Existing implementation authorization remains valid within the selected Build/Refactor scope.
- Record source snapshot, reviewed scope and uncovered areas. Distinguish explicit/enforced rules, inferred conventions and kit recommendations.
- Similar UI creates reuse candidates. Evaluate responsibility, public behavior, state ownership and abstraction cost before merging.
- Separate source evidence, runtime observations and reference comparisons. State the checks actually performed and what remains unverified.

Read the complete selected workflow and follow the supporting references it names. The operational guidance in repo-profile, component-analysis and verification remains applicable in full; a short entrypoint is not a substitute for those references. Load optional templates only when they help communicate the result.

Scale the work and report to the requested scope while executing every applicable step. Embed relevant profile, component-contract and verification details in one report for small work. Follow the user's language and requested output form. Source-only review is useful; missing runtime or design references limit the claims that depend on them.
