# Engineering workflow for Copilot

A private engineering workflow for GitHub Copilot on Windows and macOS. It supplies engineering defaults, five task skills, project profiles, and writing guidance outside company repositories. The private source clone is canonical; files installed under your home are generated.

The opinion: **understand before editing, challenge unsupported assumptions, change the owning layer, and claim only what the evidence supports.** Use the minimum sufficient machinery that preserves behavior and real contracts.

```text
Engineering defaults (user scope, when loaded by the active surface)
                         +
Applicable repository guidance / AGENTS.md
                         +
Relevant task skill, with project and writing context when needed
                         +
Inspected repository code and live MCP evidence
```

This describes how context contributes, not a precedence ladder. Instructions guide decisions; `AGENTS.md` is repository-owned agent guidance; skills are procedures selected for a task. Skill names/descriptions are discoverable before their bodies are loaded. Profiles select private identity and conventions. MCP tools provide live evidence and separately approved actions.

| Layer | Question it owns | Source |
| --- | --- | --- |
| Engineering defaults | How should Copilot reason and decide? | [Baseline](instructions/baseline.md) |
| Repository guidance | What contracts and team rules apply here? | The work repository's instructions, code, tests, tooling |
| Planning | What current proposal should guide this change? | [Planning](skills/planning/SKILL.md) |
| Implementation | How should this meaningful change be constructed here? | [Implementation](skills/implementation/SKILL.md) |
| Implementation-review | Is this pass grounded, correct, proportionate, and verified? | [Implementation review](skills/implementation-review/SKILL.md) |
| Project profile | Which project, private conventions, and tool routes apply? | [Project index](projects/index.md) and one profile |
| Writing | How should engineering prose and useful visuals communicate it? | [Writing style](writing/style.md) |
| External action | What exact consequential action is approved? | [External-action policy](instructions/baseline.md#external-action-policy), plus host permissions |

Normal questions use baseline grounding: trace only evidence that can change the answer, cite useful locations, and answer first. There is no separate tracing or visualization skill in V1. Diagrams and tables present inspected facts when useful; simple answers remain prose. Meaningful implementation uses construction guidance, then bounded self-review, adjustment and verification. Tiny edits need focused checks. [DESIGN.md](DESIGN.md) shows the complete operating model.

**Functional-first implementation:** construct meaningful features to a coherent production state, then reconcile affected tests and add meaningful coverage in a final test/verification phase. Existing checks may run diagnostically during construction, and genuine defects still need correction when discovered. Final verification and review remain required. [Construction procedure](skills/implementation/SKILL.md#functional-first-implementation)

## Install and configure

Python 3.12+ is the only installer dependency. From this private clone:

```text
python setup.py
python setup.py --check
```

Use `python3` on macOS if needed. The recommended lifecycle is: clone, inspect/customize source profiles, install, check, verify loading, use. **Configuration is required before live project use, not before first setup.** UNCONFIGURED samples are safe to install for inspection; their example hosts, reviewers, and commands must not be used.

Setup renders `instructions/baseline.md` into one full baseline, `~/.copilot/copilot-instructions.md`. CLI discovers that file. A small `~/.copilot/instructions/engineering-workflow.instructions.md` bridge requests it in VS Code when applicable; inspect the actual read, especially for fileless questions. In the Copilot app, manually paste the full generated baseline into **Settings > Sessions > App instructions**. Setup cannot update that UI field. [Surface behavior and official sources](docs/copilot-compatibility.md)

Support files and the ownership manifest live under `~/.copilot/engineering-workflow/`; five skills live under `~/.copilot/skills/`. Here `~` means the home Python resolves on your machine. [Exact destinations, onboarding, conflict recovery, and migration](docs/setup.md)

## Planning and handoff

Ask “Use planning to research this change and write a plan; do not implement yet.” Use it for requested plans and changes whose ambiguity, contracts, sequencing, or risk warrants a durable proposal. Tiny fixes need no plan file; well-understood changes can use a brief internal plan. Multiple files alone do not trigger planning.

`plan.md` describes the current proposal: problem, relevant current system, approach, coherent steps and verification, with material open questions only while unresolved. Revisions replace superseded content and normalize the whole document. It stays readable after repeated discussion, with no automatic history or ADR archive. [Procedure](skills/planning/SKILL.md) · [Small illustrative example](writing/examples/plan.md)

An explicit destination or verified repository/profile convention takes priority, including whether the plan belongs in the repository. Otherwise planning resolves a local path with `git rev-parse --path-format=absolute --git-path engineering-workflow/plan.md` from the target checkout. Git handles linked worktrees; the artifact is untracked local metadata, not shared workflow configuration. It is not pushed or synced and can disappear when its worktree is removed. An unrelated plan is never overwritten. Without an available/permitted Git destination, choose a concrete local path; the agent can draft in chat while resolving it.

Planning reports the resolved path and repository. Hand those to a later session with “Implement this plan in this repository.” Plan acceptance alone does not authorize code edits. Implementation checks current evidence, resolves routine details, and reconciles consequential invalidation in the same plan before dependent work. Check discovery with CLI `/skills info planning`, app Customize > Skills, or VS Code Agent Customizations; inspect the actual skill read. VS Code `/plan` is its built-in agent, not an alias for this skill, and its session-memory draft is not the durable handoff. [Host distinctions](docs/copilot-compatibility.md#planning-surfaces-and-artifacts)

## How this combines with an existing Copilot setup

- **Already have AGENTS.md or repository Copilot instructions?** Setup never edits them or any work repository. Applicable instructions coexist. CLI combines them without general precedence; VS Code documents personal > repository > organization priority, with all supplied. Higher priority does not remove repository context. The app's documented settings do not establish an equivalent ordering. [Compatibility](docs/copilot-compatibility.md)
- **Already have Karpathy or other skills?** Unrelated skills remain untouched. A different skill at our exact destination blocks installation before writes. A same-name skill in another discovery location can shadow ours without a filesystem conflict; inspect its actual source.
- **Already have `~/.copilot/copilot-instructions.md`?** Different unowned or locally edited content is a conflict, not permission to overwrite. Merge wanted engineering defaults into source, back up the conflicting file, remove only that destination, and rerun. Byte-identical desired content can be adopted. Keep project rules in the work repository.
- **Where do I edit or update?** Edit the private clone, including `instructions/baseline.md`, `projects/`, and `writing/`; rerun setup and check on each machine. Never hand-maintain installed copies. Refresh the app paste after a baseline change or relocation to another home.
- **How do I see what loaded?** CLI: `/instructions`, `/skills list`, `/skills info implementation`. App: Customize > Skills and `/skills`. VS Code: Agent Customizations and Chat Diagnostics. Ask for the profile path and evidence actually read; inspect tool calls. Discovery alone does not prove invocation. [Session checks](docs/verification.md)

Existing MCP/editor configuration stays intact. Conversational approval and host tool approval remain separate: exact preview, explicit approval, host gate, execute, read back. No automatic commits, pushes, PRs, custom agents, router, or review swarm. Installer checks establish file state, not model compliance.

Upgrading the old `personal-workflow` layout requires [explicit migration](docs/setup.md#migration-from-personal-workflow) before installation writes anything. [Research decisions](docs/research.md) explain the accepted mechanisms and rejected lifecycle assumptions.
