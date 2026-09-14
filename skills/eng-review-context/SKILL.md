---
name: eng-review-context
description: Summarize an existing PR's intent and discussion, including linked Jira context when relevant. Use for PR review catch-up; read-only and not a code review.
---

# Review context

Help the user understand an existing pull request before or during code review. This workflow is read-only. It does not judge the whole change, implement fixes, publish comments or reviews, resolve threads, request reviewers, edit the PR, change Jira, transition an issue, stage, commit, push, or merge.

Read `{{BASELINE_PATH}}` if its full text is absent from visible context. Use the existing project-selection process: read `{{WORKFLOW_ROOT}}/projects/index.md`, identify the repository from the explicit target and current Git evidence, then read only the matching profile. Reuse relevant context already available rather than retrieving it again.

## Gather current evidence

Inspect the available MCP schemas instead of assuming tool names. Through the selected project's configured GitHub connection, retrieve the current PR metadata and body, review threads and replies, general comments, and review states where useful.

Follow pagination far enough to reconstruct the complete relevant discussion. Do not summarize only the first page of comments when later replies, thread state, or review activity could materially change the meaning.

Follow a Jira reference only when the PR title, body, branch, commit information, or discussion provides evidence for the link. Use only the selected profile's Jira connection and site. Retrieve the issue title, description, relevant comments, and status or fields only where they clarify intent or how the discussion evolved. Do not probe other Jira servers or infer a link from similar subject matter.

Use timestamps and thread order internally so older concerns are interpreted in light of later replies and revisions.

Distinguish:

- **Resolved**: the source explicitly marks the review thread resolved.
- **Appears addressed**: later discussion or implementation evidence appears to address the concern, but no explicit resolution is visible.
- **Open**: the concern remains active, unanswered, disputed, or otherwise unresolved in the available evidence.

A reply alone does not establish resolution.

When understanding a thread materially depends on a referenced code path, inspect only the relevant current code or diff if available. Do not expand this into a full code review.

## Reconstruct the discussion

Start with the PR's purpose, then group related comments and replies by concern rather than retelling every message.

Prioritize discussion that materially affects:

- requested behavior
- correctness
- architecture or ownership
- testing
- rollout or operational behavior
- review readiness

Compress resolved nits and repetitive exchanges while retaining material unresolved concerns. Keep distinct topics separate. Preserve attribution when it changes meaning or is necessary to understand how the discussion evolved.

Maintain these evidence distinctions while reasoning:

- A participant's comment is a **discussion claim** until independently established.
- Inspected code or diff is an **observed implementation fact**.
- A conclusion that combines evidence is an **inference** and should be phrased accordingly.

These are evidence rules, not mandatory output headings.

Never silently turn a participant's claim into a code or system fact. Do not infer attitudes, motives, consensus, or team decisions that the conversation does not establish.

If Jira and PR sources differ, preserve the distinction and attribution rather than merging them into one requirement. For example, an original Jira description, a later Jira clarification, and the current PR may legitimately represent different points in the evolution of the work.

## Present the catch-up

Keep the output proportional and scan-friendly.

A small PR with one discussion may need only a short explanation.

A larger discussion may use sections such as:

- **What the PR is doing**
- **Discussion so far**
- **Resolved or addressed**
- **Still open**

Use only sections that contain useful information. Do not manufacture an open-items section when nothing material remains unresolved.

Preserve chronology only where it changes the interpretation of a concern. Do not dump timestamps or reproduce comments message by message.

For substantial summaries, read `{{WORKFLOW_ROOT}}/writing/style.md` and its summary example if present.

Surface material open questions, unresolved concerns, conflicting source statements, or uncertainty when they exist.

If the user asks to take action based on the discussion, treat that as a separate request and route it to the appropriate implementation, PR, Jira, or review workflow with its normal authorization rules.
