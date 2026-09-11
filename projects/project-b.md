# Project B — notification service

Configuration status: UNCONFIGURED

All values are illustrative. Replace identities and verify commands, templates, reviewers, and required Jira fields before setting READY. Do not contact example sites or execute these sample commands.

## Identity and connections

- Aliases: Project B, notifications, NST
- GitHub host/repository: github.com/example-company/notification-service
- GitHub MCP connection: github-work
- Optional exact local root: unset; prefer remote identity across machines.
- Jira MCP connection: jira-instance-b
- Jira site: https://jira-b.example.invalid
- Jira key prefix and project key: NST
- Jira project name: Notification Services
- Jira board: Notification team; numeric ID 202
- Board membership: confirm the board filter; no extra labels/components assumed.
- Issue type: Story; resolve its actual ID from this project's metadata.
- Required custom fields: unknown; inspect create metadata before drafting the final payload.

## PR conventions

- Base branch: develop
- Title: `<JIRA-KEY>: <imperative summary>`
- Default draft flag: false, only when the described work is ready; incomplete work requires an explicitly approved draft.
- Reviewers: default example-notification-reviewer; include example-api-reviewer when public schemas or delivery contracts change. These are placeholder GitHub logins. No team reviewers configured.
- Respect existing required repository template fields. The personal body format is:

```markdown
## Summary

<Concrete problem and resulting behavior.>

## Testing

<Checks actually run and results; state meaningful gaps.>

## Compatibility

<Evidence about affected consumers, or not applicable with a reason.>

## Ticket

<Full issue URL.>
```

## Jira story format

Title: concrete requested behavior.

```markdown
## Context

<Current behavior and the confirmed need.>

## Scope

<Requested behavior and known constraints.>

## Acceptance criteria

- Given <confirmed precondition>, when <action>, then <observable result>.
```

This project uses Given/When/Then; do not invent extra scenarios to fill the format. Leave priority, assignee, sprint, points, labels, and epic unset unless required by verified metadata or explicitly requested.

## Local checks and quirks

Verify these against package manifests, lockfiles, pyproject configuration, and Jenkins before use:

| Working directory | Candidate check |
| --- | --- |
| web | npm run lint |
| web | npm run typecheck |
| web | npx --no-install playwright test |
| api | python -m pytest |

Illustrative quirk to replace: notification delivery retries depend on stable idempotency keys. Inspect the persistence and consumer contracts before changing retry or deduplication behavior. No permission to contact real recipients or run Jenkins delivery stages is implied.
