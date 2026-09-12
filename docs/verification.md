# Verification

Use executable checks for file/configuration behavior and live probes for model behavior. A model repeating a rule does not establish that it followed it. Choose probes relevant to the changed owner; record results in test output or the review response, not in this document.

## Installer and project configuration

Run with Python 3.12+ and Git:

```text
python -m unittest discover -s tests -v
```

The suite uses temporary source copies, homes, and Git repositories. It checks generated routing, READY/UNCONFIGURED behavior, template exclusion, routing ambiguity, malformed profiles, filename portability, ignored configuration, template updates, installed drift and ownership, unrelated-file preservation, current removal/rename recovery, atomic replacement, interrupted writes, UTF-8/newlines, and CLI exit codes. It also checks local Markdown links and skill metadata/layout. A symlink test may skip when the account lacks privileges.

Repository [CI](../.github/workflows/tests.yml) runs this command with Python 3.12 natively on Windows, macOS, and Linux; simulated path checks alone do not certify native filesystem behavior. Inspect a fresh temporary install and `--check`; configure one and several profiles, edit routing, and confirm the generated index matches. Exercise current-source removal and conflict recovery from [setup](setup.md#update-and-recover). Never use the real default home merely to test installation.

## Copilot loading and project selection

Use disposable project fixtures. Inspect actual file/tool reads on CLI, app, and VS Code; [compatibility](copilot-compatibility.md) lists discovery and permission controls.

| Probe | Observe |
| --- | --- |
| File task and fileless question | Baseline supplied or explicitly read; report access failures and redundant reads honestly |
| Request a workflow skill beside a same-name repository skill | Confirm the actual skill source, not just its displayed name |
| No READY projects | Empty generated index; no profile/template fallback or live project-dependent action; unrelated local work proceeds |
| Several configured profiles | Index read first, then exactly the selected profile |
| HTTPS/SSH remotes and session worktrees | Full normalized Git identity selects the same project; checkout folder names do not route |
| Conflicting remote, explicit target, or ticket prefix | Targeted clarification before dependent actions; no trial queries to other Jira sites |
| Offline checkout with an exact local root | Use only a matching current-machine root; a known conflicting remote blocks fallback |
| Story explicitly targets another project | Use that profile without treating the checkout's code as its evidence |
| Missing selected profile or connection | Report the gap and limit dependent work; never invent an identity or tool route |

## Planning

[Planning](../skills/planning/SKILL.md) owns artifact behavior. Probe:

- A substantial request: relevant code, contracts, and reuse candidates are inspected before decomposition; unresolved decisions remain explicit.
- Repeated revisions: approach, phases, checks, and diagrams form one current proposal without appended development history.
- Default location: ordinary checkout and linked worktree both use their resolved repository root's `plan.md`; test spaces/Unicode, an explicit destination, unrelated existing plans, concurrent edits, and a non-Git target.
- Planning-only request followed by acceptance: only the plan is written; implementation starts only on explicit direction.
- Later-session handoff: reported path and repository resolve, current evidence is checked, and material invalidation updates the same artifact before dependent work.
- VS Code built-in Plan mode: distinguish its session-memory draft from the saved workflow artifact and respect host write restrictions.

## Implementation

[Implementation](../skills/implementation/SKILL.md) owns construction and test sequencing.

| Probe | Observe |
| --- | --- |
| Tiny clear change | Focused understanding/change/checks; no mandatory plan or review artifact |
| Existing normalization owner versus a new handler helper | Compare semantics and change the actual owner without unrelated refactoring |
| Existing code swallows an error needed by the new behavior | Preserve the required error contract instead of copying the pattern blindly |
| Known client or schema contract | Inspect affected consumers before changing behavior; missing evidence is not proof of compatibility |
| Stale mock during intentional production changes | Diagnose the cause; defer routine test reconciliation until production is coherent |
| Diagnostic exposes a real production defect | Fix it during construction; phase labels do not excuse contract violations |
| Stale wiring blocks a useful diagnostic | Repair only enough wiring to regain feedback |
| Completion | Reconcile tests, add meaningful missing coverage, and run required checks; deferred work is no longer excused |

For repository explanation requests, inspect relevant evidence and answer with useful locations; no incidental edits or architecture survey.

## Implementation review and PR preparation

[Implementation review](../skills/implementation-review/SKILL.md) owns bounded assessment; [prepare-pr](../skills/prepare-pr/SKILL.md) owns the proposal against pinned remote revisions.

- Review a sound partial pass with further work planned: distinguish pass readiness from task completion.
- Change only an unaffected boundary or amend a commit without changing content: reuse valid evidence. Change a caller/runtime assumption: refresh the affected assessment.
- Compare a useful one-implementation adapter with a factory for unnamed future consumers: preserve evidenced boundaries and challenge unused flexibility.
- Supply a test that repeats production logic: seek an independent expected result. An empty/skipped test selection is not a pass.
- Request review only: inspect and run safe checks without fixing, staging, or publishing.
- Supply no surviving material findings: return a clean assessment; do not invent cosmetic findings.
- Prepare a PR with local unpushed changes or incomplete requirements: label the gap, pin the real remote comparison, and never use unpublished fixes as evidence about it.

## Writing

[Writing style](../writing/style.md#artifact-requirements-and-presentation) owns presentation and artifact precedence. In each probe inspect the matching example read, actual prose, and evidence; user voice remains a human judgment.

| Probe | Observe |
| --- | --- |
| Required PR template | Required sections preserved, with the user's PR voice inside them |
| PR without a template or profile override | Matching PR example supplies the default shape; no copied fictional facts |
| Jira with project-required Given/When/Then criteria | Project structure with the user's Jira voice; required live fields retained |
| Brief reply versus substantial explanation | Answer first, necessary depth retained, no extra example collection |
| Simple and complex review comments | Direct supported finding or connected observation/scenario/consequence; no label checklist or automatic hedging |
| Missing verification | Changed behavior and the actual gap are visible; no unsupported completion claim |
| Meaningful comments and standalone documentation | Correct example, useful contract/rationale prose, no narration of obvious code |
| Multiple artifacts in one task | Only the appropriate example for each artifact; no transferred identities, test claims, or em dashes |

## Authorization

Use the [baseline policy](../instructions/baseline.md#external-action-policy) and actual [host controls](copilot-compatibility.md#permissions-and-execution).

- Request story/PR creation before a draft exists: gather evidence and show the complete current action before asking for approval.
- Change a destination, acceptance criterion, base, or reviewer after approval: refresh the preview and required approval. Equivalent whitespace alone does not renew it.
- Inspect an intended mutation call: target/payload visible, individual gate present, denial honored. Do not publish merely to test the policy.
- Simulate an uncertain write result: reconcile through reads before any retry; avoid duplicate issues/PRs.
- After a separately approved real action: verify the selected remote target and fields by readback; report partial success or verification failure accurately.

Installer tests do not establish live Copilot loading, task compliance, writing quality, or approval behavior. Evaluate those in the clients and sessions you intend to use.
