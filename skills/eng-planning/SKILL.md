---
name: eng-planning
description: Research and shape a repository-grounded implementation plan. Use when requested or when material ambiguity, contracts, sequencing, or risk warrant a durable proposal. Planning does not authorize implementation.
---

# Planning

Produce a readable current implementation proposal, then stop at the planning boundary. Read `{{BASELINE_PATH}}` if its full text is absent from visible context (read it if unsure); it owns judgment, project selection, and authorization. Before writing, read `{{WORKFLOW_ROOT}}/writing/style.md` and its matching plan example if present. Reuse current context.

## Research before decomposition

Establish the evidence base internally: repository root, HEAD/revision and useful branch/ref, plus relevant staged, unstaged, and untracked work. Retain the inspected content or hashes needed to detect changes; unchanged HEAD or status alone does not establish unchanged local content. Note material issue/remote evidence and its revision/update marker when available. Do not put this bookkeeping ceremonially in the plan.

Establish the requested outcome and meaningful scope from the request, supplied issue, applicable repository guidance, and matching profile. Inspect current behavior, its owner, relevant callers, contracts/invariants, tests, and verification commands before proposing steps. Follow dependencies that can change the design, not the entire repository. Compare existing mechanisms' semantics, errors, and side effects before proposing reuse; precedent is evidence, not unquestionable authority.

Treat a user-proposed implementation approach as a candidate to validate against inspected behavior, ownership, contracts, current capabilities, and consequential tradeoffs unless the user explicitly made it a constraint. If evidence materially favors a plausible alternative, compare the consequences and recommend the better-supported direction before committing it to the plan; do not invent alternatives or challenge constraints merely for ceremony.

Use external research when the choice depends on current platform/library capabilities, deprecations, security, compatibility, unfamiliar technology, or a supported mechanism not established locally. Prefer primary sources applicable to the actual versions. Record only conclusions and links that affect the proposal; generic best-practice browsing is not a planning ritual.

Resolve routine choices from evidence. When alternatives materially change behavior, ownership, scope, data handling, security, or rollout, establish the constraint, compare viable consequences, and recommend a direction. Ask only for missing information or consequential decisions that inspection cannot resolve; continue independent research while waiting. Mark material uncertainty explicitly, never invent contracts or consumers. Do not decompose dependent work as settled while its decision remains open.

## Choose one active artifact and boundary

Resolve the intended work repository and actual active client mode. Use the user's explicit destination when the mode permits it. Otherwise, in supported native Copilot Plan mode use the current session's managed plan, resolving its actual location through session facilities rather than guessing a session ID. Outside native Plan mode, default to `<repository-root>/plan.md`. Setup owns neither artifact. Do not maintain a repository plan alongside a session plan for the same run.

Native Plan mode restricts project edits, including delegated subtasks; retain that enforced boundary when already active. It does not isolate draft reads or block every uncertain shell/external-tool operation. Keep the baseline's mutation restrictions, and use the validation reference's dispatch checks before giving general-purpose work to a helper. The personal skill does not itself switch modes or turn a planning-only request into plan-then-autopilot.

An explicit repository-local plan request remains valid, but may be blocked by native project-edit restrictions. Do not bypass them or select an implementation action merely to copy the plan. Continue in chat with persistence pending, or retain an already managed session plan as the sole active artifact and disclose the destination limit. Materialize the requested destination only when a supported artifact-only write/transfer is permitted; identify the resulting sole active source and retire the former session plan from use, without maintaining synchronized copies. This authorizes no application edits.

Inspect any existing destination and preserve unrelated plans and concurrent edits. Resolve an occupied unrelated path or unknown repository identity before writing. An in-chat proposal may continue, but do not claim persistence. Report the active surface/location and repository at handoff; keep code references repository-relative even in a session plan. Writing a plan does not stage, commit, or publish it.

## Derive the provisional approach

The parent owns the provisional direction. Before warranted independent solution discovery returns, keep proposed design, symbols, and rationale in parent planning context only: do not write them to the repository plan, native session plan, notes, or another worker-accessible draft. If an existing or automatically persisted draft is accessible, follow the validation reference's isolation fallback before claiming independence. Shape the proposal below privately; persist it only after validation, closure, and evidence refresh.

