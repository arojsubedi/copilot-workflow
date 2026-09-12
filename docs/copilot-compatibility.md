# Copilot compatibility

Checked against primary documentation on **2026-09-10**. These are documented contracts, not live client results. GitHub's term *personal instructions* describes scope; our system is *engineering workflow* and its baseline *Engineering defaults*.

## Surface-specific loading and precedence

| Surface | Loading | Composition and precedence |
| --- | --- | --- |
| CLI | Global `.copilot/copilot-instructions.md`, modular user instructions, repository guidance and applicable agent files. | Applicable instructions combine; no general precedence order. `/instructions` can disable individual files. [CLI guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions) |
| VS Code agent Chat | User `.copilot/instructions`, repository instructions and enabled AGENTS.md; our bridge requests the baseline. | Personal > repository (`.github/copilot-instructions.md` or AGENTS.md) > organization; all types supplied. The page also says multiple project files have no guaranteed order. These are distinct claims. [VS Code guide](https://code.visualstudio.com/docs/agent-customization/custom-instructions) |
| Copilot app | Manual Settings > Sessions > App instructions paste; repository-specific UI instructions. Repository/CLI skills and MCP connections are available. | The customization page does not establish a complete ordering with AGENTS.md or automatic CLI baseline loading. Shared skills/MCP support does not establish shared instruction semantics. [App guide](https://docs.github.com/en/copilot/how-tos/github-copilot-app/customize-github-copilot-app) |
| GitHub.com Chat | Separate web personal-instructions UI; local files are not installed there. | Web guide: personal > applicable path-specific > repository-wide > agent > organization; all relevant sets supplied. Feature support is narrower: the matrix lists personal, repository-wide and organization instructions for web Chat. [Web guide](https://docs.github.com/en/copilot/concepts/prompting/response-customization), [support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support) |
| Cloud agent / code review on GitHub.com | Supported repository and organization context; setup deploys nothing to them. | Both support repository-wide, path-specific, AGENTS.md and organization instructions. Cloud also supports documented alternative agent files. Local private profiles are not deployed. [Support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support) |

The web guide says PR review reads repository instructions, agent instructions and skills from the **head branch**. This does not give review access to local home files. [Web guide](https://docs.github.com/en/copilot/concepts/prompting/response-customization)

Setup never touches AGENTS.md, repository Copilot/path instructions, or repository skills. Repository contracts own team rules architecturally; this is not an invented host precedence mechanism. Higher priority does not remove applicable repository context. Resolve consequential conflicts explicitly.

## Baseline rendering and duplicate context

`instructions/baseline.md` is canonical. Setup generates one full `.copilot/copilot-instructions.md`, also used for app paste and skill fallback. Redundant support `baseline.md` and `app-instructions.md` copies are removed through migration.

The small `engineering-workflow.instructions.md` bridge remains for VS Code's documented user directory. Its `applyTo: "**"` covers file context, not every fileless question. Attach/read the generated baseline when needed. Legacy location settings are deprecated and Local-agent-only; Agent Host uses supported user folders. [VS Code guide](https://code.visualstudio.com/docs/agent-customization/custom-instructions)

CLI also discovers the bridge. Its documented deduplication covers identical global user, repository-wide and agent instructions, not a bridge's later tool read. Relative `@` imports are constrained and not expanded in modular instructions; they do not replace this bridge. [CLI guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)

**The conditional read is model judgment, not guaranteed context inspection.** It uses visible text and reads when uncertain. Redundant reads remain possible. Two full automatic files would deliberately duplicate defaults on matching CLI tasks; a modular-only baseline would lose documented CLI global/fileless coverage. No simpler shared automatic location is established by the inspected docs. The retained bridge is a compatibility tradeoff. The app UI is still a separate manually refreshed copy.

## Skill discovery and active context

Skills are selected procedures, not another universal instruction-priority tier. Names/descriptions support discovery; bodies and resources load when needed. [GitHub skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills), [VS Code skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)

CLI resolves duplicate names first-found: project `.github/skills`, `.agents/skills`, `.claude/skills`, inherited parent `.github/skills`, personal `~/.copilot/skills`, personal `~/.agents/skills`, plugin, custom, added roots, then built-ins. A preserved repository skill can shadow ours. This differs from conflicting ownership of one installed file. Our skills omit `allowed-tools`, which can grant automatic permissions. [CLI reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)

VS Code supports personal skills in `~/.copilot/skills`, `~/.claude/skills`, and `~/.agents/skills`; do not assume CLI's entire ordering. No forked-context feature is required. [VS Code skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)

| Surface | Inspect |
| --- | --- |
| CLI | `/instructions`, `/skills list`, `/skills info implementation`; check enabled paths and selected source. Start fresh after updates. [CLI reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference) |
| App | Instruction settings, Customize > Skills, `/skills`, `/skills reload`; inspect paste and tool reads. Commands depend on session/build. [App commands](https://docs.github.com/en/copilot/reference/github-copilot-app-reference/slash-commands) |
| VS Code | Agent Customizations, Chat Diagnostics, response References; verify bridge and actual baseline read. Root AGENTS.md depends on settings; nested discovery is experimental. [VS Code guide](https://code.visualstudio.com/docs/agent-customization/custom-instructions) |

Ask for the repository/profile/skill/writing files actually read and selected MCP site; inspect calls. Discovery does not prove invocation or expose hidden attention. `--check` verifies bytes and ownership, never UI settings or live behavior.

Project loading still uses `~/.copilot/engineering-workflow/projects/index.md` and exactly one selected profile. Setup generates these from ignored local source configuration, installing only profiles referenced in the index table. The two committed `.example.md` files are human templates and are never installed. Without a source index, setup installs an empty UNCONFIGURED index; a passing `--check` for that state establishes consistency only. Missing/unconfigured identity blocks live project-dependent actions, while unrelated local work remains available. See [onboarding and migration](setup.md#project-onboarding).

## Planning surfaces and artifacts

VS Code's built-in Plan agent (also invoked with `/plan`) researches, asks questions, revises its proposal, and offers Start Implementation. It saves a draft to `/memories/session/plan.md`; the documentation says session memory is cleared when the conversation ends and is unavailable to subsequent sessions. That path is host memory, not this workflow's resolved local artifact. [VS Code planning](https://code.visualstudio.com/docs/agents/run/planning)

The portable `planning` skill supplies artifact/revision/handoff behavior without a custom agent or tool configuration. Explicitly request the skill and inspect its read; `/plan` does not establish that it loaded. When using the built-in agent, request the current proposal at the workflow's chosen destination if permitted. If the host only permits its own draft, report that limitation and resolve a permitted persistence path before claiming a durable handoff. Do not change tool grants or bypass plan-mode restrictions to write it. Git metadata may be hidden from default search: provide the resolved path and target repository to the implementation session.

Skill instructions express a no-code boundary; they do not enforce per-file write permissions. A custom planner with an edit tool likewise does not by itself constrain edits to a plan. No identical Plan-agent UI, memory lifetime, slash invocation, or handoff behavior is assumed across CLI, app, and VS Code. Verify artifact persistence, actual loaded skill, and explicit implementation direction in each live surface. [GitHub skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills), [GitHub planner example](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents)

## Visualization and viewers

V1 uses prose, tables, plain text, or compact Mermaid when useful. VS Code documents interactive Mermaid in Chat through `renderMermaidDiagram`; rendering remains client-dependent. [VS Code release notes](https://code.visualstudio.com/updates/v1_109)

App canvas extensions do not establish native support for arbitrary third-party HTML/JSON; CLI is not a browser. CodeTour requires its viewer, Excalidraw needs a compatible viewer, and HTML needs a browser or explicit integration. No custom renderer is required here; retain a readable text answer. [App guide](https://docs.github.com/en/copilot/how-tos/github-copilot-app/customize-github-copilot-app), [CodeTour](https://github.com/microsoft/codetour), [Excalidraw skill](https://github.com/github/awesome-copilot/blob/main/skills/excalidraw-diagram-generator/SKILL.md)

## Permissions and execution

CLI separates tool availability from permission, including persistent location grants and startup allow/deny rules. Denials override saved approvals; resetting session permissions does not prove persistent grants disappeared. [CLI permissions](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools)

The app has Interactive/Autopilot controls and `/reset-allowed-tools`, which clears session approvals and disables auto-approval. Keep individual approval for consequential actions. Host critique commands do not prove correctness or workflow compliance. [App commands](https://docs.github.com/en/copilot/reference/github-copilot-app-reference/slash-commands)

VS Code names its levels **Manual permissions**, **Assisted permissions**, and **Allow all**. Inspect saved rules in Manual. Assisted uses a model judge, not guaranteed human approval. Allow all and Autopilot skip prompts. Documentation says Copilot Agent Host **worktree sessions always use Allow all**. Use a session with individual call approval or keep external mutation tools disabled. Do not generalize this to every Copilot app worktree. [VS Code approvals](https://code.visualstudio.com/docs/agents/run/approvals)

The unchanged baseline policy requires exact preview, explicit approval, host/tool gate, execute, then readback. No client setting makes a Markdown preview a machine-enforced payload contract. Installer tests cannot establish live approval or model compliance.
