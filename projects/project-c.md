# Project C — reporting pipeline

Configuration status: UNCONFIGURED

All values are illustrative. Replace identities and verify commands, templates, reviewers, and required Jira fields before setting READY. Do not contact example sites or execute these sample commands.

## Identity and connections

- Aliases: Project C, reporting, DATA
- GitHub host/repository: github.com/example-company/reporting-pipeline
- GitHub MCP connection: github-work
- Optional exact local root: unset; prefer remote identity across machines.
- Jira MCP connection: jira-instance-a
- Jira site: https://jira-a.example.invalid
- Jira key prefix and project key: DATA
- Jira project name: Reporting Platform
- Jira board: Reporting delivery; numeric ID 303
- Board membership: confirm the board filter; no extra labels/components assumed.
- Issue type: Story; resolve its actual ID from this project's metadata.
- Required custom fields: unknown; inspect create metadata before drafting the final payload.

## PR conventions

- Base branch: main
- Title: `<JIRA-KEY> <imperative summary>`
- Default draft flag: false, only when the described work is ready; incomplete work requires an explicitly approved draft.
- Reviewers: default example-data-reviewer; add example-platform-reviewer for Docker or Jenkins changes. These are placeholder GitHub logins. No team reviewers configured.
- Respect existing required repository template fields. The personal body format is:

```markdown
## Change

<Concrete problem and resulting behavior.>

## Evidence

<Checks actually run, relevant dataset cases, and results.>

## Data impact

<Known schema/backfill/compatibility implications, or not applicable.>

## Jira

<Full issue URL.>
```

## Jira story format

Title: specific output or processing behavior.

```markdown
## Problem

<Current behavior and its effect on report users.>

## Expected result

<Confirmed output and scope.>

## Acceptance criteria

- <Observable result for a confirmed input case.>
```

Include dataset examples only when supplied or verified. Leave priority, assignee, sprint, points, labels, and epic unset unless required by verified metadata or explicitly requested.

## Local checks and quirks

Verify these against package manifests, lockfiles, pyproject configuration, and Jenkins before use:

| Working directory | Candidate check |
| --- | --- |
| repository root | python -m pytest |
| repository root | python -m ruff check . |
| ui | pnpm exec tsc --noEmit |

Illustrative quirks to replace: distinguish missing measurements from zero, and preserve timezone-aware event timestamps. Check dtype/schema expectations in the actual Pandas/NumPy pipeline. Production datasets, backfills, and shared databases require separately approved actions.
