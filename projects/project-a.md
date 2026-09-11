# Project A — checkout service

Configuration status: UNCONFIGURED

All values are illustrative. Replace identities and verify commands, templates, reviewers, and required Jira fields before setting READY. Do not contact example sites or execute these sample commands.

## Identity and connections

- Aliases: Project A, checkout, PCSU
- GitHub host/repository: github.com/example-company/checkout-service
- GitHub MCP connection: github-work
- Optional exact local root: unset; prefer remote identity across machines.
- Jira MCP connection: jira-instance-a
- Jira site: https://jira-a.example.invalid
- Jira key prefix and project key: PCSU
- Jira project name: Checkout Services
- Jira board: Checkout delivery; numeric ID 101
- Board membership: confirm the board filter; no extra labels/components assumed.
- Issue type: Story; resolve its actual ID from this project's metadata.
- Required custom fields: unknown; inspect create metadata before drafting the final payload.

## PR conventions

- Base branch: main
- Title: `[<JIRA-KEY>] <imperative summary>`
- Default draft flag: false, only when the described work is ready; incomplete work requires an explicitly approved draft.
- Reviewers: default example-backend-reviewer; frontend-only changes example-frontend-reviewer; mixed changes both. These are placeholder GitHub logins. No team reviewers configured.
- Respect existing required repository template fields. The personal body format is:

```markdown
## Change

<Concrete problem and resulting behavior.>

## Validation

<Checks actually run and results; state meaningful gaps.>

## Jira

<Full issue URL.>
```

## Jira story format

Title: imperative behavior change, without a redundant project prefix.

```markdown
## Problem

<Current behavior and why it needs to change.>

## Requested behavior

<Confirmed scope.>

## Acceptance criteria

- <Observable outcome derived from the confirmed requirement.>
```

Add constraints or exclusions only when known and relevant. Leave priority, assignee, sprint, points, labels, and epic unset unless required by verified metadata or explicitly requested.

## Local checks and quirks

Verify these against package manifests, lockfiles, pyproject configuration, and Jenkins before use:

| Working directory | Candidate check |
| --- | --- |
| frontend | pnpm lint |
| frontend | pnpm exec tsc --noEmit |
| frontend | pnpm exec playwright test |
| backend | python -m pytest |

Illustrative quirk to replace: order totals are represented in integer minor currency units at the API boundary. Verify this in schemas before relying on it. No permission to run deployment stages or integration tests against shared services is implied.
