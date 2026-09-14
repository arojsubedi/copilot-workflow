# Prepare and publish a review

Read this procedure when drafting a review summary, inline comment or thread reply, or preparing/executing publication. The [core review](../SKILL.md) owns the recommendation and technical acceptance; complete any required [review-state reconciliation](review-state.md) first.

## Draft summary, comments and thread replies

Only after technical acceptance and history reconciliation, read `{{WORKFLOW_ROOT}}/writing/style.md` and `{{WORKFLOW_ROOT}}/writing/examples/review.md` to draft human-facing review prose. This calibration covers the review summary, inline comments and thread replies; technical investigation and specialist records remain style-independent. Do not paste a specialist response into a comment or turn Conditional concerns into established defects.

Use natural, proportional prose: communicate current readiness, mention main concerns without repeating each inline comment, and acknowledge verified prior fixes when useful. A clean approval may need only a short concrete summary. Do not mechanically copy examples, manufacture praise, claim comments were posted when only drafted, or expose internal labels such as B1, I2, AC1 or F7. Stable tool IDs belong in operation targets, never in the prose. Critique code/behavior, not the person; do not infer laziness, incompetence or AI use. State established defects directly, use uncertainty only when real, and ask questions when genuinely inviting discussion.

When the user is preparing to submit a review, assemble the applicable publication package:

- Current connection, repository, PR and pinned head; recommended APPROVE / COMMENT / REQUEST CHANGES.
- Proposed natural-language review summary.
- New inline comments with current path, line/range/side or supported truthful anchor and complete body.
- Thread replies with exact thread/comment target and complete body.
- Accepted findings requiring no new comment because discussion already covers them.

For a focused clean review this can be an Approve recommendation, short summary and no inline comments. Review-level concerns belong in the summary/body when no truthful inline location exists. Keep package mechanics and technical records separate from the publication prose.

## Preview, approve, publish and verify

Apply the baseline approval boundary referenced by the [core review](../SKILL.md). Its recommended disposition and accepted findings are inputs to this procedure, not permission to publish.

Inspect current configured GitHub MCP schemas before previewing actions. Do not assume batch submission, inline comments, replies, thread resolution or review events exist. Map the natural recommendation to the actual supported review event (for example REQUEST_CHANGES only if the schema defines it). If unsupported, preserve the accurate draft and state the limitation; do not simulate it with another operation or shell publication.

Preview the complete intended operation set: review submission event/body, each new inline comment, each thread reply and their exact target, payload and effects. If multiple calls are required, show them all before explicit approval for that exact package. Refresh current head, anchors and thread state immediately before execution. If head changed, stop, refresh affected evidence and the package, and obtain approval again. If another comment now covers the issue or a thread/anchor changed materially, reconcile and renew the affected preview/approval instead of publishing stale duplicates.

Execute only approved operations, then read back the review state, body, inline anchors and replies. Report partial success accurately. Reconcile an uncertain write before retrying; do not duplicate a review/comment after an ambiguous response. Tool availability, silence or another agent is not an approval bypass.
