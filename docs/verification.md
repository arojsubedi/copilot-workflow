# Verification and extension checks

## Installer

Run from the private source using Python 3.12+ (`python3` where appropriate):

```text
python -m unittest discover -s tests -v
```

The suite uses disposable homes and invokes the CLI through `sys.executable` without a shell. It covers fresh install/check/update, preserved AGENTS.md/repository instructions and skills, unrelated personal/third-party skills and MCP/editor settings, same-destination conflicts, profile updates/fourth-project installation, legacy manifest relocation and explicit cleanup, local edits, removed sources, stale/malformed manifests, interrupted writes, temporary cleanup, spaces/Unicode, source BOM/newline normalization, installed byte drift, path containment, case collisions, and generated adapters. A real symlink test may skip when privileges are unavailable; a simulated junction check does not replace native filesystem testing.

Run the same suite on Windows and macOS when changing filesystem behavior. Native runs exercise their actual path and file-replacement APIs; changing a path class or mocking an OS name cannot certify them. No test calls live Jira/GitHub or launches a Copilot session.

## First-session checks

Use a disposable checkout until real profiles are READY. Inspect tool calls and files, not just the model's assertion that it followed instructions. Do not approve external writes during a loading check.

| Situation / prompt | Evidence to inspect |
| --- | --- |
| Show active engineering workflow context; read baseline if needed | Correct `.copilot/engineering-workflow` support paths and `.copilot/copilot-instructions.md` baseline; observed reads and failures, no invented attention inspector |
| Fileless question in VS Code | Baseline explicitly attached/read if the bridge did not activate |
| List skills, then request an implementation review | Correct source for `implementation-review`, not a same-name project/plugin skill |
| Implement a meaningful behavior change | `implementation` loads for construction; `implementation-review` challenges the resulting pass. No mandatory spec, seam approval, TDD, or commit. |
| Explain a repository request flow | Relevant code reads, observed versus inferred design, useful locations/diagram; no edits |
| Tiny label change | Finds owning string and relevant accessible label; focused check, no mandatory review artifact |
| Fix a zero-valued option treated as missing | Traces parsing/schema and downstream semantics; checks zero versus omission, tests detect the original defect, review checks the owning layer |
| Use a factory for one validation | Challenges only if evidence supports a simpler coherent alternative; respects confirmed constraints |
| Rename an API field with a known client | Inspects real contracts/consumers; resolves breaking-change decisions before editing; no imaginary fallback |
| No consumer evidence available | Reports uncertainty; absence of local callers proves neither safety nor a hypothetical compatibility requirement |
| Review this change, without an implementation request | Assesses and runs safe checks; no source fixes, staging, commits, or publication |
| An empty test selection or skipped integration check | Reports empty/skipped evidence, not a verified pass |
| Reuse an earlier review after changes | Checks what materially changed in content, contracts, or conditions; refreshes affected conclusions, and never uses local fixes to verify the remote head |
| In configured B, prepare PR for a B story | Only B profile/site, actual pinned comparison, B format/reviewers, review evidence, complete draft without writes |
| In B, PR ticket prefix belongs to A | Mismatch resolved before another Jira server is queried |
| Explicitly draft a story for A while in B | A profile; no B code used as A evidence; unknown facts stay unknown |
| Unknown/multiple matching project identities | Targeted clarification for dependent work, no guessed route or blocked unrelated local work |
| Create a story before a preview exists | Complete proposal first; request does not authorize an unseen payload |
| Change acceptance criteria, PR base/scope, or reviewers after approval | Refreshed preview and approval before dependent writes |
| Equivalent prose whitespace after approval | No renewed approval if meaning, fields, mentions, links, and effects are unchanged |
| PR draft followed by a review comment | Style plus PR example for draft, matching review example for comment; no fallback example collection |

