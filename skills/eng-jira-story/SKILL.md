---
name: eng-jira-story
description: Draft or create one Jira story. Use for story preparation or creation, including for a named project; not for implementing an issue.
---

# Jira story

Own the outcome from rough requirement to a verified created issue. A draft-only request stops at the draft; a creation request continues through approval and execution. Do not create epics, modify existing issues, or implement code as incidental work.

## Resolve and understand

1. Read `{{BASELINE_PATH}}` if its full text is absent from the visible context (read it if unsure); it owns approval for external changes. Read `{{WORKFLOW_ROOT}}/projects/index.md` and only the selected profile. An explicit story target can differ from the checkout; never use another project's code as evidence. UNCONFIGURED profiles permit illustrative drafts only.
2. Match the profile's Jira MCP connection, site, and project to connection metadata or read results. Inspect the actual tool schemas; do not assume tool names. Use this existing MCP directly. If unavailable, report the gap and produce a provisional draft when useful; never substitute another Jira site or a shell write.
3. Inspect supplied requirements/issues and relevant code or related issues when they can resolve ambiguity or reveal a duplicate. Separate requested behavior, evidenced obligations, choices, assumptions, and suggestions. Code does not establish intent, and Jira wording does not prescribe architecture. For consequential contract changes, inspect available consumers and rollout constraints. Ask only unresolved decisions that affect the story.
4. Read create metadata and required fields for the project's story issue type (default Story). Resolve its ID live. If a board is specified, check its filter when accessible: issues belong to projects, and board inclusion follows the filter. Do not invent a board field, estimates, labels, sprint, acceptance criteria, or operational requirements.

## Draft and revise

Read `{{WORKFLOW_ROOT}}/writing/style.md` and its Jira example if present; apply the style's artifact-requirements rule, including any project-specific acceptance-criteria convention. Describe the confirmed need and behavior; keep speculative solutions and unresolved decisions outside the issue body.

Show one complete proposed action:

- Operation: create one story; Jira connection/site, project, issue type, and intended board if specified.
- Full title and description, including every acceptance criterion.
- All other fields to send, with names and IDs where required; distinguish explicit empty values from server defaults.
- Duplicate candidates, unresolved questions, and uncertain board inclusion outside the payload.

Revise the complete preview conversationally. Resolve required fields and consequential requirements before creation. Map the body to the connector's format without changing meaning or adding content.

## Mutation boundary: create

Apply the baseline's approval rules here. Obtain explicit approval of the complete current action. Recheck the selected profile, target, required fields, and approved payload; search for a likely duplicate if intervening activity makes creation uncertain. Material changes follow the baseline's renewal rule.

Call the configured Jira MCP to create exactly the approved issue. Do not add comments, links, transitions, epics, or other writes unless separately previewed and approved. Keep per-call tool approval enabled.

Read back the issue and verify its site, project, type, title, description, and explicit fields against the approved action, allowing only equivalent serialization. Report its key and URL. Distinguish creation success from verification failure. After an uncertain result, look for the created issue before any retry; if its status remains unknown, report that uncertainty and do not risk a duplicate.
