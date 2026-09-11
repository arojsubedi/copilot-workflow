---
name: prepare-pr
description: Prepare and, after approval, create a pull request through the existing GitHub MCP connection. Use for PR preparation or creation requests, optionally with a Jira key. Inspect the actual branch and requirements, draft the full proposal, request approved reviewers, and verify the remote result.
---

# Prepare PR

Own preparation through verified PR creation and approved reviewer requests. A prepare-only request ends with a reviewable proposal until the user approves creation. Do not implement fixes, stage, commit, discard work, change branches, or publish incidentally.

## Resolve and inspect

1. Read `{{BASELINE_PATH}}` if its full text is absent from the visible context (read it if unsure); its External-action policy owns authorization. Read `{{WORKFLOW_ROOT}}/projects/index.md` and the one matching profile. Inspect the actual Git root, remotes, status, current branch, and HEAD; the session may use a worktree. Resolve identity conflicts, detached HEAD, merge conflicts, or UNCONFIGURED profiles before creation.
2. Match the profile's GitHub connection and host/repository to live metadata. Retrieve the supplied or project-required Jira story through the selected Jira MCP/site, checking the key against the project. Inspect actual tool schemas; use the existing MCP servers directly. A missing required story/connection permits a provisional draft, not an invented requirement or alternate-server search. Resolve the gap before creation, or obtain an explicit decision to create a draft with the limitation disclosed when project policy permits.
3. Select base from the user's explicit choice, then the profile, then verified repository metadata; surface conflicts with branch policy. Verify the branch exists. Inspect remote head/base and pin their SHAs. A scoped fetch may refresh tracking refs. Inspect commits and the full relevant three-dot diff from merge-base, including renames, binary changes, and submodules when present. Obtain sufficient history or state the comparison limitation. Validate refs and quote shell arguments; never interpolate issue text into commands.
4. Compare local HEAD with the intended remote PR head. Report unpushed commits and staged, unstaged, and untracked work separately; none is in the remote PR. Label an assessment using local changes as provisional until the intended commits are published. If a push is needed, preview its exact remote, branch, commits, and effects as a separate approved action. After that action, refresh the comparison and PR proposal. No implicit push or force-push.

## Assess and draft

Use current implementation assessment and verification evidence where it covers the pinned comparison, requirements, and relevant conditions. If missing or materially invalidated, use `implementation-review` for a bounded reassessment in review-only mode; tiny clear changes need focused checks. Read [implementation-review](../implementation-review/SKILL.md) if needed. This supplies engineering evidence, not exhaustive PR review or integration approval. Do not refactor during preparation. Unpublished fixes cannot prove the remote head. Carry findings, verification results, pending CI, remaining requested work, and material gaps into the proposal; completing an implementation pass does not establish that the PR's whole scope is complete.

Read `{{WORKFLOW_ROOT}}/writing/style.md` and its PR example file if present. Use the profile's title/body format and required repository template fields. Describe the final behavior and actual verification. Select reviewers from explicit profile mappings and repository requirements; verify identities/eligibility where available, exclude the author, and deduplicate. Do not invent substitutes.

Show the complete proposed action:

- GitHub connection, host/repository, and linked Jira issue/site if applicable.
- Head repository/branch/SHA, base branch, and compared base SHA.
- Exact title/body, draft status, all other fields, and proposed reviewers.
- Each proposed write, including reviewer requests if separate from creation.
- Requirement gaps, uncertainty, unpublished changes, and verification evidence.

Allow revision. Do not present incomplete behavior as ready; resolve material gaps or propose an explicitly approved draft with honest limitations.

## Mutation boundary: publish

Apply the baseline's External-action policy here. Obtain explicit approval of the complete current action set. Recheck the profile, local/remote head/base, and existing PRs for the same head/base. Refresh the assessment and preview when the comparison changes; renew approval for material changes. Do not silently update an existing PR when creation was approved.

Use GitHub MCP to create the approved PR, then request exactly the approved reviewers if this requires a separate call. Each write remains subject to per-call tool approval. Missing capabilities block that action; do not substitute shell publication.

Read back the PR and reviewer state. Verify repository, head/base, title/body, draft status, and requested reviewers. Report the URL and any partial success. If a write outcome is uncertain, reconcile it before retrying; do not create a duplicate. Do not merge, post comments/reviews, change Jira status, or enable automatic merge without separately previewed and approved actions.
