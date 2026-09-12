# Engineering workflow for Copilot

This is a personal engineering workflow for GitHub Copilot. It keeps engineering behavior, private project context, repeatable workflows, and writing preferences consistent across repositories without requiring those repositories to contain your personal configuration.

It is designed for day-to-day software work where the repository and connected tools remain the source of truth. The workflow helps Copilot gather the right evidence, use specialized guidance only when it applies, and ask before it changes a shared or external system.

## What it helps with

- Grounding normal engineering questions and changes in the current repository.
- Planning substantial, ambiguous, or cross-cutting work.
- Implementing changes around the repository's existing contracts and responsibilities.
- Reviewing a meaningful implementation pass before treating it as complete.
- Preparing Jira stories from current project requirements.
- Preparing pull requests, including appropriate reviewers.
- Catching up on an existing PR's review discussion and relevant Jira history without changing either system.
- Applying private per-project GitHub, Jira, reviewer, and convention facts.
- Keeping plans, reviews, PRs, Jira stories, and other engineering prose in a consistent voice.
- Requiring an exact preview and explicit approval before consequential external changes such as creating an issue or PR, requesting reviewers, pushing, merging, or posting a review.

## How it works

General engineering guidance applies across repositories. When a task needs a focused workflow, Copilot loads the matching skill. When a task depends on a configured project, it identifies that project and reads only its private profile. Meaningful prose also uses the writing style and the example for that kind of output.

The repository, its own instructions, and current GitHub or Jira data still provide the facts. Personal configuration supplements that evidence; it does not replace it. See [DESIGN.md](DESIGN.md) for the conceptual model.

## Configure and install

Python 3.12 or newer is the only installer dependency.

1. Copy `projects/project.example.md` to a local profile such as `projects/my-project.md`.
2. Fill in the project-specific values and set `Configuration status: READY`.
3. Run:

```text
python setup.py
python setup.py --check
```

4. If you use the Copilot app, complete its manual app-instructions step described in [the setup guide](docs/setup.md#install-and-check).

You may install without a READY profile for repository-only work, then add project configuration later. Profiles are local and ignored by Git. Do not store credentials in them.

## Customize the workflow

If Copilot keeps doing something you dislike, change the owner of that behavior and rerun setup.

| If you want to change... | Edit... |
| --- | --- |
| General engineering judgment | [`instructions/baseline.md`](instructions/baseline.md) |
| How planning works | [`skills/planning/SKILL.md`](skills/planning/SKILL.md) |
| How implementation works | [`skills/implementation/SKILL.md`](skills/implementation/SKILL.md) |
| Implementation self-review | [`skills/implementation-review/SKILL.md`](skills/implementation-review/SKILL.md) |
| PR preparation | [`skills/prepare-pr/SKILL.md`](skills/prepare-pr/SKILL.md) |
| Jira story preparation | [`skills/jira-story/SKILL.md`](skills/jira-story/SKILL.md) |
| PR and Jira review catch-up | [`skills/review-context/SKILL.md`](skills/review-context/SKILL.md) |
| Tone or writing voice | [`writing/style.md`](writing/style.md) and its [matching example](writing/style.md#examples) |
| GitHub, Jira, or reviewer facts for one project | That local file under `projects/` |
| Installation behavior | [`setup.py`](setup.py) and [the setup guide](docs/setup.md) |

Work repositories can keep their own repository-specific instructions. Avoid duplicating the same generic guidance in both places.

## Updating or removing it

Edit or update this source clone, then run `python setup.py` and `python setup.py --check` again. Start a fresh Copilot session so it sees the updated files.

To remove the installed workflow:

```text
python setup.py --uninstall
```

Uninstall removes only unchanged files previously installed by this workflow. It stops without removing anything if managed content was edited locally, and it preserves unrelated Copilot configuration. If you pasted instructions into the Copilot app, clear those manually afterward.

See [setup and troubleshooting](docs/setup.md) for operations and [technical details](docs/technical-details.md) for installed layout, compatibility, ownership, and validation internals.