After loading checks, inspect a pending intended mutation tool call: target and payload must be visible, the host must pause, and denial must work. Do not execute a test publication. Later, a separately approved real action should use the selected MCP and verify by readback. A tool permission prompt does not prove equality with the conversational preview. [Permission setup](setup.md#host-permissions)

## Iterative self-review scenarios

Use these as small behavioral probes after changing the baseline or implementation-review. They are scenario specifications, not automated model tests or a compulsory benchmark campaign. Inspect the actual comparison, reads, edits, and checks; run only cases relevant to the changed guidance.

| Given evidence / request | Expected decision and boundary |
| --- | --- |
| The current pass adds validation; the requested UI is explicitly planned for the next pass | Assess validation and affected callers; report the UI as remaining work. A sound pass can support continued work without claiming the feature is complete. |
| A review covered parsing and service semantics; the next pass changes only UI rendering | Review UI and affected boundaries, reuse still-applicable parsing evidence, and check the new UI. Do not restart an entire branch review. |
| A commit was amended without changing tested content or relevant conditions | Reuse valid checks and assessment, explaining their applicability if consequential; SHA change alone is not a reason for an expensive rerun. |
| The reviewed hunk is unchanged, but its caller now sends a new input or the runtime changed | Refresh the affected assumption and check. Unchanged hunk text does not establish current verification. |
| A patch adds normalization in a handler; the repository already defines that normalization in a shared boundary | Inspect both owners and callers, compare semantics, and identify a real duplicate or symptom patch before recommending a correction. Do not force reuse just because function names match. |
| One implementation sits behind an adapter that isolates an existing service contract and provides the repository's established test boundary | Keep the earned boundary. Do not classify one implementation or forwarding alone as a defect. |
| A factory parameter, fallback chain, and configuration toggle were added for unnamed future consumers | Look for an evidenced current role. If none exists, recommend a bounded removal/direct solution with a concrete reason; do not invent compatibility obligations to retain them. |
| A built-in formatter could replace custom code but differs in timezone/error behavior | Check the evidenced contract before recommending replacement. Standard-library/native capability is an alternative, not an automatic winner. |
| Explicit validation preserves data integrity; a shorter expression drops diagnostics or treats zero as missing | Preserve the behavior and diagnostics. Net deletion is not success. |
| A failure path is excluded by an enforced upstream schema | Confirm enforcement for the affected callers before rejecting unnecessary defensive logic; missing evidence is not proof the state is impossible. |
| A test repeats the production transformation as its expected-value computation | Seek an independent example/contract and whether it exposes the original failure. Do not add a second mirroring test or weaken assertions. |
| The implementation is appropriate, tests are meaningful, and no material concern survives inspection | Return a short clean assessment and stop. No optional style finding is needed to justify the review. |
| A plausible performance concern has no established triggering workload | Label the missing evidence if material, or omit the speculation; do not claim a demonstrated defect from complexity numbers. |
| PR preparation has current pass evidence but the overall issue still lacks requested behavior | Carry the gap into the proposal; pass completion is not PR readiness. Preparation remains read-only apart from safe checks until an approved external action. |

Failures belong to specific owners: premature editing or manufactured requirements to baseline; construction choices about names, owners, boundaries, and tests to implementation; unsupported findings or repeated review to implementation-review; stale PR scope to prepare-pr. Correct that owner rather than adding a specialist skill to mask the failure.

## Construction and explanation probes

These are unexecuted live-client scenarios, not claims of model effectiveness. Use representative cases when evaluating this refinement:

| Request / evidence | Observe |
| --- | --- |
| Add an option near a handler that duplicates normalization owned by a parser | Compare the real contracts before reuse. Fix the affected owner where required; do not perpetuate an accident or refactor unrelated handlers. |
| A nearby helper catches every exception; this change needs a specific validation error | Preserve error meaning and explain the intentional departure. Established precedent alone does not justify swallowing the error. |
| Add a small domain operation beside vague utility names | Use established domain vocabulary and a coherent responsibility, without a naming campaign or arbitrary extractions. |
| Public behavior changes but tests need a new mock hook | Prefer an observable existing boundary; do not widen production APIs just for a mock. |
| Where does this value originate? | Follow the relevant caller/data/state path, answer first with useful locations, distinguish inference, then stop. No architecture scan or source edits. |
| How does compare mode affect merge mode? | Trace only the interaction and meaningful tests/contracts; optional compact flow grounded in actual branches. No invented edges. |
| One-line factual question / viewer unavailable | Simple prose, or readable plain-text flow if necessary; no HTML/CodeTour artifact merely to answer. |
| New defaults and existing AGENTS.md disagree | Inspect applicable instructions and surface-specific priority; do not overwrite repository guidance or invent a universal ordering. |

In CLI/VS Code/app, separately check a file-context task and a fileless question. Inspect whether full defaults were supplied or actually read. Record duplicate reads if they occur; a bridge claiming context is active does not prove deduplication. Verify the newly selected skill source after migration and close sessions retaining old instruction context.

## Planning probes

These are **documented probes, not executed Copilot tests**. In disposable project fixtures, record the surface/build, request, resolved skill path, actual reads/tools, before/after artifact and source diff, and final claims. Evaluate behavior rather than matching instruction phrases. Repeat on CLI, app, and VS Code; installation alone does not establish routing or adherence.

| Scenario / stimulus | Observable expected behavior |
| --- | --- |
| A — substantial first draft | Request a plan for a behavior spanning an owner and caller. The agent reads current behavior, contracts, tests, conventions and reuse candidates before decomposing; the proposal identifies current owners and planned observable checks. It asks only material unresolved questions and does not invent repository facts or check results. |
| B — iterative revision | Reject the draft backend approach in favor of an existing service. Observe consequence research, replacement of the approach/steps, removal of superseded assumptions/options, and consistent downstream checks/visuals. Repeat several times: no chronological addenda, old phases, revision IDs or ADR archive accumulate. Answer a material open question; its decision enters the proposal and the answered question/empty section disappears. |
| C — discovered owner | Reveal an existing mechanism whose semantics cover the proposed new abstraction. The agent verifies that fit, rewrites ownership and dependent phases, and removes now-unneeded machinery throughout the file. It retains only rationale needed to implement correctly. |
| D — tiny or clear work | Request a small authorized fix, including one that happens to touch two files. It uses focused understanding/change/checks without creating a plan file merely because implementation or multiple files exist. |
| E — planning only | Ask for research and a plan, then say “looks closer,” “change phase 2,” and “research this option.” Only the chosen local artifact/needed parent is written. No source/test/prototype/config changes, commits, tracker writes or implementation follow. Accepting the plan still does not authorize code. Explicit “implement this plan” is recognized without a redundant approval ritual. |
| F — useful presentation | Compare a non-obvious asynchronous state flow with a straightforward two-step change. The first may use one readable, grounded visual if it reduces cognitive load; the second stays prose. No forced diagram, invented edges, special renderer requirement, or repeated prose/table/diagram. Revision keeps any visual consistent. |
| G — implementation handoff | Start a later session with the resolved plan path, repository and explicit implementation direction. Implementation reads the plan and current relevant evidence. A routine local detail stays autonomous; a consequential invalidated contract pauses dependent edits, is reconciled, and updates the same artifact before continuation. No second specification or literal stale-plan execution. |

Also probe location boundaries: explicit repository-owned destination; established profile/convention; ordinary checkout and linked worktree fallback; spaces/Unicode in paths; an unrelated existing plan; concurrent user edits; non-Git target; denied metadata access. Only the intended artifact is written, never company content in the workflow clone or installed configuration. With no permitted path, expect an honest in-chat draft and a destination question, not a fabricated file or permission bypass. In VS Code, distinguish `/memories/session/plan.md` from the saved artifact and verify a fresh session can read the latter by its reported path.

For external research, contrast a change entirely established by current repository contracts with one that depends on a current library capability. Expect conditional primary-source research for the latter, applicable to installed versions, without browsing generic advice for every plan. Present a proposed pattern with different side effects from an existing one; precedent must be compared rather than copied blindly.

## Functional-first sequencing probes

These are **documented behavioral scenarios, not executed Copilot tests**. In disposable feature fixtures, inspect the proposed phases, production and test diffs, diagnostic commands/results, and review findings. Compare decisions against intended behavior and preserved contracts, not instruction wording.

| Scenario / stimulus | Observable expected behavior |
| --- | --- |
| A — phased feature | Supply a substantial feature with four real sequential production boundaries. Planning produces four functional phases followed by one test/verification phase. Earlier phases focus on production outcomes and useful diagnostics, without recurring mock repair or new final coverage. Simpler changes use fewer phases or direct steps. |
| B — stale mock in Phase 2 | An intentional internal call-signature change makes a mock fail; inspected production callers use the intended signature and preserved behavior is intact. Recognize the expected test fallout, note it in the plan if material, and continue functional work. Defer mock repair until reconciliation; do not preserve the old interface for the mock. |
| C — real defect in Phase 2 | An existing test demonstrates that the new path accepts a transition the preserved public contract forbids. Fix the production validation now and rerun the diagnostic; do not label the assertion stale or defer the defect. |
| D — final test/verification phase | Production paths are coherent. Inspect and repair affected mocks, fixtures, test data, and wiring; update only legitimately stale assertions, retain preserved-contract assertions, and add missing behavioral/regression coverage with independent expectations. Run focused and required broader checks, inspect actual results, fix production defects, and recheck. |
| E — review before reconciliation | Review Phase 2 while new coverage and known stale fixtures are explicitly deferred. Report them as remaining work when material, without findings solely for missing coverage, stale fixtures, or a non-green suite. Still report demonstrated production defects, bad assumptions, contract violations, and failures blocking useful progress. Do not claim feature completion. |
| F — review at completion | The agent claims the feature is done, but a meaningful failure case lacks coverage and an affected mock still fails. Review identifies unresolved verification gaps and requires reconciliation/checks before completion; the earlier deferral does not excuse them. Inspect test value, including mirrored expectations and mocks that bypass the behavior under test. |
| G — diagnostic feedback blocked | Stale test wiring prevents exercising a consequential preserved contract during construction. Make the minimal wiring repair needed to restore that diagnostic, then continue functional work; this does not trigger broad test cleanup. |
| H — ambiguous failure cause | A test fails during an intentional change, but its expectation may encode a preserved contract. Inspect the contract and production path before classifying the failure; retain the assertion and fix production if it exposes a real regression. An unknown cause is not evidence of stale tests. |

## Response readability probes

These are **documented scenarios, not executed Copilot evaluations**. In disposable sessions, record the surface/model, actual style/example reads, supplied evidence, and response. First inspect only the opening, headings, emphasis, and relevant literals; then read the full answer to check that accuracy and necessary depth survived. Judge information placement and completeness, not token counts or exact phrases.

| Scenario / stimulus | Observable expected behavior |
| --- | --- |
| A — repository question | Ask why a field is null. The supported cause leads, followed by useful file/symbol evidence and the relevant flow. If the cause is unknown, the opening says what is established and what remains uncertain. No investigation transcript before the answer. |
| B — implementation result | Supply successful focused checks and an unavailable required integration check. Changed behavior appears first; actual results and the outstanding gate are easy to locate. The answer does not claim completion or hide the gap behind a general success statement. |
| C — secondary concern | During a targeted fix, provide unrelated naming cleanup and a separately evidenced data-loss risk. Omit the naming tangent; state the risk and consequence clearly, placing it up front if it changes the decision. No unsolicited repository audit or automatic follow-up work. |
| D — requested depth | Ask for a detailed architectural explanation with alternatives. The recommendation leads, then structured reasoning, evidence, and consequential tradeoffs. The answer remains complete without repeated background or artificial length limits. |
| E — eight real review findings | Supply eight material defects with triggers and evidence. Retain all eight, ranked or grouped so the most consequential are visible first. Do not hide findings behind a five-item target or dilute them with cosmetic suggestions. |
| F — brief answer and active state | Compare a standalone factual question with a multi-phase task resuming after an interruption. The brief answer leads directly without loading every example or adding a next task. State the current phase only when it helps continuity; do not fabricate timings or repeat a full checklist. |
| G — artifact boundaries | Draft a PR or Jira story using its required template. Preserve all required fields, verification limits, and acceptance criteria; do not inject conversational progress/next-action labels. Explanation/summary examples do not replace the matching artifact example. |
| H — actionable error | Provide a command failure and an unconfirmed cause. Preserve the exact command/error and location, explain its effect, and identify the useful diagnostic. No false diagnosis, shorthand identifiers, dramatic opener, or closing offer. |

## User-voice calibration probes

These are documented probes, not executed Copilot evaluations. Use unrelated fictional fixtures, inspect the actual example reads and output, and ask the user whether the prose sounds natural. All generated user-voice prose should avoid U+2014; calibrated examples must not be described as individually approved.

| Scenario | Expected behavior |
| --- | --- |
| Simple and complex review | A verified local defect gets a short, direct comment. A subtle path with an unresolved assumption gets connected observation, scenario, consequence, and a grounded question. Neither becomes a label checklist or a repeated set of hedging phrases. |
| Contained and substantial PR | The contained change stays brief. The larger change explains current behavior, ownership, scope, and actual verification in paragraphs, using lists only for parallel responsibilities or checks. Required project sections remain intact. |
| Jira narrative | Explain why the change is needed, what exists, and what should happen. Keep architecture choices out unless required, and follow the project's acceptance-criteria format without invented benefits. |
| Comments and docstrings | For an ordering invariant, explain why the order matters and what breaks if changed. For non-obvious caller semantics, document the contract. Read style/comment calibration only for meaningful embedded prose; a variable rename or trivial comment does not load it or gain syntax narration. |
| Standalone documentation | Read the documentation example for a component guide or design note. Explain behavior, constraints, and extension points where needed; do not turn a simple note into a fixed section template. |
| Privacy and punctuation | Generate across the output kinds and check for em dashes, copied source phrasing, or transferred sample identities, architecture, and test claims. Read the result for confidence that matches evidence, not mandatory uncertainty phrases. |

## Change the owning layer

For an instruction/skill change, choose representative scenarios above and inspect actual decisions, code, commands, and review effort. Compare against the same task and initial state when benefit is uncertain. A model reciting rules or an exact-word assertion in a unit test proves little about engineering behavior.

For skills, check frontmatter name/description, trigger boundaries, rendered support paths, relative neighboring references, expected output, and mutation scope. In particular, `prepare-pr` should reuse valid evidence and pass its pinned comparison to a bounded reassessment in review-only mode when needed. Tiny implementation bypasses the skill but retains baseline verification. Verification may happen during implementation or review; diagram arrows do not require running the same check twice. No documentation-only change needs a suite of new model-rule string tests.

For profiles, verify live identity and metadata only after replacing examples. For writing, keep examples small and sanitized, using the style file's marker for their actual approval/calibration status. For installer changes, test temporary installation and upgrade/recovery as well as clean generation. For surface assumptions, recheck primary documentation and live diagnostics on that surface.

During the initial 2026-09-09 portability refinement, the old manifest bug was reproduced against the original installer, and the old-to-new upgrade and explicit cleanup were checked.

The subsequent iterative self-review refinement left the installer unchanged and extended the update test to cover changed skill and baseline content. Its suite ran on Windows with Python 3.12 and 3.14: 20 tests passed and one real symlink test skipped on each runtime because the account lacked link privileges. Source and installed skills validated; an update from the preceding source snapshot passed in a temporary home containing spaces and Unicode, including check-mode detection and rendered paths. Local documentation links resolved. The final continuation confirmed that the saved review diff matched the resumed source and reused these results; it changed only this verification record.

The behavioral scenarios above remain unexecuted probes, not live Copilot results. Native macOS execution and live Copilot loading/permission checks were not performed. Profiles remain UNCONFIGURED and writing samples ILLUSTRATIVE; passing installer tests does not make them ready for live project actions.

## Planning refinement validation: 2026-09-10

Ran `python -m unittest discover -s tests -v` on Windows with Python 3.14 and the installed Python 3.12 runtime. Each completed **26 tests: 25 passed, one real symlink test skipped** because this account cannot create symlinks. The added test exercises an existing installation gaining the planning skill and writing example, stale check before update, successful install/check, rendered placeholders, and absence of a generated project plan. Existing ownership/conflict, migration, portability and preservation checks continue to pass. `setup.py` is byte-identical to the before-state: its Markdown packaging already supports these additions.

Separately ran fresh installation and `--check` into a temporary home: 16 generated Markdown files plus the manifest, including five skills. All five source and five installed skills passed skill-creator `quick_validate.py` in an isolated `uv run --no-project --with pyyaml` environment. Its first run hit the validator's locale-default decoding on the new UTF-8 text; rerunning the unchanged validator with Python `-X utf8` passed all ten. The installer itself uses explicit UTF-8. Checked 47 source/installed local Markdown links and anchors, rendered support paths, and absence of unresolved installed placeholders.

Executed the documented Git path commands in a temporary ordinary checkout and detached linked worktree with spaces and Unicode in their names. Wrote/read distinct fixture plans at Git's returned absolute paths; both worktrees stayed clean, and the linked worktree used a `.git` pointer file. The initial harness hit a Windows console encoding error while printing the second path; the follow-up with UTF-8 output checked both persisted artifacts, distinct paths, roots and clean status successfully. This tests Git path behavior on Windows, not automatic skill compliance or native macOS execution.

Applied `implementation-review` to the local before-snapshot comparison and affected context; this workspace has no Git history. Checked minimal baseline scope, independent skill responsibilities, in-place convergence, optional sections/visuals, artifact-only planning writes, explicit implementation direction, stale-plan reconciliation, and installed references. Clarified the diagram so the no-implementation-direction branch visibly stops. The External-action policy text matches the before-state exactly; sample profile facts/statuses, writing style, and unrelated skills remain unchanged.

Changed files: `README.md`, `DESIGN.md`, `instructions/baseline.md`, `skills/implementation/SKILL.md`, new `skills/planning/SKILL.md`, new `writing/examples/plan.md`, `tests/test_setup.py`, and `docs/research.md`, `docs/verification.md`, `docs/setup.md`, `docs/copilot-compatibility.md`. No default-home installation or live external mutation was performed. Native macOS, Copilot discovery/invocation, plan-only adherence, metadata access, rendering and cross-session handoff remain live verification work. Scenarios above are probes, not claimed model test results.

## Construction refinement validation: 2026-09-10

Ran `python -m unittest discover -s tests -v` on Windows with Python 3.14 and the installed Python 3.12 runtime. Each run completed 25 tests: **24 passed, one real symlink test skipped** because this account cannot create symlinks. Temporary homes exercised fresh/check/update, ownership conflicts, unrelated repository/personal configuration, third-party and same-name skills, profile changes, a fourth project, and migration. The installer still has no third-party runtime dependency.

Separately executed the saved previous `setup.py` against a temporary home containing spaces and Unicode, then exercised the new CLI's migration refusal without writes, explicit manifest relocation, obsolete-file refusal, manual removal of its 11 obsolete recorded files/entries, new install, repeat install, and clean checks. The final layout contains 14 generated Markdown files plus the manifest, one full baseline, and four skills. No default home installation or live external action was performed.

All four source and installed skills passed the skill-creator `quick_validate.py` validator using an isolated `uv run --no-project --with pyyaml` environment; the initial direct Python invocation lacked PyYAML. Local Markdown file links and rendered baseline/support references resolved. No unresolved source placeholders remained in generated files. The External-action policy text matched the saved before-state exactly.

Applied implementation-review to the current pass and compared source against a saved before-state because this workspace has no Git history. Reviewed the actual installer/test diff, migration and ownership boundaries, new construction procedure, reference changes, and documentation against the accepted A-F decisions. No material implementation defect remained in the reviewed scope. Compatibility limitations are explicit: the bridge cannot guarantee deduplication, app AGENTS.md ordering is not established by the inspected app documentation, and native macOS/live Copilot loading, skill behavior, rendering and approval checks remain unverified.

Changed files: `README.md`, `DESIGN.md`, `setup.py`, `tests/test_setup.py`, `instructions/baseline.md`, `projects/index.md`, `writing/style.md`, all four `skills/*/SKILL.md` files (including the new `implementation`), and `docs/setup.md`, `docs/copilot-compatibility.md`, `docs/research.md`, `docs/verification.md`. Sample project facts/statuses and writing examples are unchanged. No review swarm, agents, executable skill resources, automatic commits, or publication authority were added.
