# Technical details

This document describes the current installer and runtime integration. It is optional depth for maintainers; ordinary configuration and operations are in [setup.md](setup.md).

## Installed layout

Setup resolves the selected home through Python and manages these destinations:

| Source | Destination under the selected home |
| --- | --- |
| `instructions/baseline.md` | `.copilot/copilot-instructions.md` |
| Generated VS Code instruction adapter | `.copilot/instructions/engineering-workflow.instructions.md` |
| READY profiles and generated project lookup | `.copilot/engineering-workflow/projects/` |
| `writing/**/*.md` | `.copilot/engineering-workflow/writing/` |
| `skills/**/*.md` | `.copilot/skills/<name>/` |
| `skills/*/scripts/*.py` | `.copilot/skills/<name>/scripts/<filename>` |
| Direct `agents/*.agent.md` | `.copilot/agents/<filename>` |
| Generated ownership data | `.copilot/engineering-workflow/install-manifest.json` |

Human documentation and `projects/project.example.md` remain source-only. Setup renders workflow and personal-instruction paths into runtime Markdown. Source Markdown accepts UTF-8 with an optional BOM and ordinary platform newlines; installed files use UTF-8 with LF newlines.

Baseline, writing, skill and agent source paths are checked for links/redirection before reading. Skill-owned Markdown resources are discovered recursively, including nested `references/` paths, without a fixed resource list. Their installed paths receive normal collision and ownership checks. Local edits to active or stale managed resources block mutation.

Python skill scripts use the same UTF-8/LF rendering and manifest ownership. Setup installs them but never executes them. The PR-review parent invokes its report writer only for an authorized private report; custom reviewers retain read/search-only tools.

The read-only `--status` command uses the same expected-file rendering, manifest loading, hashes, and conflict inspection as install and check. It summarizes that shared inspection for a person but deliberately keeps drift exit semantics in `--check`.

Agent discovery is dynamic and case-sensitive, selecting only direct `.agent.md` files, with no fixed names or count. Status derives agent definitions and component state from expected destinations alongside skills. Profiles use the same rendering, portable collision checks, and ownership preflight as other managed Markdown. The manifest admits only direct `.copilot/agents/*.agent.md` destinations for agents.

## Project lookup generation

`setup.py` scans only Markdown files directly under `projects/`, excludes `*.example.md`, and installs profiles marked READY. It reads the `Project`, `Git remote`, `Jira prefix`, and optional `Local root` bullets from the Routing section. The rest of each profile remains free Markdown and is copied without interpreting reviewer or convention semantics.

The generated `projects/index.md` contains routing facts only. It lets runtime guidance select one profile without reading all private profiles. Project names and Git identities must be unique after case and Unicode normalization. Jira prefixes may be shared because several repositories can belong to one Jira project.

READY profiles reject exact template placeholders, reserved example domains, malformed Git identities, invalid Jira keys, unsafe filenames, and relative local roots. At least one Git remote or Jira prefix must identify the project. UNCONFIGURED profiles are not installed.

## Ownership and safe replacement

The manifest maps each managed relative path to the SHA-256 digest of the bytes last installed by this workflow. It is an ownership record, not a security signature.

Before install, update, or removal, setup validates all relevant paths and file states. A desired file may be created, adopted when its bytes already match, or replaced when its current bytes match the previously recorded digest. A stale managed file may be removed only when it still matches its recorded digest. Missing stale files require only manifest cleanup. A locally changed managed file blocks all mutation so the user can preserve it first.

Uninstall performs the same kind of full preflight against every manifest entry. It removes unchanged managed files and the manifest, treats absent managed files as already gone, and stops without deleting anything if a target differs or is not a regular file. It does not recursively remove `.copilot`, `.copilot/skills`, `.copilot/instructions`, or other shared directories.

Active and stale managed agents receive that same protection; unrelated agents are preserved. Runtime PR reports under `.copilot/engineering-workflow/reviews/` are not installed configuration. Setup neither generates nor accepts manifest ownership of them. Reports survive updates and uninstall; their safe creation and collision behavior belong to the [PR-review workflow](pr-review.md).

Writes use a closed temporary sibling followed by `os.replace`, which is atomic per file. The entire installation is not one atomic transaction. Run one setup process at a time; after interruption, `--check` and a rerun reconcile the remaining state.

## Path safety and portability

