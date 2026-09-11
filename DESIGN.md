# Architecture

## Purpose and operating model

This private source supplies engineering defaults, five task skills, project profiles, and writing guidance for local Copilot sessions. Python installs ordinary files outside company repositories. Existing GitHub/Jira MCP connections supply live evidence and approved actions; the workflow stores no credentials or MCP configuration. Local context storage does not imply offline inference or offline MCP calls.

The guiding decision is: what kind of change is this, how risky and uncertain is it, and what is the minimum process needed to do it well? The diagram below shows these choices, not file plumbing or a programmed state machine. Questions and drafts do not enter an implementation pipeline.

| Change | Expected depth |
| --- | --- |
| Tiny and clear | Understand, change, focused verification |
| Normal implementation | Ground and understand, short plan if useful, implement a meaningful pass, review, adjust and verify; continue as needed |
| Requested plan or materially ambiguous/risky change | Research and converge on a durable current proposal when warranted; proceed to implementation only when explicitly directed, then review, adjust and verify proportionately to risk |

These are judgment defaults. There is no fixed change budget, required planning artifact, reviewer persona, or requirement to produce findings. Additional critique is useful only for an observed concern; V1 does not orchestrate it.

| Engineering question | How the system answers it |
| --- | --- |
| Grounding: what does this system actually do? | Inspect current repository guidance, code, schemas, callers, tests, and relevant live evidence |
| Judgment: what does the request require? | Separate intent and evidenced obligations from observation, inference, assumptions, and proposed means |
| Ownership: where does this behavior belong? | Trace the responsibility and inspect existing mechanisms before adding a second path |
| Risk: how much scrutiny is warranted? | Investigate uncertainty that can change the solution; keep routine decisions autonomous |
| Planning: what proposal can we currently support? | Research before decomposition, resolve material decisions, rewrite one current artifact, hand off with explicit implementation direction |
| Implementation: what is the smallest coherent solution? | Use sufficient, clear machinery while preserving contracts, safeguards, diagnostics, and testability |
| Self-review: can this pass support continued work or completion? | Assess behavior, design, simplicity, and evidence within the pass and affected boundaries |
| Simplicity: what did the problem not earn? | Challenge unused flexibility, duplicate capabilities, and unjustified abstractions without chasing fewer lines |
| Verification: what actually supports the result? | Inspect checks of the relevant content and conditions; distinguish current results from nearby or stale work |
| Communication: how should I explain it? | Use project formats and personal writing style, preserving uncertainty and the difference between pass and task completion |
| Authorization: may I perform this action? | Apply the single baseline policy to a concrete preview, then use the host gate and verify the result |

## Complete engineering model

```text
ENGINEERING DEFAULTS: judgment and authorization
                    |
             GROUND / UNDERSTAND
                    |
         +----------+-------------------+
         |                              |
      QUESTION                        CHANGE
         |                              |
   trace current evidence         plan warranted?
         |                         no       yes
   answer grounded                  |        |
   behavior first                   |     planning
         |                          |  research / converge
         |                          |     plan.md
         |                          |        |
         |                          +----+---+
         |                               |
         |                 EXPLICIT IMPLEMENTATION DIRECTION?
         |                   no -> report proposal; stop
         |                   yes -> implementation
         |                          construct a pass
         |                               |
         |                     implementation-review
         |                     challenge; adjust; verify
         |                               |
         +----------+--------------------+
                    |
             VERIFY / REPORT
                    |
             COMMUNICATE
          writing; visual if useful
                    |
             EXTERNAL ACTION?
             no           yes
           finish       exact preview
                             |
                       explicit approval
                             |
                        host/tool gate
                             |
                          execute
                             |
                          read back
```

Verification happens where it provides useful evidence, including during construction. The arrows do not require duplicate checks or artifacts. Tiny work uses focused understanding and verification. Questions authorize inspection and explanation only. Project profiles supply identity/private conventions when needed across these branches; repository guidance supplies team contracts. No PR review swarm is active in V1.

## Always-on principles versus on-demand procedures

