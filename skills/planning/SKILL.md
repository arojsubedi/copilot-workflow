---
name: planning
description: Research and shape a repository-grounded implementation plan. Use when requested or when material ambiguity, contracts, sequencing, or risk warrant a durable proposal. Planning does not authorize implementation.
---

# Planning

Produce a readable current implementation proposal, then stop at the planning boundary. Read `{{BASELINE_PATH}}` if its full text is absent from visible context (read it if unsure); it owns judgment, project selection, and authorization. Before writing, read `{{WORKFLOW_ROOT}}/writing/style.md` and its matching plan example if present. Reuse current context.

## Research before decomposition

Establish the requested outcome and meaningful scope from the request, supplied issue, applicable repository guidance, and matching profile. Inspect current behavior, its owner, relevant callers, contracts/invariants, tests, and verification commands before proposing steps. Follow dependencies that can change the design, not the entire repository. Compare existing mechanisms' semantics, errors, and side effects before proposing reuse; precedent is evidence, not unquestionable authority.

Use external research when the choice depends on current platform/library capabilities, deprecations, security, compatibility, unfamiliar technology, or a supported mechanism not established locally. Prefer primary sources applicable to the actual versions. Record only conclusions and links that affect the proposal; generic best-practice browsing is not a planning ritual.

Resolve routine choices from evidence. When alternatives materially change behavior, ownership, scope, data handling, security, or rollout, establish the constraint, compare viable consequences, and recommend a direction. Ask only for missing information or consequential decisions that inspection cannot resolve; continue independent research while waiting. Mark material uncertainty explicitly, never invent contracts or consumers. Do not decompose dependent work as settled while its decision remains open.

## Choose one artifact

Use the user's explicit destination first. Otherwise resolve the intended work repository with `git rev-parse --show-toplevel` and use `<repository-root>/plan.md`. This is a first-class artifact in that repository; setup does not manage it.

Confirm the target before writing. Inspect an existing plan and reuse it only for the current effort. Preserve unrelated plans and concurrent edits; ask for another concrete destination when the path is occupied by unrelated work or the Git root cannot be resolved. An in-chat draft may continue, but do not claim it is persisted.

Keep references inside the plan repository-relative. Report its resolved path and repository at handoff. Writing the plan does not stage, commit, or publish it.

## Write the current proposal

Use the smallest structure that supports execution. Usually this means **Problem**, **Current system**, **Approach**, **Implementation plan**, and **Verification**, combining sections when clearer. Include **Open questions** only for unresolved material blockers or decisions that may change implementation; remove it when resolved. Add scope/constraint sections only when they prevent likely mistakes. No empty template sections.

Explain the outcome and boundary, the few current facts needed to understand it, and the chosen direction with rationale needed for correct implementation. Cite useful repository-relative paths and symbols; distinguish observed owners from proposed additions. Name responsibility when the exact file is not yet established. Avoid brittle line numbers unless the task depends on one.

Sequence implementation by real dependencies and responsibility boundaries.

For small or well-contained changes, use direct numbered steps. Do not invent phases merely for structure.

For substantial, cross-cutting, or multi-stage changes, prefer **2–5 named implementation phases** when phasing makes ownership, dependency order, or verification easier to understand. A phase represents a coherent implementation increment, not an arbitrary group of files or an equal-sized chunk of work.

Useful phase boundaries may include establishing a contract, implementing the owning behavior, migrating dependent callers, integrating a user-facing or external boundary, performing a required data transition, or completing integration verification. Use only boundaries justified by the actual change.

Keep top-level phases to five or fewer in normal planning. If a proposal appears to require more, first regroup closely related work under a smaller number of responsibility-oriented phases with concise substeps. Exceed five only when the system genuinely has more independent sequential boundaries and combining them would make the plan materially harder to implement or verify. Five is a planning complexity budget, not a correctness rule.

Do not mechanically divide work into backend, frontend, and tests unless those are the real dependency boundaries.

Each phase or direct step should convey its objective, owning areas or important symbols, concrete behavior, meaningful dependencies/order, and observable outcome. Include concise substeps only when they clarify a phase.

Use functional-first sequencing for meaningful features: normally place functional production phases before a final test/verification phase, within the existing phase budget. Concentrate affected test repair, mocks/fixtures/wiring updates, new behavioral/regression coverage, and focused/broader repository checks in that final phase once functionality is coherent enough to exercise. Do not distribute test maintenance across functional phases merely to keep an intermediate suite green. Earlier phases may name diagnostic checks that expose wrong assumptions, preserved-contract violations, or blocking integration failures; real production defects need correction when discovered. [Implementation](../implementation/SKILL.md#functional-first-implementation) owns this distinction between diagnostic execution and deferred test maintenance.

Do not force a universal contract-first, backend-first, frontend-first, or test-first sequence. Follow the actual dependency graph of the change.

Inspect actual check commands and side effects; distinguish planned checks from results already observed and expose unavailable verification. Include meaningful failures/edges and final integration evidence without repeating every step's checks.

Keep local implementation details autonomous. Omit copied implementation code, inventories, artificial IDs, badges, generic advice, and unrequested estimates. No mandatory TDD, prototypes, subagents, or ADRs. Use one compact visual only when it clarifies a grounded relationship; label proposed flows, keep meaning readable without rendering, and avoid duplicating it in prose and tables.

## Converge in place

The artifact describes the **current proposal, never the history of planning**. On a meaningful revision, investigate its consequences and resolve material choices, then rewrite affected sections. Delete superseded assumptions, alternatives, tasks, phases, and answered questions. Recheck downstream dependencies, verification, scope, and diagrams. Read the whole file after the update and normalize it to one coherent proposal.

Do not append revisions, addenda, corrections, decision logs, or chronological rationale unless explicitly requested. Keep only rationale that prevents a wrong implementation. Ordinary discarded options stay out of the artifact; do not preserve them in an ADR. A separate architectural record needs independent durable value, repository conventions, and its own requested scope.

## Stop and hand off

Present the current plan with its location, material unresolved decisions, and readiness limits. A first draft is not agreement. Plan acceptance, “looks closer,” research requests, and phase edits do not authorize coding. Ask for or recognize explicit direction to implement; reuse authorization already given when it clearly covers implementation after planning. Without it, stop at the proposal.

Planning permits inspection, research, discussion, and local plan writes only. Do not incidentally edit production code, tests, prototypes, or configuration. Checks must respect this boundary and the baseline's approval rules. Planning grants no commit, publication, external-mutation, or destructive authority.

On authorized handoff, [implementation](../implementation/SKILL.md) consumes the plan as evidence alongside current code. Routine details remain autonomous; consequential invalidation requires reconciling the affected assumption and updating this same plan before dependent implementation. Never create a competing specification.
