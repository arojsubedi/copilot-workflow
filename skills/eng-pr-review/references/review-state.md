# Review state and later rounds

Use the [core review](../SKILL.md) for evidence, acceptance, severity and disposition. Read this procedure when prior reviews/threads need reconciliation or a later review baseline is needed.

## Route the comparison from neutral metadata

The core's early probe routes the lifecycle, not technical judgment. Use current tool schemas for review submissions, author/viewer identity, reviewed commit, thread/history presence, and ordering. Do not retrieve full verdicts to classify a run. A user naming their prior review or explicitly requesting a later round supplies intent even if authenticated identity is unavailable; establish the actual revision separately. Never infer that another reviewer's submission belongs to the user.

| Evidenced state | Technical sequence |
| --- | --- |
| First review, no evidenced prior review by this reviewer | Analyze the current pinned PR comparison and close its material coverage. |
| First review with other reviewers' discussion | Perform independent first technical analysis; reconcile full comments/threads late for duplicates and additive replies. Other reviewers' threads alone do not establish re-review. |
| Re-review with a new head | Establish the best-supported prior reviewed revision; inspect its delta, re-expand affected unchanged contracts, and establish the current gate/coverage before reconciling old concerns. |
| Follow-up on the same head | Do not invent a code delta. Inspect new discussion/evidence, extract factual contract/trigger changes, revalidate affected current code and conclusions, then reconcile threads/disposition. |
| History unknown | Review current pinned code fully enough for the requested conclusion; disclose prior-baseline/history/deduplication limits and invent no previous revision. |

For a new-head re-review, choose the prior revision from an identified review submission or an explicitly identified prior local analysis, not merely the last commit. Check correspondence and ancestry. After force-push, if the old revision is unavailable or not an ancestor, compare exact revisions only where meaningful and disclose the incremental limit; review the current pinned PR surface sufficiently for the conclusion. A delta alone cannot establish whole-PR coverage. Reuse prior evidence only where its content, contracts, conditions and coverage remain valid; unresolved previous coverage cannot silently become closed.

For same-head follow-up, reuse still-valid technical evidence. If the earlier analysis itself is unavailable, the unchanged SHA supplies no reusable conclusions: inspect enough current code for the requested result. New facts may change the gate without a commit. Strip old opinions, severity and disposition from neutral worker packets; an independently evidenced contract and trigger may focus a regression check. Full concern reconciliation remains after current technical acceptance.

### Explicit follow-up using a private baseline

When the user explicitly requests re-review/follow-up and GitHub cannot establish the previous local analysis baseline, an existing immutable private report may supply technical context. Read only an identified report or a bounded candidate under the exact host/owner/repository/PR report directory; verify the identity, full base/head, timestamp and evidence inside it. A filename or most-recent timestamp alone cannot prove it is the intended baseline. Resolve consequential ambiguity rather than guessing, and do not scan unrelated projects or build an index.

Label its source as local prior analysis, never a submitted GitHub review or proof of publication. Extract neutral revision, contract/trigger and coverage evidence early; keep old finding prose and disposition out of independent packets. Inspect actual current code and remote evidence, which can defeat the report. Reports lacking usable evidence leave the baseline unresolved. Later apply normal reconciliation to prior local concerns while using actual GitHub threads for deduplication; a report cannot establish remote discussion state.

## Reconcile independently established results

After independent technical acceptance/rejection, retrieve current review submissions, threads/replies, resolution state, outdated/current anchors, reviewed commits and relevant earlier rounds through the configured GitHub schemas. Follow pagination far enough to compare all accepted findings with relevant existing discussion. Reuse [review-context](../../eng-review-context/SKILL.md) for substantial reconstruction. If retrieval is incomplete, retain technical results and disclose duplicate-check coverage; do not draft a new inline comment as known-new until its relevant history is established.

Compare issues by contract, trigger, consequence and current code, not identical wording or line numbers. Re-evaluate prior material concerns against the current head as addressed, partially addressed, still applies, superseded/no longer applicable, or unable to establish. A reply is not proof of a fix; a resolved thread is discussion state, not correctness evidence. An outdated anchor does not prove the underlying problem disappeared. Drop a prior verdict defeated by new evidence rather than preserving it for consistency. If this phase supplies new technical evidence, revisit candidate acceptance and the behavior gate before disposition.

Keep the technical finding separate from the publication action:

| Current relationship | Appropriate action |
| --- | --- |
| Genuinely new accepted issue | Draft a new inline comment at a truthful current changed-code anchor, or a review-level concern when none exists. |
| Same issue already covered by an open thread | Retain the technical finding and count its consequence in disposition; normally no new comment. |
| Prior concern still applies or is partially addressed | Prefer a follow-up in the existing thread, grounded in current-head evidence. |
| Related thread, materially additive evidence | Draft a reply with the reproduction, additional affected consumer, current-head confirmation or clarified consequence. |
| Prior concern addressed or superseded | Do not repeat the criticism; acknowledge the verified change naturally in the summary when useful. |
| Prior state cannot be established | Name the missing premise and avoid a duplicate or unsupported resolution claim. |

Do not manufacture +1 replies to create activity. Concise acknowledgment is useful only when it serves the user's review. Apply the same rule to another reviewer's finding and the user's earlier review. Do not delete a valid technical finding merely because another reviewer already raised it. Record exact thread/comment targets internally for useful replies. If reply capability is absent, preserve reply text and disclose the limitation; never substitute a duplicate inline or top-level comment. Do not resolve threads automatically.

