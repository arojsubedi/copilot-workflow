# Add an adaptive PR-review subsystem

## Problem

Add a user-level PR-review capability that can take a request such as `Review PR #123`, pin the exact repository and comparison, reconstruct the best-supported behavior contract, establish behavior before lower-value critique, scale review depth to the change, and return only findings that survive an evidence-based counter-check.

The review must be read-only with respect to the contributor's branch and external systems. It may retrieve evidence, run safe local checks, produce a private review report when the review is substantial, and draft comments. Posting a comment or review, approving, requesting changes, resolving threads, editing the PR, or changing Jira remains a separate preview and approval flow under `instructions/baseline.md`.

This plan is the temporary implementation artifact. `docs/pr-review.md` will become the concise current-state architecture document after implementation; it must not retain planning history.

## Current system

- `instructions/baseline.md` already owns repository/project selection, evidence distinctions, proportionate investigation, safe verification, writing triggers, and approval before external changes. PR review should consume these rules rather than restate a second global policy.
- `skills/implementation-review/SKILL.md` challenges an in-progress implementation pass and explicitly excludes full PR review. `skills/review-context/SKILL.md` reconstructs PR/Jira discussion without judging the whole change. `skills/prepare-pr/SKILL.md` owns PR creation and reviewer requests. These boundaries are compatible with a separate PR-review skill and should remain intact.
- `writing/style.md` plus `writing/examples/review.md` already calibrate review-comment prose, and `writing/examples/summary.md` can calibrate a substantial report. They belong at the presentation boundary, not in finding discovery or specialist prompts.
- `setup.py:build_files` discovers all skill Markdown dynamically and installs it below `.copilot/skills/`. `inspect_installation`, the hash manifest, and shared preflight protect new, updated, stale, and locally modified installed files across install, `--check`, `--status`, and `--uninstall`. The manifest currently accepts skills and workflow data, but not `.copilot/agents/`; status also has no agent component.
- GitHub currently documents personal skills at `~/.copilot/skills/<name>/SKILL.md` and personal Copilot CLI custom agents at `~/.copilot/agents/*.agent.md`. Agent profiles require a description and can restrict tools; omitted tools grant all tools. [Agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills), [CLI configuration layout](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference), [custom-agent configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- Copilot CLI can run built-in or custom agents as subagents with separate context windows, can run independent work in parallel, and returns the subagent's final response to the parent. Its current built-ins include `explore`, `task`, `code-review`, `rubber-duck`, and `security-review`. The new workflow can use these capabilities selectively, but must still succeed when no subagent is useful or available. [CLI custom agents and built-ins](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents), [CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference), [subagent result boundary](https://docs.github.com/en/copilot/reference/hooks-reference#subagentstop--subagentstop)

## Approach

### Ownership and source layout

| File | Responsibility |
| --- | --- |
| `skills/pr-review/SKILL.md` | Own the end-to-end review: target pinning, evidence gathering, behavior reconstruction and gate, proportional depth, impact tracing, optional delegation, candidate falsification, severity, report generation, comment drafting, and the publication boundary. |
| `agents/review-correctness.agent.md` | Independently reconstruct consequential behavior and challenge correctness assumptions when a second context can materially test the main workflow's conclusion. Seek reachable counterexamples and return candidate findings rather than comments. |
| `agents/review-design-simplicity.agent.md` | Independently assess whether the implementation is a sound, proportionate engineering solution, with concrete consequences for unnecessary or misplaced machinery. It is not an architecture, lint, or style reviewer. |
| `agents/review-test-evidence.agent.md` | Reason from the evidenced behavior contract to what tests and other evidence actually establish, including material missing regression scenarios. It does not start from a submitted-test checklist. |
| `docs/pr-review.md` | Describe only the implemented current subsystem, including its compact ASCII lifecycle diagram, adaptive depth, behavior gate, impact tracing, selective reviewers, finding acceptance, output, and approval boundary. |
| `tests/review-quality-cases.md` | Hold the nine sanitized, non-deterministic review-quality cases and their evidence-oriented evaluation rubrics. This is evaluation input, not runtime guidance or a results log. |
| `setup.py` | Dynamically render/install source agents to `.copilot/agents/`, admit those owned paths in the manifest, and report agent installation status through the existing safe ownership machinery. |
| `tests/test_setup.py` | Cover agent discovery, install/update/check/status/stale cleanup/conflict/uninstall behavior while preserving unrelated agents and other Copilot configuration. |
| `tests/test_content.py` | Validate skill and agent metadata, filenames, read-only tool declarations, rendered references, local documentation links, and content invariants without hardcoding a reviewer count. |
| `README.md`, `DESIGN.md` | Mention PR review in the overall workflow and link to `docs/pr-review.md`, without duplicating its internals or maintaining an agent inventory. |
| `docs/setup.md`, `docs/technical-details.md` | Explain the new installed agent layout, dynamic discovery/status, ownership behavior, private report location, client discovery limits, and smoke checks. |

No change is needed to `instructions/baseline.md`, project profiles, existing skills, or writing guidance. The main workflow reuses baseline judgment and project selection, optionally uses `review-context` for material discussion history, and reads the existing review/summary writing calibration only at presentation. It does not invoke `implementation-review`, planning, implementation, Jira-story, or PR-preparation skills as substitutes for PR review. Do not add technology-specific reviewers or a separate integration reviewer; impact analysis remains a main-workflow responsibility.

### Main review lifecycle

`skills/pr-review/SKILL.md` should encode the following responsibilities in this order. Every review completes target pinning, behavior reconstruction and gate, a lightweight impact scan, proportional verification, and the stopping decision. Deeper reviews expand behavior modeling and impact tracing and may add independent perspectives. Every candidate still passes through the same evidence, anchor, consequence, and counter-check contract regardless of review depth.

1. **Pin the review target.** Apply baseline project selection using the actual Git root/remotes and the generated project index, then read only the selected profile. Inspect the configured GitHub MCP's current schemas and retrieve the PR identity, repository, base ref/SHA, head ref/SHA, metadata, changed files, and complete relevant diff. Distinguish the pinned remote comparison from local HEAD, staged, unstaged, and untracked content. Use local files or checks only when they correspond to the pinned commits; otherwise retrieve exact remote content or state the comparison gap. Never silently mix a stale checkout with the live PR.
2. **Understand the change and reconstruct expected behavior.** Maintain a compact evidence ledger that distinguishes explicit requested behavior, PR/Jira/discussion claims, evidenced repository obligations, observed behavior, inference, and unresolved ambiguity. Start with the PR and repository evidence needed to understand the diff. Invoke or reuse `review-context` only when Jira, later discussion, review history, or resolution state can materially clarify intent or prevent a duplicate finding. A discussion claim remains a claim until independently established, and conflicting sources stay visible rather than being silently ranked as truth.
3. **Apply the behavior gate.** State the relevant behavior proposition and record one internal outcome before investing in design polish or broad optional review:
   - `PASS`: inspected evidence sufficiently establishes the intended change or the relevant behavior-preserving equivalence.
   - `FAIL`: a reachable defect or regression establishes incorrect behavior. Create one or more Blocking candidate findings and continue only far enough to establish scope or other material correctness failures; do not let polish obscure them.
   - `UNRESOLVED`: a material premise cannot be established from available requirements, code, tests, runtime, or external evidence. Useful static review may continue, but the result must not say behavior was verified.
4. **Choose proportional depth and trace impact.** Every meaningful review asks what responsibility or contract changed, who consumes it, and what outside the diff could defeat isolation. A focused review is complete when behavior is sufficiently established, a lightweight neighboring-convention/consumer search finds no material expansion path, focused verification supports the conclusion, and no risk signal warrants more work. Deepen when evidence shows a broad or externally consumed contract, migration/schema change, CI/deployment orchestration, nontrivial state space, high-consequence boundary, substantial or cross-cutting design, weak/central tests, conflicting intent, or uncertainty that more inspection can resolve. Diff size is a signal, not a routing rule.
5. **Model behavior only when the state space earns it.** Use a decision table, truth table, transition model, partitions, or targeted counterexamples for enums, optional/absent/null values, permissions, boundaries, historical/latest-state semantics, or interacting states. Do not require matrices for simple changes.
6. **Use independent work selectively.** The main workflow always owns behavior reconstruction, the behavior gate, correctness judgment, impact conclusions, candidate validation, severity, final acceptance, and synthesis. It may use `explore` for a bounded dependency trace, `task` for an appropriate existing check, `review-correctness`, `review-design-simplicity`, or `review-test-evidence` when that isolated perspective can materially change the result, and `security-review` only when the change implicates a credible security boundary. Performance, concurrency, accessibility/UX, and operational/rollout analysis are likewise conditional concerns, not permanent agents or mandatory checklist passes. Treat the initial behavior gate as the current evidence assessment: after an independent correctness result or other material evidence arrives, the parent must re-evaluate and, when warranted, change the gate before final output. Do not invoke `code-review` as a mandatory duplicate of the owning workflow. Run independent investigations in parallel only when their questions are independent and they share a pinned target and neutral evidence packet; do not require `/fleet`, three reviewers, or any fixed reviewer count.
7. **Validate candidates and synthesize.** Treat every candidate, including subagent output, as a hypothesis. Try to establish that another layer handles the case, the path is unreachable, the assumed contract is unevidenced, framework/library semantics differ, later code addresses it, compatibility behavior is intentional, or the proposed alternative violates another constraint; use a focused test/search/probe where applicable. For a proposed Blocking finding, or a cross-cutting/consequential finding that depends on nontrivial inference, use an independent challenger when another isolated investigation can materially test the conclusion. Prefer the current `rubber-duck` built-in or a different applicable specialist and ask it to seek counter-evidence, not agreement. This is not mandatory two-agent review, majority voting, or a confidence score: direct evidence can settle a finding without delegation, and disagreement must be resolved against evidence by the parent. If the needed premise remains unresolved, keep the candidate Conditional rather than promoting it through consensus. Do not add a permanent judge agent for this role. Deduplicate only genuinely identical issues. Reject defeated or preference-only candidates; never suppress an independent accepted finding because of report length.
8. **Present and stop.** Classify accepted findings by impact, generate proportional output, and stop when further inspection is unlikely to reveal another affected contract or change the conclusion. Convert an accepted engineering finding into human-facing comment prose only after reading the existing writing style and review example. For a substantial report, also use the summary calibration. Do not expose raw reasoning, subagent transcripts, rejected candidates, copied issue text, or a process diary.

### Impact and stopping rules

Impact traversal should follow responsibilities and contracts, not file extensions:

- A local metadata/config edit normally stops after the changed value, equivalent neighbors/local convention, and an obvious consumer constraint where relevant.
- A local logic rewrite compares old/new semantics, relevant callers or state assumptions, and focused regression evidence.
- A data/schema change expands through migration, schema/model, queries and raw SQL, API, jobs/scripts, fixtures/tests, and evidenced deployment implications.
- A function/API contract change expands through its owner, callers/consumers, schema/error semantics, mocks/tests/jobs, and established external compatibility obligations.
- A CI/deployment change expands through shared orchestration, environment/artifact contracts, downstream jobs/services, and evidenced runtime/deployment effects.

Stop following a path when inspected ownership and references make another affected contract unlikely and additional traversal cannot reasonably change the current conclusion. Do not deepen because tools or reviewers exist. Do not invoke another reviewer unless its isolated perspective can materially change the result. Stop candidate validation when the concern is established, defeated, or genuinely conditional because a material premise cannot reasonably be resolved.

### Specialist handoff contract

Before delegating, the main workflow supplies the selected agent with the repository identity, PR number, pinned base/head SHAs, relevant changed files/diff or exact local correspondence, relevant requirement and repository evidence with its source distinctions, known ambiguities, a neutral bounded question, useful impact leads, and the finding contract. Do not assume a subagent inherits the parent skill, baseline, or conversational evidence.

Do not include the parent's gate result or desired conclusion in the handoff. `review-correctness` independently derives the supported behavior and attempts to break the implementation; it is not told that behavior is correct. `review-design-simplicity` receives an area to assess, not an expected design defect. `review-test-evidence` receives the behavior evidence and test surface, not a claim that tests are weak. The parent can narrow scope without anchoring the answer.

All three agent profiles should declare only portable read/search tools, have no edit, shell, or agent-delegation tools, and explicitly prohibit source/external mutation and polished review-comment writing. The main workflow owns safe command execution and may delegate a specifically bounded check to the `task` built-in under the same authorization, so the specialists cannot modify the worktree through a shell.

Because isolated agents cannot be assumed to inherit shared guidance, put a compact common discipline directly in each profile rather than adding another policy file or relying only on the handoff. Each profile must treat repository precedent as evidence rather than authority; avoid invented requirements, callers, consumers, and compatibility obligations; distinguish observed behavior, evidenced obligation, inference, and uncertainty; remember that code shows behavior but not necessarily intent; consider existing/native/framework mechanisms before new machinery when relevant; accept zero findings; use no finding quota; reject personal preference; seek counter-evidence; base severity on consequence rather than confidence; return technical records rather than polished prose; and prohibit external mutation/publication. The handoff then carries only target-specific evidence and scope.

Each specialist returns zero or more candidate records with:

- severity recommendation;
- primary changed-file line/range, or symbol if line data is unavailable;
- concise factual issue;
- expected/evidenced contract;
- inspected evidence and concrete consequence;
- supporting locations where relevant;
- counter-check performed or counter-evidence found;
- `VERIFIED`, `CONDITIONAL`, or `REJECTED` recommendation;
- material evidence gap, if any.

These are handoff fields, not a required JSON serialization. The parent independently rechecks every material candidate. Only `VERIFIED` findings normally enter Findings. A consequential `CONDITIONAL` concern is reported separately when its missing premise cannot reasonably be resolved; `REJECTED` candidates disappear.

### Severity and code anchors

- **Blocking:** established incorrect behavior, regression, broken contract, data loss/corruption, exploitable vulnerability, invalid migration, or materially unsafe rollout that makes the PR unsafe to merge as-is.
- **Important:** a material test-evidence, ownership/duplication, dependency, maintainability, operational, or integration issue that deserves explicit consideration before approval even if immediate behavior may work.
- **Suggestion:** an evidence-backed improvement with a concrete benefit while current behavior remains sound.

Severity never depends on model confidence, reviewer identity/agreement, or fix difficulty. All severities require evidence. A cross-file issue anchors the finding to the changed line that introduces it and lists consumers/contracts as supporting locations. If no truthful changed-line anchor exists, use a changed symbol or an explicitly review-level concern with concrete supporting locations; never fabricate an inline location.

### Partial-review semantics

- If the PR cannot be fetched or repository/base/head cannot be pinned, stop before claiming a PR review. A provisional comparison is allowed only when the exact target is independently established and its limitation is explicit.
- If linked Jira is missing/unavailable or PR discussion retrieval is incomplete, continue when repository/PR evidence still establishes the relevant contract. Mark the behavior gate unresolved or report a verification gap only when the missing evidence could materially change the conclusion.
- If the local checkout does not match the pinned target, use exact remote evidence or omit local/runtime claims. Do not run checks against mismatched code and attribute them to the PR.
- If tests, runtime, or current external documentation cannot be used, preserve useful static conclusions, downgrade the behavior gate or candidate state when that evidence is consequential, and name the material gap. A failed freshness lookup cannot establish that an API is deprecated.
- If a custom or built-in subagent fails or is unavailable, continue in the main workflow when it can cover the concern. Report reduced coverage only when that independent investigation was material; one unavailable optional reviewer does not make the entire review fail.

### Review output and persistence

A tiny/focused review returns concise chat output: all accepted findings, or a concrete no-material-findings statement naming the behavior/impact evidence inspected. State `FAIL` or `UNRESOLVED` explicitly; a straightforward `PASS` may be conveyed by the evidence sentence rather than a ceremonial report section. It does not create a report file unless the user asks for one.

A substantial review returns a structured report with the repository/PR and pinned SHAs, behavior-gate result and explanation, concise coverage, all accepted findings grouped by severity, conditional concerns only when present, and material verification gaps only when present. Coverage should name the behavior checked, affected contracts traced, design/tests concerns covered where warranted, checks/probes run, and consequential unavailable evidence. It is evidence of review scope, not a diary or generic praise.

Materialize that substantial report outside the work repository under `{{WORKFLOW_ROOT}}/reviews/<host>/<owner>/<repository>/pr-<number>-<head-sha>.md`. Validate target-derived path components and never write through links. This runtime report is deliberately outside `setup.py`'s manifest: setup owns installed configuration, while review output belongs to the user and survives uninstall. Do not overwrite an existing report with different bytes; return the current result in chat and surface the collision. If the private location is unavailable, preserve the complete report in chat and disclose that persistence failed. The pinned identity in both path and report prevents the file from masquerading as current project documentation.

Drafted review comments are derived only from accepted findings and remain separate from the engineering records. Publication always stops at an exact preview of repository, PR, operation, anchor, and complete comment/review payload. Only explicit approval authorizes the external write, after which the workflow reads back and verifies the result using the baseline rules.

## Implementation plan

### Phase 1: Establish the owning PR-review workflow

Create `skills/pr-review/SKILL.md` with narrow metadata that triggers full PR review, not implementation self-review or discussion catch-up. Encode the target-pinning, evidence reconstruction, mandatory behavior gate, focused/deeper decision, adaptive behavior modeling, lightweight impact scan, concern-based deepening, candidate falsification, severity, exact anchors, partial-review semantics, report persistence, comment boundary, and publication stop described above.

Reference `review-context` as an optional evidence provider rather than copying its discussion-reconstruction procedure or requiring it before code inspection. Reference the installed baseline/writing paths through existing render placeholders. Make the zero-subagent focused path explicit and complete before adding specialist support.

Observable outcome: a single main agent can conduct a dependable focused or substantial read-only review and explain any material evidence limitation without custom agents.

### Phase 2: Add the three selective independent reviewers

After the zero-subagent main workflow is coherent, create `agents/review-correctness.agent.md`, `agents/review-design-simplicity.agent.md`, and `agents/review-test-evidence.agent.md` with valid agent-profile frontmatter, narrow descriptions, the compact shared review discipline, and explicit read/search-only tool lists. Keep them technology-agnostic and style-independent.

The correctness reviewer earns an isolated context for consequential or nontrivial business logic, API contracts, multiple branches/states, enum or null/absent/value behavior, persistence and migrations, historical/latest-state queries, error/side-effect semantics, transitions, externally consumed contracts, and material regression risk. From neutral evidence it should independently derive the supported behavior, test reachability and preserved contracts, detect dead/no-op behavior or incomplete branches, and construct targeted counterexamples. It returns candidates without displacing the parent's behavior gate or final correctness judgment.

The design/simplicity reviewer earns an isolated context when added machinery or ownership is consequential. It should investigate responsibility, duplicate ownership/logic, unnecessary state or refs, interfaces/types/helpers/wrappers with no independent responsibility, existing interfaces or repository mechanisms that can responsibly own the behavior, equivalent standard-library/framework/platform/native capabilities, unnecessary dependencies, newly introduced deprecated or inappropriate APIs, unjustified abstractions, speculative configurability/extensibility, YAGNI/shrink/delete opportunities, dead/redundant/no-op machinery, unnecessary indirection, control-flow complexity, materially obscuring domain names, and repeated orchestration whose variation belongs in data/configuration. A candidate must identify a concrete synchronization, maintenance, correctness, dependency, or comprehension consequence, or a specific benefit from the evidenced replacement. "Could be cleaner," speculative patterns, and language-style preferences are not findings.

The test/evidence reviewer earns an isolated context when tests materially support consequential behavior or may leave a regression boundary unprotected. It should reason from the behavior contract toward the evidence suite: what existing tests actually prove; whether expectations are independently derived; meaningful partitions, boundaries, counterexamples, regressions, enum/state paths, null/absent/value combinations, and historical/latest-state cases; implementation-shaped or contrived data; mocks that hide the behavior; weak assertions; duplicated scenarios; meaningful versus ceremonial parameterization; useful neighboring patterns; and whether a claimed regression test would fail on the defect. It may raise a specific missing-test candidate when the scenario materially distinguishes the intended contract from a plausible alternate behavior. Lack of a test alone is not proof of incorrect implementation: consequential unprotected behavior may be Important, while useful nonessential evidence may be a Suggestion, and routine branch/line coverage demands are rejected.

All three agents return the shared candidate record and actively seek counter-evidence. The main skill decides whether any is warranted, supplies neutral pinned context, receives their final responses, independently falsifies candidates, and handles failures. A specialist may follow a bounded impact lead, but the parent retains the complete impact map and stopping decision. They broaden or challenge reasoning; they do not own impact analysis, the behavior gate, final findings, severity, output, or publication. No integration, judge, or technology-specific reviewer is added.

Observable outcome: substantial reviews can gain the particular isolated perspectives they earn, including an independent correctness challenge, while tiny or sufficiently established reviews still complete with zero subagents.

### Phase 3: Install and manage custom agents safely

Extend `setup.py:build_files` to discover direct `agents/*.agent.md` source files dynamically, render them with the same UTF-8/LF contract, and map them to `.copilot/agents/<filename>`. Extend cross-platform collision checks and `load_manifest`'s destination allowlist to cover only that managed agent subtree. Do not hardcode the reviewer filenames or count into installation logic.

Extend `status` to derive an agent definition count and component state from the expected files, alongside the existing dynamic skill status. Let the existing shared inspection/preflight drive adoption, update, `--check`, stale removal, conflicts, and uninstall so a changed installed agent blocks all mutation and unrelated agents remain untouched. Do not manage runtime files below `engineering-workflow/reviews/` in the manifest.

Update `docs/setup.md` and `docs/technical-details.md` with the source-to-destination mapping, agent status/discovery behavior, local conflict and uninstall semantics, report ownership distinction, and the need for a fresh client session. State that `.copilot/agents` is the documented personal Copilot CLI path; other surfaces must be verified in their own agent picker, and missing delegated-agent support falls back to the main skill rather than blocking review.

Observable outcome: install, update, check, status, and uninstall treat agent profiles with the same ownership guarantees as current skills while preserving user reports and unrelated configuration.

### Phase 4: Document and surface the completed subsystem

Create `docs/pr-review.md` as the sole detailed current-state architecture. Explain adaptive effort, the behavior gate, focused review, deepening triggers, responsibility-based impact tracing and stopping, selective correctness, design/simplicity, and test/evidence challenges, candidate falsification/acceptance, exact anchors, substantial report shape, private persistence, partial-review disclosure, and publication approval. Keep the portable ASCII lifecycle diagram's single "selective independent review work" branch rather than implying three agents run for every substantial PR. Exclude setup parser details, full agent prompts, historical alternatives, roadmap language, evaluation cases, and implementation chronology.

Make minimal `README.md` changes to list PR review as a capability and link the new document. Make minimal `DESIGN.md` changes to place PR review as a specialized task skill/subsystem and link to the document. Do not duplicate the architecture or maintain a reviewer inventory in either file.

Observable outcome: users can discover the capability from the top-level docs while future architecture changes remain localized to `docs/pr-review.md` and the owning skill/agents.

### Phase 5: Reconcile infrastructure tests and evaluate review quality

Update `tests/test_setup.py` after the functional installer path is coherent. Cover dynamic agent discovery without a fixed count, rendering and installed path, manifest entries, `--check`, status count/state, updates, stale unchanged-agent cleanup, missing stale targets, locally modified active/stale agent conflicts with no partial mutation, uninstall/reinstall, and preservation of unrelated `.copilot/agents` files and unmanifested review reports. Reuse existing generic ownership cases where they already prove a behavior instead of duplicating every permutation.

Extend `tests/test_content.py` to discover all source agent profiles, require portable `.agent.md` filenames and matching names/descriptions, validate the deliberately read-only tool lists, reject unresolved render placeholders, check relevant workflow-content invariants such as behavior-gate states and non-mandatory delegation, and continue validating all local Markdown links. Assertions should verify responsibilities and contracts, not copy whole prompts or require exactly three reviewers.

Create `tests/review-quality-cases.md` with one compact, sanitized evidence packet and rubric for each case below. Each case records the known material issue or clean expectation, evidence required, expected depth/delegation, relevant concern, required useful signals, and obvious false positives to avoid:

- **A, simple JSON/config change:** clean focused review; inspect the changed value, equivalent neighboring entries, and any obvious parser/consumer constraint; no agent required; do not invent distant consumers or demand broader cleanup.
- **B, behavior-preserving React logic rewrite:** clean focused equivalence/regression review; compare old/new truth conditions, state/prop boundaries, callers, and focused tests; stop when equivalence is established; do not turn syntax preference into a finding.
- **C, newly introduced deprecated library/config API:** design/freshness concern; require the actual dependency/config version and current authoritative documentation; deepen or use design/simplicity review when consequential; keep it conditional if freshness evidence is unavailable and do not flag unrelated legacy use.
- **D, passing but weak tests:** Important test/evidence issue; require both identification of misleading existing evidence and any missing high-value scenario exposed by the behavior contract. Compare independent inputs/outcomes and inspect duplicated fixtures, implementation-shaped data, contrived hardcoding, mocks, and assertions. The missing scenario must distinguish consequential intended behavior from a plausible alternate implementation; do not equate line coverage, parameter count, or local test style with quality.
- **E, removed database column with remaining consumers:** Blocking impact issue; trace migration through schema/model, queries/CRUD/raw SQL, API, jobs/scripts, and relevant fixtures/deployment evidence; report concrete surviving references and avoid generic migration speculation. When the cross-cutting Blocking conclusion depends on nontrivial contract inference, exercise an independent correctness or challenger pass before acceptance without treating agreement as proof.
- **F, incorrect historical/latest-state query:** Blocking correctness issue; use schema/order semantics, caller expectation, and a minimal multi-row counterexample proving that the query selects the wrong state. The test/evidence review must identify a regression scenario where older and latest rows have different values, because single-row true/false cases cannot distinguish `ANY historical` from `LATEST state`; do not accept a passing single-row suite as independent evidence.
- **G, enum/action validation with missing branch and null/absent confusion:** Blocking correctness issue; enumerate the evidenced action and message-ID partitions in a compact matrix and show the reachable failing combinations. The test/evidence review should identify a meaningful uncovered cell, such as an evidenced action with absent input, rather than requesting mechanical branch coverage; do not expand to states excluded by the interface contract.
- **H, unnecessary dependency:** Important design/simplicity issue only when an existing/native capability is evidenced to provide equivalent required semantics; inspect dependency/build/lock impact, the current owner, and replacement behavior. This case must exercise proportionate engineering reasoning, not generic "dependency bad" advice, preference, or line-count reduction.
- **I, duplicated Jenkins orchestration:** Important design/simplicity issue only when pipeline/shared-library/downstream evidence shows duplicate responsibility and a concrete synchronization, maintenance, or behavior consequence. Identify the better existing ownership boundary or data/configuration variation; do not raise a mechanical DRY finding for merely similar syntax.

Exercise each case in a fresh Copilot session against its supplied sanitized packet or disposable checkout. Judge whether the review selected the expected depth, established or honestly left the behavior gate unresolved, followed the required evidence path, avoided prohibited false positives and unnecessary agents, anchored every accepted finding, and retained all independently verified findings. The rubric may expect an independent perspective where it materially tests the result, but it must permit zero agents when the main workflow can establish the conclusion reliably and must not require deterministic agent invocation. Evaluate semantic signals, not exact wording, finding order, model confidence, or agent agreement.

## Verification

Run these checks after all functional phases and test reconciliation:

1. `python -m unittest discover -s tests -v`
2. Install into a temporary home, then exercise install, `--check`, `--status`, update, stale-agent cleanup, conflict refusal, `--uninstall`, and reinstall. Inspect the manifest and confirm unrelated agents plus private review reports survive.
3. Install normally in a disposable/test user context where possible, start a fresh Copilot CLI session, verify `pr-review` skill and the three named custom agents are discoverable, and invoke each specialist against a read-only fixture. On other intended clients, inspect their skill/agent views and record any delegation limitation without weakening the main-agent path. Installer tests must continue deriving the agent inventory dynamically rather than asserting a fixed count.
4. Run a focused clean case and confirm there is no report artifact or unnecessary subagent. Run a substantial case and confirm the private report path, pinned target, behavior-gate state, coverage, exact anchors, accepted findings, and material gaps match the chat result without changing the worktree.
5. Exercise all nine sanitized cases using their rubrics. Include at least one subagent failure/unavailability, missing Jira/discussion evidence, mismatched checkout, unavailable test/runtime, and unavailable freshness documentation across the cases or focused failure probes. Confirm partial work is disclosed proportionally and never presented as comprehensive.
6. Preview a drafted comment/review and confirm no GitHub/Jira mutation occurs before explicit approval. In an approved disposable target, publish only the shown payload and read it back to verify the existing baseline approval boundary end to end.

The automated suite proves source/installer/content contracts. Client smoke checks prove discovery and handoff on supported surfaces. The sanitized cases assess review behavior and false-positive control; none of these layers substitutes for the others.
