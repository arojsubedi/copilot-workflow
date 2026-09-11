# Project selection

This index selects the private profile for the active project. The assistant reads it because the baseline and workflow skills explicitly require it. All rows below are illustrative and must be replaced with real identities before use.

Maintainer: edit this index and profiles in the private source clone, then rerun setup on each machine. Setup may run with UNCONFIGURED samples for inspection; configure and verify a profile before live use, then mark it READY. Installed copies are generated. See `docs/setup.md` in the source repository for connection names, machine roots, and adding a project.

| Profile | Explicit names / aliases | Git host and repository | Jira prefix hint | Optional exact local root |
| --- | --- | --- | --- | --- |
| project-a.md | Project A; checkout; PCSU | github.com/example-company/checkout-service | PCSU | (unset) |
| project-b.md | Project B; notifications; NST | github.com/example-company/notification-service | NST | (unset) |
| project-c.md | Project C; reporting; DATA | github.com/example-company/reporting-pipeline | DATA | (unset) |

1. For code or PR work, inspect the actual session directory using `git rev-parse --show-toplevel` and `git remote -v`. Use the app's session worktree, which may differ from the original checkout. Compare full host/owner/repository identities, not folder names or substrings. Normalize HTTPS and SSH forms, remove a trailing `.git`, and ignore credential components. Resolve SSH host aliases with Git/SSH configuration when necessary. Never display embedded credentials.
2. A unique matching remote selects the profile. Multiple matching projects, an explicit project that conflicts with the repository, or a ticket prefix that conflicts with it require clarification. A prefix is a cross-check, never sufficient evidence to redirect a PR to another repo or Jira site. Do not query both Jira sites to find a ticket by trial and error.
3. If no remote matches, an exact configured local root may identify an offline checkout. If source lists labeled Windows/macOS roots, use only the current machine's entry. Normalize paths for the OS, compare the Git root (not a subdirectory), and resolve links. A known conflicting remote overrides this fallback and must be resolved. An unknown remote may be a fork; inspect its upstream or ask rather than inventing a mapping.
4. For a story explicitly requested for Project A while working in B, select A for the story and say so. Do not use B's code as A's evidence. Otherwise use the uniquely resolved current repo. Outside a repository, a unique explicit project alias is enough for story drafting. Ambiguous or missing identity means ask one targeted question.
5. Read exactly one profile relative to this index. Do not open the others. Re-read on a target change, after compaction if the selection evidence is missing, and before an approved write. Use a new session when moving between projects so old profile content is not retained in conversation history.

Profiles marked `UNCONFIGURED` permit illustrative drafts only. Do not contact their example hosts, run their sample commands, select their sample reviewers, or execute writes. Fill in the real facts and change the status to `READY` after checking them. Missing required facts block the dependent action, not unrelated local work.
