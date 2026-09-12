# Project profile: `<PROJECT-NAME>`

Configuration status: UNCONFIGURED

Copy to `projects/<meaningful-name>.md`, replace placeholders, and add its filename and identity to local `projects/index.md`. Verify facts before setting READY. Do not contact example sites, select placeholder reviewers, or run placeholder commands. This template is not runtime context. Local profiles are ignored by Git; setup installs referenced profiles as generated copies. No credentials, tokens, passwords, or private keys belong here; authentication stays in the host/tool.

## Identity and connections

- Aliases: `<PROJECT-ALIAS>`, `<ANOTHER-ALIAS>`
- GitHub host/repository: `github.example.com/<org>/<repository>`
- GitHub MCP connection: `<github-mcp-connection>`
- Optional exact local root: unset; prefer remote identity. If needed, label exact Windows/macOS Git roots separately.
- Jira MCP connection: `<jira-mcp-connection>`
- Jira site: https://jira.example.com
- Jira key prefix and project key: ABC (replace with the verified key)
- Jira project name: `<JIRA-PROJECT-NAME>`
- Jira board: `<BOARD-NAME>`; numeric ID `<BOARD-ID>`, or unset if not applicable.
- Board membership: confirm the board filter; no extra labels/components assumed.
- Issue type: Story; resolve its actual ID from this project's metadata.
- Required custom fields: unknown; inspect create metadata and record required field names/IDs and verified handling before drafting the final payload.

## PR conventions

- Base branch: `<BASE-BRANCH>`
- Title: `[<JIRA-KEY>] <imperative summary>` (replace with the project's convention).
- Default draft flag: false, only when the described work is ready; incomplete work requires an explicitly approved draft. Verify this default for the project.
- Reviewers: `<DEFAULT-REVIEWER-LOGIN>`; for `<CHANGE-CONDITION>`, also request `<CONDITIONAL-REVIEWER-LOGIN>`. Replace with verified rules, including mixed changes; state any configured team reviewers explicitly or leave unset.
- Respect existing required repository template fields. Replace the personal body format as needed:

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

Replace with the project's format, such as Given/When/Then when required. Add constraints or exclusions only when known and relevant. Leave priority, assignee, sprint, points, labels, and epic unset unless required by verified metadata or explicitly requested.

## Local checks and quirks

Verify checks against package manifests, lockfiles, Python configuration, and CI before use; replace or remove each placeholder:

| Working directory | Verified check |
| --- | --- |
| `<RELATIVE-DIRECTORY>` | `<LINT-OR-TYPECHECK-COMMAND>` |
| `<RELATIVE-DIRECTORY>` | `<FOCUSED-TEST-COMMAND>` |

- Project constraints/quirks: `<VERIFIED-CONTRACT-OR-CONSTRAINT>`, with the code/schema location that establishes it, or none known.
- No permission to run deployment stages or integration tests against shared services is implied.