Use the smallest structure that supports execution. Usually this means **Problem**, **Current system**, **Approach**, **Implementation plan**, and **Verification**, combining sections when clearer. Include **Open questions** only for unresolved material blockers or decisions that may change implementation; remove it when resolved. Add scope/constraint sections only when they prevent likely mistakes. No empty template sections.

Explain the outcome and boundary, the few current facts needed to understand it, and the chosen direction with rationale needed for correct implementation. Cite useful repository-relative paths and symbols; distinguish observed owners from proposed additions. Name responsibility when the exact file is not yet established. Avoid brittle line numbers unless the task depends on one.

Sequence implementation by real dependencies and responsibility boundaries.

For small or well-contained changes, use direct numbered steps. Do not invent phases merely for structure.

For substantial, cross-cutting, or multi-stage changes, prefer **2–5 named implementation phases** when phasing makes ownership, dependency order, or verification easier to understand. A phase represents a coherent implementation increment, not an arbitrary group of files or an equal-sized chunk of work.

Useful phase boundaries may include establishing a contract, implementing the owning behavior, migrating dependent callers, integrating a user-facing or external boundary, performing a required data transition, or completing integration verification. Use only boundaries justified by the actual change.

Keep top-level phases to five or fewer in normal planning. If a proposal appears to require more, first regroup closely related work under a smaller number of responsibility-oriented phases with concise substeps. Exceed five only when the system genuinely has more independent sequential boundaries and combining them would make the plan materially harder to implement or verify. Five is a planning complexity budget, not a correctness rule.

Do not mechanically divide work into backend, frontend, and tests unless those are the real dependency boundaries.

Each phase or direct step should convey its objective, owning areas or important symbols, concrete behavior, meaningful dependencies/order, and observable outcome. Include concise substeps only when they clarify a phase.

