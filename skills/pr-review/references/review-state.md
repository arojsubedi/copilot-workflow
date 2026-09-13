# Review state and later rounds

Use the [core review](../SKILL.md) for evidence, acceptance, severity and disposition. Read this procedure when prior reviews/threads need reconciliation or a later review baseline is needed.

## Establish the previous comparison

For a second or third review round, inspect available schemas for prior review submissions, reviewer identity, reviewed commit/head, prior inline comments, and later commits. Use authenticated viewer identity only when available; do not guess which reviews belong to the user. Establish the best-supported previous reviewed revision and source, not merely the last commit or report filename. Inspect the delta since that revision, re-expand contracts where it can invalidate earlier conclusions or interact with unchanged code, and run the behavior gate on the current pinned head. If the previous revision is unavailable or no longer an ancestor after a force-push, compare exact revisions where meaningful and disclose the limit; do not pretend a complete incremental review. Earlier material concerns are hypotheses to re-evaluate against current code, never verdicts to inherit. Defer their technical opinions until independent analysis where possible; a bounded regression check may use the old trigger and evidenced contract without supplying the old conclusion.

## Reconcile independently established results

After independent technical acceptance/rejection, retrieve current review submissions, threads/replies, resolution state, outdated/current anchors, reviewed commits and relevant earlier rounds through the configured GitHub schemas. Follow pagination far enough to compare all accepted findings with relevant existing discussion. Reuse [review-context](../../review-context/SKILL.md) for substantial reconstruction. If retrieval is incomplete, retain technical results and disclose duplicate-check coverage; do not draft a new inline comment as known-new until its relevant history is established.

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

