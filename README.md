# Engineering workflow for Copilot

Engineering defaults, five task skills, private project context, and writing calibration for local GitHub Copilot sessions on Windows and macOS. Work repositories keep their own guidance and tooling. This clone is the editable source; installed files are generated.

## Configure and install

Python 3.12+ is the only installer dependency.

1. Copy `projects/project.example.md` to a meaningful local name such as `projects/sre-api.md` using Finder, Explorer, or your editor.
2. Fill in routing and connection facts, remove inapplicable fields, and verify them before setting `Configuration status: READY`. Repeat for other projects.
3. Run from this clone:

```text
python setup.py
python setup.py --check
```

Use `python3` on macOS if needed. Real profiles are ignored by Git. Setup scans them and generates the routing index; there is no index to maintain. Without READY profiles, setup installs an explicitly unconfigured index for inspection and unrelated local work.

Setup installs:

- `~/.copilot/copilot-instructions.md`: the full engineering defaults.
- `~/.copilot/instructions/engineering-workflow.instructions.md`: a VS Code bridge to those defaults.
- `~/.copilot/skills/`: the five workflow skills.
- `~/.copilot/engineering-workflow/`: generated project routing/profiles, writing guidance, and the ownership manifest.

In the **Copilot app**, paste the full generated `~/.copilot/copilot-instructions.md` into **Settings > Sessions > App instructions**. CLI discovers the baseline file; in VS Code, verify the bridge's actual baseline read, including fileless questions. Setup cannot update the app's UI setting. [Installation and project configuration](docs/setup.md) ? [Surface behavior](docs/copilot-compatibility.md)

## Everyday use

| Task | Procedure |
| --- | --- |
| Research a change and converge on a proposal | [planning](skills/planning/SKILL.md) |
| Construct an authorized change | [implementation](skills/implementation/SKILL.md) |
| Assess a meaningful implementation pass | [implementation-review](skills/implementation-review/SKILL.md) |
| Draft or create one Jira story | [jira-story](skills/jira-story/SKILL.md) |
| Prepare or create a PR | [prepare-pr](skills/prepare-pr/SKILL.md) |

Ask for planning when you want a durable proposal. Its default is `<repository-root>/plan.md`; an explicit destination takes priority. [The planning skill](skills/planning/SKILL.md#choose-one-artifact) owns the location and handoff rule. Pass the resolved path and repository to a later session with explicit direction to implement. Accepting a plan alone does not authorize code changes.

Meaningful implementation uses construction guidance, then bounded review and verification. Small clear edits need focused checks. Ordinary repository questions use the [baseline](instructions/baseline.md) directly. Publication follows its [external-action policy](instructions/baseline.md#external-action-policy).

## Coexistence and maintenance

Setup preserves AGENTS.md, repository instructions, existing MCP/editor settings, and unrelated skills. Different content at one of its exact destinations blocks installation before writes. A same-name skill elsewhere may shadow this workflow; inspect the actual source loaded.

Edit this clone, rerun setup and check, refresh the app paste when the baseline changes, and start a fresh session. Transfer ignored profiles separately between machines; Git updates the workflow and template without syncing local project facts. Never edit installed copies or store credentials in profiles.

[Current architecture and owners](DESIGN.md) ? [Conflict recovery](docs/setup.md#update-and-recover) ? [Verification checklist](docs/verification.md)