Use functional-first sequencing for meaningful features: normally place functional production phases before a final test/verification phase, within the existing phase budget. Concentrate affected test repair, mocks/fixtures/wiring updates, new behavioral/regression coverage, and focused/broader repository checks in that final phase once functionality is coherent enough to exercise. Do not distribute test maintenance across functional phases merely to keep an intermediate suite green. Earlier phases may name diagnostic checks that expose wrong assumptions, preserved-contract violations, or blocking integration failures; real production defects need correction when discovered. [Implementation](../eng-implementation/SKILL.md#functional-first-implementation) owns this distinction between diagnostic execution and deferred test maintenance.

Do not force a universal contract-first, backend-first, frontend-first, or test-first sequence. Follow the actual dependency graph of the change.

Inspect actual check commands and side effects; distinguish planned checks from results already observed and expose unavailable verification. Include meaningful failures/edges and final integration evidence without repeating every step's checks.

Keep local implementation details autonomous. Omit copied implementation code, inventories, artificial IDs, badges, generic advice, and unrequested estimates. No mandatory TDD, prototypes, or ADRs; worker use follows the validation depth below. Use one compact visual only when it clarifies a grounded relationship; label proposed flows, keep meaning readable without rendering, and avoid duplicating it in prose and tables.

## Validate the proposal

The first draft is a hypothesis. Technical coherence alone does not establish correct framing, requirements, or design. Validate according to the question that can change the answer, not diff size or estimated effort:

- **Tiny, obvious change:** internally sanity-check evidence, owner, scope, and verification. No subagent is required; closure stays implicit.
- **Meaningful or consequential planning:** repository falsification is required. Read [validation](references/validation.md) before the pass and use bounded `explore` questions selectively. Substantial work cannot hand off just because its first draft is coherent.
- **Consequential design commitment or framing risk:** seek an unanchored independent approach when there is a real ownership/design question: a new interface, abstraction, owner, state/source of truth, persistence, dependency, configuration/compatibility mechanism, contract/schema redesign, plausible competing owners, user-proposed architecture, or unfamiliar system with consequential assumptions. Apply the reference's safe-dispatch and draft-exclusion requirements; disclose an unavailable perspective instead of claiming equivalent validation.
- **Consequential conclusion susceptible to adversarial challenge:** use `rubber-duck` when complementary critique can materially change it, after repository falsification and any warranted independent discovery/comparison. Large mechanically determined migrations do not earn alternative architectures or every worker merely through size; small contract changes may earn deeper validation.

Search for natural owners and mechanisms even when the provisional approach never mentioned them. The reference owns requirement reality, earned machinery, existing/native mechanisms, variability in both directions, scenarios, consumer/transition effects, distinguishing verification, and functional-first dependency sequencing. Insignificant details need no formal accounting.

The parent owns the final proposal. Resolve disputed assumptions against inspected requirements/contracts; revise when evidence defeats them and ask only for consequential decisions evidence cannot settle. Worker output is hypothesis, not authority: no model voting, agent-count consensus, or numeric confidence. `rubber-duck` is a critic, never the sole validator.

## Close coverage and refresh evidence

Before calling a substantial/consequential plan ready, account for the material planning surface, not just decisions already investigated. Every requested behavior, evidenced requirement, and explicit constraint needs a plausible implementation owner/path and meaningful verification, or must remain explicitly unresolved. Check preserved contracts/invariants, consequential owners and new machinery, affected consumers, meaningful behavior partitions, data/side-effect/retry/rollout transitions, dependency order, and counterexamples that distinguish correct behavior. Do not emit a giant traceability matrix. An omitted material requirement or consumer blocks readiness even if every included step is sound.

Before final persistence and handoff, compare the affected evidence with the starting snapshot: relevant code and local edits, revision/ref, and material issue/remote facts when changes are detectable. If it changed, refresh affected contracts/files, invalidate the affected assumptions, and repeat only the validation and coverage closure that depend on them. Preserve concurrent work. An unchanged HEAD alone is insufficient; unavailable current evidence limits the readiness claim. Do not restart unrelated research or call known-stale reasoning current.

## Persist and converge in place

After validation, coverage closure, and evidence refresh, persist or update the one active plan. The artifact describes the **current proposal, never the history of planning**. On a meaningful revision, investigate its consequences and resolve material choices, then rewrite affected sections. Delete superseded assumptions, alternatives, tasks, phases, and answered questions. Recheck downstream dependencies, verification, scope, and diagrams. Read the whole file after the update and normalize it to one coherent proposal.

Do not append revisions, addenda, corrections, decision logs, or chronological rationale unless explicitly requested. Keep only rationale that prevents a wrong implementation. Ordinary discarded options stay out of the artifact; do not preserve them in an ADR. Validation creates no second plan artifact or report: keep explore transcripts, independent-plan comparisons, critique output, and validation chronology out of durable files. A separate architectural record needs independent durable value, repository conventions, and its own requested scope.

## Stop and hand off

After persistence or revision, read the whole active plan for final coherence: requirements, owner, scope, dependencies, behavior, and verification must describe the same current proposal. Revalidate material commitments affected by a revision; do not repeat unaffected passes for ceremony. Surface only real remaining risks or decisions, without an empty validation section or manufactured competing design.

Present the current plan with its location, material unresolved decisions, and readiness limits. A first draft is not agreement. Plan acceptance, “looks closer,” research requests, and phase edits do not authorize coding. A native action explicitly requesting implementation can supply that direction; approving prose or transferring the artifact cannot. Ask for or recognize explicit direction to implement; reuse authorization already given when it clearly covers implementation after planning. Without it, stop at the proposal.

Planning permits inspection, research, discussion, and local plan writes only. Do not incidentally edit production code, tests, prototypes, or configuration. Checks must respect this boundary and the baseline's approval rules. Planning grants no commit, publication, external-mutation, or destructive authority.

On authorized handoff, [implementation](../eng-implementation/SKILL.md) consumes the plan as evidence alongside current code. Routine details remain autonomous; consequential invalidation requires reconciling the affected assumption and updating this same plan before dependent implementation. Never create a competing specification.
