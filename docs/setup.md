# Configure, install, update, and remove

Keep this clone outside work repositories. Python 3.12 or newer and its standard library are sufficient. Setup does not change work repositories, MCP connections, editor settings, or repository instruction files.

## Configure a project

1. Copy `projects/project.example.md` to `projects/my-project.md`.
2. Replace the placeholders with verified project facts. Remove optional sections or fields that do not apply.
3. Set `Configuration status: READY`.
4. Repeat for any other projects, then run setup.

The identification section is intentionally small:

```markdown
## Routing

- Project: My Project
- Git remote: github.example.internal/team/repository
- Jira prefix: ABC
```

Use the name you naturally use for the project. The Git remote is `host/owner/repository`, without a URL scheme or credentials. Use `unset` for an inapplicable Git remote or Jira prefix, but keep at least one of them. An optional `- Local root: ...` may identify an offline checkout on this machine.

Put GitHub and Jira connection names and the Jira site under `## Connections`. Put default GitHub usernames under `## Pull requests`:

```markdown
## Pull requests

- Reviewers: reviewer-one, reviewer-two
```

PR preparation combines those names with applicable repository requirements, verifies eligibility when possible, excludes the author, removes duplicates, and shows the exact reviewer list before requesting approval.

Profiles should contain only facts that are private, hard to derive, or genuinely project-specific. Good examples are connection identities, reviewers, a private PR-title convention, a branch-naming convention, or a required acceptance-criteria convention. Leave repository commands, coding standards, generic templates, architecture, and live board fields to the repository and tools.

Profiles remain local and are ignored by Git. They are configuration, not credential storage.

## Install and check

Run from this clone:

```text
python setup.py
python setup.py --check
```

The first command installs or updates the workflow. The second verifies that installed content matches the source. A fresh install without READY profiles is valid for repository-only work; setup will report that project-dependent workflows are not configured.

If you use the Copilot app, paste the full generated personal instruction file into **Settings > Sessions > App instructions**. Setup cannot edit this UI field. Start a fresh session after installing or updating.

For a disposable test destination, use `python setup.py --home <directory>`. That option installs files there but does not make Copilot discover the alternate location.

Setup discovers direct `agents/*.agent.md` profiles and installs them to `.copilot/agents/` under the selected home. This is the documented personal Copilot CLI agent location. After installation, start a fresh CLI session and inspect its skills and agent picker; verify `eng-pr-review` and invoke each installed reviewer on a read-only fixture. Other clients need their own skill/agent discovery check. Missing delegated-agent support falls back to the main review skill. See [PR review](pr-review.md) for the workflow and [GitHub's CLI layout](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference) for discovery paths.

Internal reviewer names use the `pr-review-` prefix and CLI `infer: false` to prevent unrelated automatic selection. Check explicit named dispatch in the client you use; if it is unavailable with inference disabled, the parent handles the question. Supplementary Markdown under each skill, including nested `references/`, is installed recursively with rendered paths and normal ownership protection. The report writer is installed with the skill and needs Python 3.12+ only. Substantial reports are separate immutable runs under `engineering-workflow/reviews/<host>/<owner>/<repository>/pr-<number>/<head-sha>/`, so the same head can be reviewed again after discussion changes.

## Verify skill selection

For a normal request, Copilot may select a skill based on the prompt and its description. Explicit invocation is useful when you want a particular workflow, especially for consequential work; automatic selection is not guaranteed. Ordinary use does not require manual skill inspection. [Selection and invocation](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills#using-agent-skills)

The personal task skills use `eng-` names, including `/eng-planning`, `/eng-implementation`, `/eng-implementation-review`, `/eng-pr-review`, `/eng-review-context`, `/eng-prepare-pr`, and `/eng-jira-story`. Use these names for explicit invocation. No generic aliases are installed. CLI project skills take priority over duplicate personal names; the namespace avoids collisions with generic repository workflows but does not defeat an exact same-name project definition. [CLI skill precedence](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#skill-locations)

For troubleshooting or consequential planning/review, start a fresh session or run `/skills reload`, then `/skills info eng-planning` or `/skills info eng-pr-review`. Check that the selected path is the expected personal `~/.copilot/skills/eng-.../SKILL.md`. `copilot skill list --json` also exposes source/path/enabled state. Installation alone does not prove loading, and `/instructions` separately inspects combined instruction files. Other clients require their own discovery controls; this is not a ritual for every prompt. [Skill inspection](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)

For native CLI Plan mode, `/session plan` displays the session's active plan. The [planning workflow](planning.md) owns its relationship to explicitly requested repository plans and implementation authorization; setup does not manage either artifact.

## Inspect status

Run `python setup.py --status` for a human-readable overview of the source clone, installation location and state, installed guidance, dynamically discovered skill and agent counts/states, and READY projects. It also reports that Copilot app instructions are manual because setup cannot inspect whether the app currently loaded them.

Status is read-only and performs no installation, repair, deletion, or manifest update. It returns `0` when it can report the state, including not installed, update available, or local conflict. Invalid or unreadable source configuration or ownership data returns `2`.

Use `--check` for deterministic source-to-install comparison in automation. Check retains its existing exit behavior: `0` for a match, `1` for safe differences, and `2` for invalid data or conflicts. `--status`, `--check`, and `--uninstall` are mutually exclusive; `--home` works with each.

## Update

Update this source clone or edit its tracked guidance, then rerun:

```text
python setup.py
python setup.py --check
```

If the engineering defaults changed, refresh the manual Copilot app instructions as well. Existing local profiles are not updated from the template; apply useful template changes to them deliberately.

## Uninstall

Run:

```text
python setup.py --uninstall
```

Uninstall first checks every file recorded as belonging to this workflow. Missing files count as already removed. Unchanged managed files are removed, along with the workflow's ownership record. If any managed file has been edited or replaced, uninstall stops before removing anything and reports the conflict. Unrelated files and neighboring Copilot configuration are never removed.

Agent profiles and supplementary skill resources use the same ownership protection on install, update, check, stale cleanup, and uninstall. A locally modified active or stale managed agent blocks mutation; unrelated personal agents remain untouched. Runtime reports under `.copilot/engineering-workflow/reviews/` are user-owned, excluded from the manifest, and survive uninstall.

Renamed managed skills, resources and profiles use ordinary stale-file cleanup: setup removes an unchanged old destination and installs its current source name, without aliases. A locally edited old destination blocks the entire update until its changes are preserved and the conflict is resolved.

Setup cannot remove instructions pasted into the Copilot app. Clear that UI field manually after uninstalling if you used it for this workflow.

## Recover from a conflict

A conflict usually means an installed file was edited directly or another workflow already uses the same destination. Setup and uninstall stop before making partial changes.

1. Inspect the reported installed file and its source counterpart.
2. Copy any change you want to keep into this source repository or another safe location.
3. Remove only the reported installed file after preserving what matters.
4. Rerun the intended setup or uninstall command.

Do not delete whole Copilot configuration directories or edit the ownership record to force an operation. Unrelated instructions, skills, and settings may live beside this workflow.

For install and uninstall, exit code `0` means the operation completed. Invalid configuration, unsafe paths, conflicts, and I/O failures use `2`.

See [technical details](technical-details.md) for validation rules, installed paths, ownership behavior, and client compatibility.
