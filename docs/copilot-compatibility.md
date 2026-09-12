# Copilot compatibility

These are documented host capabilities and limitations. Installation tests establish file state; verify actual loading and permissions in the client you use.

## Instructions and coexistence

GitHub recommends short, broadly applicable custom instructions. Specialized procedures belong in skills loaded when relevant. This workflow uses a baseline with task/context triggers and five separate skill bodies. [GitHub instruction guidance](https://docs.github.com/en/copilot/concepts/prompting/response-customization), [Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)

| Surface | Current loading and composition |
| --- | --- |
| CLI | Discovers `~/.copilot/copilot-instructions.md`, modular user instructions, repository instructions, and applicable AGENTS.md. Applicable files combine without a general precedence order; avoid conflicts. `/instructions` shows discovered files and permits disabling them. [CLI instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions) |
| VS Code agent Chat | Discovers user `.copilot/instructions` files and applicable repository instructions/AGENTS.md. All are supplied; documented priority is personal, then repository, then organization. Ordering among multiple project instruction files is not guaranteed. [VS Code instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions) |
| Copilot app | Global instructions are edited under Settings > Sessions > App instructions; repository-specific instructions have a separate UI field. Repository/CLI skills and MCP connections are available. That sharing does not establish automatic CLI baseline loading or a complete AGENTS.md precedence order in the app. [App customization](https://docs.github.com/en/copilot/how-tos/github-copilot-app/customize-github-copilot-app) |

Setup preserves repository guidance and other personal configuration. It deploys local home files only; it does not configure GitHub.com or upload private profiles there.

## Baseline rendering and duplicate context

Setup generates one full baseline at `~/.copilot/copilot-instructions.md`. CLI discovers it, the app uses a manual paste, and skills can read it explicitly. The VS Code `engineering-workflow.instructions.md` bridge uses `applyTo: "**"` and requests a baseline read when its full text is absent.

The bridge's file pattern does not guarantee activation for fileless questions. Attach/read the baseline when needed. CLI also discovers the bridge; its identical-file deduplication does not guarantee deduplication of a later model-directed read. Treat the conditional read as model judgment and inspect actual tool calls. [CLI loading](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions), [VS Code file instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions)

## Skills and active context

Personal skills under `~/.copilot/skills` are supported by CLI and VS Code and available in the app. Descriptions support discovery; bodies/resources load for relevant tasks. A project skill can shadow a personal skill with the same name in CLI, whose documented duplicate-name rule is first-found by search priority. These skills do not set `allowed-tools`. [GitHub skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills), [CLI skill reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference), [VS Code skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)

| Surface | Inspect |
| --- | --- |
| CLI | `/instructions`, `/skills list`, `/skills info implementation` |
| App | Customize > Skills, `/skills`, `/skills reload`, and the instruction UI |
| VS Code | Agent Customizations, Chat Diagnostics, response References, and actual file reads |

Discovery alone does not prove invocation. Start a fresh session after updates and inspect the selected profile/skill path and MCP site. [CLI reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference), [App commands](https://docs.github.com/en/copilot/reference/github-copilot-app-reference/slash-commands), [VS Code customization](https://code.visualstudio.com/docs/agent-customization/custom-instructions)

## Planning surfaces and artifacts

VS Code's built-in Plan agent, also available through `/plan`, is distinct from this workflow's `planning` skill. Its draft lives in `/memories/session/plan.md`; the documentation says session memory is unavailable after the conversation ends. [VS Code planning](https://code.visualstudio.com/docs/agents/run/planning)

Explicitly request our skill and inspect its read. Its [artifact rule](../skills/planning/SKILL.md#choose-one-artifact) defaults to `<repository-root>/plan.md`. When using a restricted host planning mode, resolve a permitted persistent destination without bypassing tool grants. Neither a skill nor a plan-mode label alone enforces per-file write boundaries.

## Permissions and execution

The baseline owns [external-action authorization](../instructions/baseline.md#external-action-policy). Host permissions are a separate execution gate:

- CLI distinguishes available tools from permission to use them. Inspect persistent approvals and startup flags; deny rules override allows. [CLI permissions](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools)
- The app's `/reset-allowed-tools` clears session-level approvals and disables auto-approval. Inspect the actual pending call and session settings. [App commands](https://docs.github.com/en/copilot/reference/github-copilot-app-reference/slash-commands)
- VS Code offers Manual permissions, Assisted permissions, and Allow all. Assisted approval is not necessarily human approval; Copilot Agent Host worktree sessions use Allow all. Use a session with individual approval or keep consequential mutation tools disabled. [VS Code approvals](https://code.visualstudio.com/docs/agents/run/approvals)

Before relying on a consequential tool, check that its target/payload are visible and denial works, without executing a test publication. A tool gate does not prove that the payload equals the conversational preview. Setup cannot inspect UI settings or certify model compliance. [Live checks](verification.md#authorization)