The implementation uses only Python 3.12+ standard-library APIs and makes no network or shell calls. It rejects manifest path escapes, absolute manifest paths, unsafe path components, reserved device names, and links or junctions below the selected home. It also rejects source destinations that would collide on common case-folding or Unicode-normalizing filesystems.

The selected home itself is resolved before these checks. The checks prevent accidental redirection and cross-platform ambiguity; they are not a defense against a hostile process racing filesystem changes.

## Copilot surfaces and other instructions

GitHub documents personal CLI instructions at `~/.copilot/copilot-instructions.md`, personal skills at `~/.copilot/skills/`, and repository instruction forms including `.github/copilot-instructions.md`, `AGENTS.md`, and `CLAUDE.md`. Support differs by Copilot surface, so inspect the capabilities of the client in use. [GitHub's support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support) lists current combinations.

Personal task skills use the stable `eng-` namespace in GitHub's documented personal skill location. Project-level skills win duplicate names in CLI; generic legacy aliases are not installed, and an exact namespaced collision still requires inspecting the selected source. See [discovery controls](setup.md#verify-skill-selection). Skill names and supplementary resources are discovered dynamically; unchanged obsolete owned paths are removed on update, while locally modified active/stale files block all mutation. The core skill explicitly directs conditional reads of supporting Markdown; discovery alone does not load every procedure into the model context. The clients expose different discovery and inspection controls; use the current client's instruction or skill view rather than assuming that installation proves loading. [GitHub's customization reference](https://docs.github.com/en/copilot/reference/customization-cheat-sheet)

Personal CLI agents are installed at `~/.copilot/agents/*.agent.md`. The CLI reference and configuration-layout pages give matching project definitions precedence over personal ones; some GitHub invocation guidance describes the reverse. Inspect the actual selected profile in a fresh client session instead of relying on its name alone. Installation at this path does not establish discovery or subagent support in every other surface. The main PR-review skill covers unavailable delegated perspectives where possible and discloses material gaps. [CLI configuration layout](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference), [CLI agent locations](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#custom-agent-locations), [invocation guidance](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents)

Internal `pr-review-` profiles target personal Copilot CLI dispatch and retain only `infer: false` for auto-delegation control, plus restricted read/search tools. The CLI command reference still documents that field. The broader cloud-agent configuration instead marks it retired and describes `disable-model-invocation`; those surface-specific controls are not stacked speculatively. Explicit named parent dispatch must be checked in the active client with inference disabled. If unavailable, keep the restriction and let the parent cover the question with any material independence gap disclosed. These custom agents have no required role in planning/implementation. [CLI frontmatter](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#custom-agent-frontmatter-fields), [cloud-agent configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)

Reviewer frontmatter explicitly grants only the portable `read` and `search` aliases, which read files and search repository text. GitHub documents a separate `web` alias for internet lookup. Version-specific freshness/deprecation evidence comes through the parent workflow; profiles do not receive shell, edit, delegation, web, or MCP mutation tools. [Custom-agent configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)

For Copilot CLI, GitHub says applicable personal and repository instructions are combined and does not define a general precedence order. The CLI `/instructions` command shows discovered files. This is not a hard isolation boundary between reviewed branch guidance and the personal skill. [CLI custom-instruction documentation](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)

This workflow installs personal/user-level instructions. Work repositories may also contain `AGENTS.md`, `CLAUDE.md`, or Copilot repository instructions. Relevant instructions may be combined depending on the surface, so avoid duplicating generic behavior in both places; repository files should contain repository-specific knowledge and instructions. This repository does not add an `AGENTS.md` because its maintainership rules are already expressed by its source, design, and tests.

The generated `engineering-workflow.instructions.md` adapter points VS Code clients to the shared personal defaults when their full text is not already visible. The Copilot app uses a manual paste into its app-instructions UI because setup cannot edit that setting. Restart or open a fresh session after changes; discovery alone does not prove that a particular file was loaded.

The reviewed configuration surface can include `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`, their imported files, project skills (`.github/skills`, `.claude/skills`, `.agents/skills`), `.github/agents`, `.github/hooks/*.json`, hooks in `.github/copilot/settings*.json` or `.claude/settings*.json`, and applicable MCP/LSP/plugin configuration. Inspect actual loaded configuration rather than treating this as an exhaustive permanent list. Setup installs none of these into work repositories. [CLI instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions), [skill locations](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills), [hooks](https://docs.github.com/en/copilot/reference/hooks-reference)

LSP servers can start automatically after directory trust; `.github/lsp.json` project configuration takes precedence over matching plugin/user definitions. Existing semantic operations are optional evidence tools, with executable configuration subject to the review's trust boundary. Setup neither installs nor manages language servers. [LSP loading](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/lsp-servers)

Sandbox policy is client configuration, not installed workflow enforcement. Verify current support and effective policy; local sandboxing is experimental, off by default, and currently requires a Windows Insiders build on Windows. Network and authentication availability must be checked separately. Setup does not enable it or broaden permissions. [Local sandbox use](https://docs.github.com/en/copilot/how-tos/cloud-and-local-sandboxes/using-local-sandboxing)

## MCP reference

[`mcp/mcp.example.json`](../mcp/mcp.example.json) is source-only reference material showing the current `mcpServers` shape for one standard-input server and one remote HTTP server. Setup does not install, merge, modify, or claim ownership of MCP configuration.

GitHub Copilot CLI currently stores user-level MCP definitions in `~/.copilot/mcp-config.json`. Manage real servers through Copilot's current MCP commands or configuration tooling, and do not commit credentials to this workflow. See [GitHub's MCP configuration documentation](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers).

## Validation and tests

`python setup.py --check` builds the expected file set and performs the same configuration, path, ownership, and drift preflight without writing. It returns `0` when installed state matches, `1` for safe differences, and `2` for conflicts or invalid input.

Run the automated suite with:

```text
python -m unittest discover -s tests -v
```

The tests use temporary source copies and homes. They cover READY and UNCONFIGURED profiles, single and multiple projects, project lookup changes, template exclusion, routing validation, reviewer preservation, unrelated-file preservation, ownership conflicts, stale files, interruption recovery, path safety, encoding/newlines, install/check/status/update/uninstall/reinstall behavior, dynamic skill discovery, the source-only MCP example, skill metadata/rendering, and Markdown links. A symlink-specific test can skip when the local account cannot create symlinks.

Automated filesystem tests do not establish that a Copilot client loaded the intended instruction, selected the correct project, followed writing calibration, or honored a conversational approval boundary. Verify those behaviors in the clients you actually use by inspecting discovered instructions, selected skills/profile, MCP target, and proposed external action.

Agent tests cover dynamic discovery/rendering/status, adoption and updates, stale and missing targets, refusal of local conflicts before any mutation, and preservation of unrelated agents and private reports through uninstall/reinstall. Content checks cover metadata, restricted tools, rendered references, workflow contracts, and links. [Sanitized review-quality cases](../tests/review-quality-cases.md) provide semantic evaluation packets and rubrics; they do not make model behavior deterministic. In fresh Copilot sessions, exercise focused and substantial output, read-only specialist handoffs, unavailable-evidence/delegation paths, and comment preview. Publication/read-back testing requires an explicitly approved disposable external target and payload.

Report-writer tests verify multiple immutable same-head runs, UTC collision suffixes, UTF-8/LF and read-back bytes, invalid components/revisions, containment, link/redirection refusal and I/O failures. Reports live at `reviews/<host>/<owner>/<repository>/pr-<number>/<head-sha>/<review-run-id>.md` below the workflow root; setup refuses ownership of that subtree. Review-lifecycle cases cover duplicates, addressed or still-applicable prior concerns, new evidence on an unchanged head, dispositions, natural summaries and replies. They assess semantics rather than exact wording or fixed agent selection.

Skill namespace migration tests cover safe removal of obsolete owned destinations, conflict refusal, dynamic discovery and unrelated-file preservation. Supplementary-resource tests cover recursive discovery/rendering, update/check/status, stale cleanup, source/destination redirection refusal, conflict preflight and unrelated-file preservation through uninstall/reinstall. Semantic cases separately exercise coverage closure, deletions, transition/retry behavior and execution/instruction trust, including manual maintained-built-in comparisons.

[Planning quality cases](../tests/planning-quality-cases.md) cover draft exclusion, native artifact ownership, coverage closure, freshness, and question-driven worker selection. [Review quality cases](../tests/review-quality-cases.md) cover neutral lifecycle detection and follow-up semantics. Actual model independence, client selection, Plan-mode restrictions and review quality require client evaluation; automated tests do not certify them.