The baseline owns decisions that should influence almost every engineering task: understand before editing, ground conclusions in evidence, challenge unsuitable means while preserving the goal, locate ownership, distinguish obligations from assumptions, bound scope, preserve unrelated work, prefer coherent simplicity, and verify before claiming success. It also contains short context triggers and the one normative external-action policy.

`planning` earns a separate procedure because it owns a recurring research/discussion cycle, one evolving artifact, and a no-code handoff. Baseline grounding supplies its evidence discipline; writing supplies expression. It has no dependency on a tracing skill, visualization skill, custom agent, or subagent hierarchy. The trigger is an explicit planning request or consequential uncertainty/contracts/sequencing/risk that benefits from a durable proposal, not file count. Ordinary implementation still needs no persistent plan.

The plan is the current proposal. Its flexible contract covers the problem, relevant current system, approach, coherent increments and verification; unresolved material questions remain only until answered. Revision rewrites affected sections, removes superseded material, and checks the whole artifact including downstream steps and visuals. A plan is neither a transcript nor an ADR; a separate architectural record needs independent durable value and its own scope. No history system, universal phase sequence, task IDs, or implementation code is generated.

The [planning skill](skills/planning/SKILL.md#choose-one-artifact) owns location resolution. Explicit destinations and verified repository/profile conventions precede a checkout-local Git metadata fallback resolved through Git, including linked worktrees. This keeps ephemeral company plans out of tracked source and shared private workflow configuration without an installer storage service. The resolved path and target repository accompany handoff. Local metadata is not synced and is not guaranteed to survive worktree removal; cross-machine sharing needs an explicitly chosen destination and publication authorization where applicable.

Planning writes only its artifact and needed directory. It stops at the current proposal; agreement alone is not direction to code. Existing explicit implementation direction remains valid within its scope. Implementation uses the plan as evidence and updates that same proposal when consequential discoveries invalidate it, reconciling before dependent work. Routine implementation choices remain autonomous. This local handoff is separate from the unchanged External-action policy.

`implementation` owns construction choices during meaningful code work: learn the affected subsystem's vocabulary and conventions; locate semantic ownership; shape interfaces/functions/data around that responsibility; preserve error meaning; explain non-obvious contracts; and introduce behavior with useful observable checks. It distinguishes an established contract from a historical accident and a larger redesign opportunity. It does not require a spec, TDD, approved test seams, line quotas, or automatic commits. This fills a recurring gap that post-pass critique cannot address while code is being shaped. Baseline gains only a short trigger, not a construction handbook.

Functional-first sequencing belongs to these task layers: planning normally puts functional phases before a final test/verification phase; implementation owns diagnostic feedback during construction and test reconciliation once production behavior is coherent; implementation-review judges test obligations against the current phase. Intentionally deferred maintenance is acceptable during construction, but must be resolved with meaningful coverage and required checks before completion. Baseline retains universal contract preservation and verification honesty without absorbing this sequencing procedure.

Normal and deeper repository questions remain in baseline grounding for V1. Its existing dependency scope, owner/invariant inspection, counterexample, evidence/inference distinction, locations, no-edit boundary, and stopping rule already supply the proposed tracing procedure. A new tracing skill would mostly restate those instructions. Broad maps and persistent code tours are different requested artifacts; no automatic architecture files are created.

Visualization remains presentation inside writing guidance. It consumes inspected facts, labels inference/proposals, and uses a compact flow/table/diagram only when it improves understanding. It has no independent truth-gathering or mutation authority. Rich browser formats add dependencies and viewer assumptions without a demonstrated recurring gap here. [Research](docs/research.md) records the alternatives and extension criteria.

`implementation-review` owns the bounded, iterative self-review of a meaningful implementation pass: establish its intended behavior and comparison, inspect behavior and design, test consequential suspicions, challenge unearned machinery, evaluate test value, and account for verification. Its details can evolve without adding always-loaded text. A review procedure alone cannot prevent premature implementation, so ownership and evidence defaults remain in baseline. Verification honesty remains there so skipping the skill on a tiny task cannot license unsupported success claims.

The baseline triggers review after a meaningful nontrivial pass, before treating it as complete, and for requested implementation reviews. It does not trigger after every edit. Earlier findings and check results remain usable when content, contracts, and relevant conditions still support them. Changes to a caller can invalidate a conclusion even with an unchanged hunk; a new SHA alone need not invalidate the whole assessment. The baseline supplies a direct-review fallback if the skill cannot load.

Review stops when the relevant evidence and proportionate verification are accounted for, material concerns are resolved or clearly reported, and more investigation is unlikely to change the decision. Reported uncertainty can still block dependent work. An intentionally partial pass may be ready for continued development while requested work or final repository gates remain outstanding; it must not be represented as a completed feature. Verification can occur during implementation or review; the flow does not require duplicate runs of the same checks.

Simplicity stays inside this skill because it uses the same change, owner, and contract evidence as correctness. It tests whether machinery earns its cost through a current responsibility. Removal, standard-library reuse, native/repository reuse, avoiding speculative flexibility, and clearer expression are alternative lenses, not output tags or a fixed ladder. A one-implementation adapter may be justified by an existing contract or test boundary. Removing useful diagnostics or compressing explicit logic can make a solution worse. No separate simplicity skill would add an independent responsibility here.

`prepare-pr` consumes current assessment evidence. When it is missing or materially invalidated, preparation can request bounded reassessment in review-only mode; tiny PRs get focused checks. Preparation still checks the pinned proposal's whole requested scope and remote state. Self-review is not exhaustive PR review, specialist audit, release certification, or integration approval. A later integration-review mechanism could consume the same ordinary evidence, but no swarm, specialist routing, agent hierarchy, or placeholder interface is implemented. Review-only requests do not authorize source fixes; no skill redefines authorization.

## Ownership and loading

| Source | Consumer / when loaded | Owns | Does not own |
| --- | --- | --- | --- |
| `instructions/baseline.md` | Model, through a surface's active instructions | Operating principles, context triggers, authorization, context-inspection response | Review checklist, language manual, private project facts |
| `skills/planning/SKILL.md` | Model, for requested plans or warranted durable proposals | Bounded research, material decisions, current plan artifact, in-place revision, no-code handoff | Implementation authority, conversation history, ADR archive, universal web research, task database |
| `skills/implementation/SKILL.md` | Model, during meaningful implementation | Construction in the affected subsystem, vocabulary, shape, contracts, observable checks | Independent publication, mandatory spec/TDD, final assessment |
| `skills/implementation-review/SKILL.md` | Model, after a meaningful nontrivial pass or for requested self-review | Bounded comparison, behavior/design/simplicity assessment, test value, verification and gaps | Exhaustive PR review, specialist audits, publication, permission grants, exact repository commands |
| `skills/prepare-pr/SKILL.md` | Model, for PR preparation/creation | Repository and revision resolution, proposal, reviewers, approved writes and readback | Fixes, commits, implicit pushes, duplicated implementation audit |
| `skills/jira-story/SKILL.md` | Model, for story drafting/creation | One story from requirements through approved creation/readback | Story implementation, incidental issue updates |
| `projects/index.md` and one profile | Model, when work depends on project identity/conventions | Identity, private routing, verified facts, project templates and check hints | Credentials, generic engineering procedure, inferred requirements |
| `writing/style.md` and matching example if present | Model, before meaningful engineering prose | Voice, density, structure, useful diagrams, style calibration | Project identity, acceptance criteria, verification facts |
| Existing repository guidance, code, templates | Model, as applicable to affected work | Repository contracts, architecture, team conventions | Personal workflow policy or private routing |
| Repository checks; this source's `setup.py` and tests | Python/tool runtime, explicitly executed | Mechanically testable contracts; rendering, ownership and drift | Model judgment, live instruction loading, host permissions |
| `README.md`, `DESIGN.md`, `docs/` | Human maintainer; model only when explicitly relevant | Overview, rationale, setup/recovery, compatibility, provenance, validation | Always-on model context |

Names and descriptions are skill discovery metadata; the body is loaded when selected. Profiles and writing files are explicitly read, not automatically included because a path appears. Missing context blocks dependent work only. On request, the baseline reports actual reads and loading gaps without claiming to inspect hidden model attention.

### Responsibility and context-cost decisions

| Concern | Owner and reason |
| --- | --- |
| Evidence, goals versus means, scope, ownership, honest claims | Baseline: these apply before any specialized task |
| Research to a convergent current proposal and implementation handoff | Planning: recurring artifact procedure, with existing grounding and writing owners |
| Neighboring patterns, domain names, meaningful extraction, narrow interfaces | Implementation: decisions during construction, learned from the subsystem |
| Error boundaries, useful types/invariants, rationale/public semantics, test seams | Implementation: preserve meaning while introducing behavior; repository contracts supply specifics |
| Does the resulting change work, belong here, earn its complexity, and have evidence? | Implementation-review: challenge the artifact using concrete triggers; do not repeat a construction checklist |
| Exact style, language idioms, team conventions and commands | Repository guidance; formatters, linters, type checks and tests enforce deterministic rules |
| Question-specific trace, observations versus inference, no edits, stop when answered | Existing baseline: another discovery entry/body is not yet justified |
| Prose and useful diagrams | Writing guidance: on demand, presentation never invents repository behavior |
| Numeric change budgets, short-function quotas, universal docstrings/DI, automatic commits | Nowhere: slogans or lifecycle constraints do not establish better changes |
| External action | Unchanged baseline policy plus host/tool gate; no skill can override it |

Five skill descriptions are discoverable; bodies load only for their tasks. The baseline has short planning and construction triggers. It does not absorb their procedures or force every skill into each session. These decisions can be revisited for observed failures, not to fill a conceptual box.

## Projects, writing, and publication

The index resolves actual Git root and remote identity, including worktrees, or an explicit story target. A Jira prefix cross-checks identity; it never selects another site by trial and error. Remote identity works across machines; an optional exact local-root fallback is machine-specific and unset in the examples. Profiles may be installed UNCONFIGURED for inspection, but remain unusable for live project actions until their facts are verified and status is READY. Their sample commands/hosts must not be used. Edit the private source index/profile, rerun setup on each machine, and verify a fresh session; installed profiles are never canonical. Connection names come from the active clients' existing MCP configuration. [Onboarding](docs/setup.md#project-onboarding) covers labeled machine roots/connection names and adding another project. Unknown identity does not prevent unrelated local work.

Repository guidance owns team contracts; profiles own private routing and personal conventions. When both describe the same project fact, inspect the current source and resolve a consequential conflict instead of treating profile hints as live truth. Required repository template fields shape PR structure; writing style shapes expression within it. `writing/style.md` owns scan-first presentation: the requested answer first, evidence and detail by importance, and visible outcomes and limits. Baseline supplies only the compact answer-first default and writing trigger; task skills retain procedure and evidence ownership. Matching examples use the style file's approval/calibration markers. Implementation reads comment calibration only when authoring meaningful embedded prose; standalone documentation uses the documentation example. No separate response mode or skill is needed.

`jira-story` uses requirements and create metadata to draft one complete action; `prepare-pr` pins the head/base comparison, distinguishes local/unpublished work, gets review evidence, and drafts the complete PR/reviewer proposal. Each stops at the draft for draft-only work. After approval of a concrete proposal, each executes only that action and reads back the remote result. Ambiguous writes are reconciled before retrying.

The single normative authorization policy remains [External-action policy](instructions/baseline.md#external-action-policy). It is preserved verbatim in this refinement. Skills name their mutation boundary and concrete preview, then defer to that policy. No `allowed-tools` grants are supplied. Host per-call permissions remain a separate execution gate; prose cannot enforce semantic payload equality or prevent a broadly authorized tool from running. [Setup](docs/setup.md) and [compatibility](docs/copilot-compatibility.md) explain the required host checks and surface limits.

## Portable installation

`setup.py` remains the sole installer/update/check implementation. It uses Python 3.12+ standard facilities, no shell commands, symlinks, executable scripts, network, or third-party packages. `Path.home()` resolves the user's home; `--home` selects an explicit destination for tests or intentional installation. Source discovery uses the script's location, not the working directory. Non-default `COPILOT_HOME` is rejected because equivalent discovery by other surfaces is not documented for relocated CLI storage.

The installer renders `{{WORKFLOW_ROOT}}` to `.copilot/engineering-workflow` under the resolved home and `{{BASELINE_PATH}}` to `.copilot/copilot-instructions.md`. One full generated baseline serves CLI discovery, manual app paste, and skill fallback. The modular `engineering-workflow` bridge provides VS Code discovery and may also be seen by CLI; its conditional read is best effort, not guaranteed deduplication. [Compatibility](docs/copilot-compatibility.md#baseline-rendering-and-duplicate-context) explains why the bridge remains. Absolute paths differ across machines; relative layout and behavior are equivalent. Forward slashes are serialization in Markdown/JSON accepted on both OSes, never an assumption about a shell. Source UTF-8 accepts a BOM and normalizes CRLF/LF; generated bytes use UTF-8 without BOM and LF. Installed drift compares exact bytes, so an editor's newline rewrite remains a local edit to preserve. If a console cannot encode a path, CLI output escapes those characters without changing installed paths or the operation's exit status.

Destinations must be relative, portable names beneath the selected home. Case/Unicode-normalization aliases, Windows device names, traversal, and linked paths beneath that home are rejected on every host where applicable. Temporary files are siblings, closed before replacement and removed on failure. Installed files are ordinary data; source executable bits and ACLs are not replicated. No Unix home layout or symlink privilege is required.

The old `personal-workflow` manifest stops setup before writes. The maintainer backs up and relocates just that record, then explicitly cleans up obsolete files/entries; current skill/CLI ownership hashes are retained. An unrecorded old bridge also blocks installation to avoid activating its replacement beside it. Unrelated neighbors remain untouched. [Migration](docs/setup.md#migration-from-personal-workflow) is an intentional one-time operation, not automatic deletion.

All conflicts are checked before writes. A file may be replaced only if absent, identical to the desired bytes, or matching its last owned hash. The manifest is an ownership record, not a security signature. Check mode detects missing/stale manifest entries as well as content drift and writes nothing. Installation repairs ownership only when content is safe to adopt. Removed sources block update/check and require explicit cleanup, preventing obsolete skills from silently remaining active.

Replacement is atomic per file, not a transaction over all files. One installer runs at a time; concurrent edits are outside the preflight guarantee. An interrupted update can normally be checked and rerun against the same source. Files matching neither desired bytes nor recorded ownership require inspection. [Setup and recovery](docs/setup.md) lists destinations, exit codes, and upgrade cleanup.

## Maintenance and validation

Choose the owner before changing a rule. Edit private source, run relevant checks, rerun setup, refresh the app UI paste from the generated CLI baseline if it changed, and start a fresh session. Never patch installed copies as a second source of truth. Human explanations belong here or in `docs/`; do not add them to the baseline to make maintenance easier.

Add a skill only for a coherent recurring procedure with a clear trigger, inputs, result, and mutation boundary. Use a lowercase directory matching frontmatter `name`; descriptions must distinguish nearby tasks. Setup currently packages files with a lowercase `.md` extension under `skills/`, `projects/`, and `writing/`, consistently on both OSes. Non-Markdown resources require an intentional installer extension and tests; they are not copied today. Relative skill references and rendered support paths must resolve in the installed tree.

Installer changes require `python -m unittest discover -s tests -v`. Tests exercise temporary homes, ownership, partial failure, encoding, adapters, and portable paths through the actual installer and CLI. [Behavioral scenarios](docs/verification.md) test routing, adaptive review, and claims against observed actions. Assertions about instruction wording are not evidence of better engineering. Native macOS execution and live Copilot loading/approval checks remain separate validation, not something simulated path tests can certify.
