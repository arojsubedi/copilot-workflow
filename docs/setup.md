# Setup and updates

Keep this source in a private clone outside company repositories. Do not store credentials, company source, MCP configuration, logs, or session transcripts here. Python 3.12+ and its standard library are sufficient. Setup changes only the generated destinations below, never work repositories, AGENTS.md, MCP configuration, shell profiles, or editor settings.

## Install

1. Inspect `projects/index.md` and the profiles in the source clone. Prefer configuring the projects you will use now; leaving UNCONFIGURED samples is safe for installation/inspection. They permit illustrative drafts only, never use of sample hosts, commands, or reviewers.
2. Run `python setup.py`, then `python setup.py --check`. Use `python3` on macOS if needed. An absolute script path also works from another directory. Setup discovers source relative to itself.
3. In the **Copilot app**, copy the complete generated `~/.copilot/copilot-instructions.md` into **Settings > Sessions > App instructions**. Preserve wanted existing UI preferences by merging them into the source baseline and regenerating first; review the combined text before replacing the UI field. Setup neither reads nor writes that setting. [App customization](https://docs.github.com/en/copilot/how-tos/github-copilot-app/customize-github-copilot-app)
4. In **CLI**, use `/instructions`. In **VS Code**, inspect the `engineering-workflow` bridge in Instructions and its actual baseline read. Check the five skills: `planning`, `implementation`, `implementation-review`, `jira-story`, `prepare-pr`. [Surface distinctions](copilot-compatibility.md)
5. Keep existing GitHub/Jira MCP connections. Inspect duplicate skill names across repository, personal, and plugin locations. Verify loading and host permissions using [session checks](verification.md) before live use.

## Installed layout

`~` means the home resolved by Python, not a Unix-only path. Setup prints its destination. All these files are generated; human docs remain in the source clone.

| Source | Destination under the selected home | Consumer |
| --- | --- | --- |
| `instructions/baseline.md` | `.copilot/copilot-instructions.md` | Full CLI instructions; manual app paste; explicit read by VS Code/skills |
| Small bridge in `setup.py` | `.copilot/instructions/engineering-workflow.instructions.md` | VS Code file-context discovery; also discovered by CLI |
| `projects/**/*.md` | `.copilot/engineering-workflow/projects/` | Explicit read of index and selected profile |
| `writing/**/*.md` | `.copilot/engineering-workflow/writing/` | Explicit read when meaningful prose is needed |
| `skills/**/*.md` | `.copilot/skills/<name>/` | Task skill discovery and activation |
| Calculated SHA-256 hashes | `.copilot/engineering-workflow/install-manifest.json` | Installer ownership and drift checks; not model context |

There is one full generated baseline. The old support `baseline.md` and `app-instructions.md` copies are gone; skills and app paste use the CLI file. Source placeholders `{{WORKFLOW_ROOT}}` and `{{BASELINE_PATH}}` become machine-local absolute paths. The VS Code bridge is still needed because its documented personal discovery directory differs from CLI's global file. Its conditional read is a model instruction, not guaranteed context deduplication. [Loading tradeoffs](copilot-compatibility.md#baseline-rendering-and-duplicate-context)

`--home <directory>` selects a destination for inspection/tests or intentional installation. It does not configure Copilot to read that home. A conflicting `COPILOT_HOME` is rejected because cross-surface discovery of relocated CLI storage is not established. No default installation has to be performed to test this repository.

Planning adds ordinary Markdown files under the existing skill/writing discovery rules; updating the current layout needs no migration. Setup installs the procedure and illustrative example, never a company's plan artifact. Actual plans follow the [planning location rule](../skills/planning/SKILL.md#choose-one-artifact) in the target project context. They are not installer-owned or copied between machines by setup.

## Project onboarding

The private source repository owns configuration. The lifecycle is **clone -> inspect/customize source -> setup -> check -> verify loading -> use**. Before first setup, only a valid source clone and Python are required. Before live use, verify the selected project's identity and action-dependent facts, replace examples, then set its status from UNCONFIGURED to READY. READY is a maintainer assertion, not installer validation or permission to write.

Edit the source `projects/index.md` and the corresponding `projects/project-*.md` together. Verify full Git host/owner/repository identity, Jira site/key, conventions, templates, and reviewer identities; inspect repository tooling before treating sample commands as real checks. Resolve required Jira fields from current metadata when needed. Unknown optional facts should remain explicitly unknown; missing required facts block their dependent action.

Populate GitHub and Jira **MCP connection names from the connections actually configured in the client**. Inspect that client's MCP list/configuration and its exposed tools, then match the connection's verified host/site through metadata or a read-only result. The samples `github-work` and `jira-instance-a` are placeholders, not accounts setup creates. If names differ between your clients, record a clearly labeled client/machine mapping in the source profile; select the one verified in the active client. Never include credentials, create connections implicitly, or query another Jira site to discover where a ticket belongs.

Prefer remote repository identity: HTTPS/SSH spellings can normalize to the same project across Windows, macOS, and worktrees. Leave the optional exact local root unset unless an offline checkout needs it. If necessary, record explicitly labeled Windows/macOS exact Git roots in source; only the current machine's exact match may be used, and a conflicting known remote blocks fallback. Do not put one machine's checkout path into generic defaults or maintain installed profiles differently on each machine.

After a source profile changes, sync the private clone to each machine through your normal process, run setup and check there, then start a fresh project session. Installed profiles are never edited directly. The model should identify the selected profile and actual remote evidence on request; a file merely existing proves no loading.

To add a fourth project, copy a sample to `projects/project-d.md` in source, keep it UNCONFIGURED while replacing its facts, and add its unique identity/aliases and relative filename to the index. Verify and mark READY before live use, then rerun setup on each machine. No installer registry or interactive configuration framework is needed.

## Update and recover

Edit source and rerun setup. Refresh the app UI paste when its generated baseline changes. Start a fresh session after instruction/profile changes; `/skills reload` is available in the app. [App commands](https://docs.github.com/en/copilot/reference/github-copilot-app-reference/slash-commands)

| Exit code | Meaning |
| --- | --- |
| 0 | Install completed, or checked files and manifest match |
| 1 | Check found missing/outdated files or manifest entries |
| 2 | Conflict, migration required, invalid input/manifest, unsafe path, or I/O failure |

Check mode never writes. Setup preflights all destinations: content may be adopted/replaced only if absent, byte-identical to the desired result, or matching its last owned hash. A manifest records ownership; it is not a security signature. Even an installed newline-only edit counts as drift. An ownership conflict aborts before any generated file changes.

**Coexisting instructions** occupy different files and may all be supplied by the host. **Conflicting ownership** means different content at the same managed destination. Thus an unrelated Karpathy skill is preserved, but another `~/.copilot/skills/implementation/SKILL.md` blocks installation. A repository skill of that name is preserved and may shadow ours. Extra unowned files inside a skill directory are not deleted. Setup does not scan or resolve every host's discovery configuration.

For a conflict, compare the installed file with source, merge wanted content into the appropriate source owner, back up the installed file, and remove only that conflicting file before rerunning. If keeping an existing same-name skill instead, rename this workflow's source skill directory and frontmatter together and update its references before installation. Do not erase a whole skills/instructions directory or reset the manifest to bypass ownership.

Removed/renamed source files block both update and check. Back up the listed obsolete files and manifest, review their contents, remove only those obsolete files, remove only their entries from the manifest, then rerun. Empty directories are harmless. Removal is always an explicit maintainer step.

## Migration from personal-workflow

This version renames the support root and bridge to `engineering-workflow`, removes the two redundant baseline copies, and adds the `implementation` skill. Skill names already installed remain unchanged. Perform this once per machine, with Copilot sessions closed so old context is not reused:

1. Run the new setup or `--check`. If `.copilot/personal-workflow/install-manifest.json` exists, it stops before writes and identifies the old and new manifest paths. Back up that manifest and its recorded files outside active Copilot discovery directories. Preserve any local edits in source before cleanup.
2. Create `.copilot/engineering-workflow/` if absent and relocate **only** the old `install-manifest.json` to that directory, retaining every entry/hash. Do not rename or delete the whole old directory. If a new manifest already exists, compare and reconcile the two records and files first; never overwrite either blindly. Retain the old backup for recovery.
3. Run `python setup.py --check`. It lists obsolete paths. For this upgrade these include the old bridge, old support baseline/app copies, and old managed project/writing files. Inspect and remove only the listed obsolete files and their corresponding manifest entries. Retain entries for `.copilot/copilot-instructions.md` and `.copilot/skills/...`: their hashes authorize the update. Preserve every unrelated neighbor.
4. Rerun setup and check. A conflicting new destination or same-name implementation skill still blocks writes. If the old bridge survives without a manifest entry, setup reports it separately and requires explicit inspection/backup/removal before the new bridge can be installed.
5. Replace the old app UI paste with the full generated `.copilot/copilot-instructions.md`. Remove any manually attached old baseline from saved workflow prompts. Start fresh sessions and verify the new support paths and five skills.

If upgrading an even older VS Code adapter, the manifest may also list `.copilot/personal-workflow/vscode/personal-workflow.instructions.md` and `vscode-settings.json`; clean up only the reported owned files. If you previously added this workflow to `chat.instructionsFilesLocations`, remove just that old settings entry yourself, preserving other settings. Current setup writes no editor setting. Unrecorded copies in custom directories require human inspection; setup cannot certify all active context.

No automatic deletion or manifest relocation occurs. This conservative one-time migration keeps ownership evidence and prevents setup from reporting success with its recorded old instructions still active. If interrupted, continue from the relocated manifest and its remaining obsolete entries. Per-file writes are atomic, not a transaction: run one installer and avoid concurrent edits. Check and rerun the same source after an I/O interruption; inspect conflicts if source or installed content changed again. Failed ordinary writes clean up temporary siblings; a process kill or power loss may leave temporary files to inspect.

## Host permissions

Use the app's Interactive mode and inspect persistent grants/startup flags as well as session approval state. CLI and VS Code have different controls. [Compatibility and permission limits](copilot-compatibility.md#permissions-and-execution)

Before relying on external writes, inspect a pending intended tool call: its destination and payload must be visible, the host must pause, and denial must work. Do not approve a publication merely to test the prompt. If required details or the individual gate are unavailable, keep that mutation capability disabled. The [baseline policy](../instructions/baseline.md#external-action-policy) still requires a concrete preview and explicit conversational approval; host permission is a separate gate. Setup cannot validate live compliance.
