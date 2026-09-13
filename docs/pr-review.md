# PR review

The [pr-review skill](../skills/pr-review/SKILL.md) reviews an existing PR against a pinned repository, base, and head. It establishes supported behavior, follows affected contracts, reconciles current review discussion, and recommends a review disposition. It supports first reviews and later rounds without duplicating existing comments. Review is read-only for contributor code and external systems. A focused review can finish in chat with zero custom subagents.

```text
Pin exact review target
        |
Understand change + early intent evidence
        |
Behavior gate: PASS / FAIL / UNRESOLVED
        |
Proportional depth + lightweight impact scan
        |
        +-- Evidence warrants deeper work?
        |       -> behavior modeling + impact tracing
        |       -> selective independent review work
        |       -> re-evaluate behavior gate
        |
Candidate findings -> falsification / counter-evidence
        |
VERIFIED / CONDITIONAL / REJECTED -> severity
        |
Accepted findings -> late review-state reconciliation
        |
Recommended disposition + proportional output
        |
Private substantial report as an immutable review run
        |
When preparing submission: summary + comments + thread replies
        |
Exact preview -> explicit approval -> publish -> verify
```

## Behavior and review depth

The skill separates requested behavior, discussion claims, repository obligations, observed code behavior, inference, and ambiguity. Neither Jira, the PR description, current code, nor submitted tests alone establish intent. Early discussion is used only for material intent, scope, rollout or contract clarification. Technical opinions stay out of neutral specialist packets. After independent acceptance, current discussion is reconciled for review state and duplicate prevention. [Review context](../skills/review-context/SKILL.md) reconstructs substantial history when needed; ordinary reviews need only minimum current state, without a verbose catch-up first.

Before investing in implementation polish, the parent assesses the relevant behavior proposition:

- **PASS:** evidence establishes intended behavior or behavior-preserving equivalence.
- **FAIL:** a reachable defect or regression produces Blocking candidates; further investigation establishes material scope and related correctness problems.
- **UNRESOLVED:** a material premise remains unknown. Static review can continue, with no claim that behavior was verified.

Later evidence can change the gate. An initial PASS does not constrain an independent reviewer or the final result.

A focused review stops after behavior, local conventions/consumers, and focused verification establish the result with no material expansion signal. Broader contracts, schema changes, deployment orchestration, interacting states, consequential design, weak tests, conflicting intent, or resolvable uncertainty earn deeper work. Decision tables, behavioral partitions, truth tables, state transitions, and counterexamples help with enums, absent/null/value inputs, permissions, boundaries, and historical/latest-state rules; simple changes need no matrix.

## Impact follows responsibility

Every meaningful review asks what contract changed, who consumes it, and what outside the diff could defeat isolation. The parent owns this analysis even when a specialist follows a bounded lead.

| Change | Evidence normally worth tracing |
| --- | --- |
| Metadata/config | Changed value, equivalent neighbors, obvious parser/consumer constraint. |
| Local logic | Old/new semantics, callers/state assumptions, focused regressions. |
| Schema/data | Migration, model, queries/raw SQL, API, jobs/scripts, fixtures and evidenced deployment effects. |
| Function/API contract | Owner, consumers, schema/errors, mocks/tests/jobs, established compatibility obligations. |
| CI/deployment | Shared orchestration, environment/artifact contracts, downstream jobs/services and rollout effects. |

Stop when inspected ownership and references make another affected contract unlikely and more traversal is unlikely to change the conclusion. Technologies guide evidence paths, not reviewer personas. Security, performance, concurrency/reliability, accessibility/UX, and operational safety receive attention when changed behavior implicates a concrete boundary or consequence.

## Selective independent perspectives

The parent prefers maintained built-in workers where their responsibility fits: `explore` for bounded consumer traces, `task` for inspected safe checks, and optional `code-review` for a generic defect sweep against an exact representable comparison. A worker inspecting local diffs needs a matching local/disposable checkout. None owns review policy or substitutes for contract reconstruction, impact ownership, test evidence, design assessment or history reconciliation.

The custom [correctness](../agents/pr-review-correctness.agent.md) perspective independently reconstructs domain contracts, state/enum and absent/null/value semantics, historical/latest-state rules and business counterexamples. [Design and simplicity](../agents/pr-review-design-simplicity.agent.md) assesses proportionate machinery and ownership; [test evidence](../agents/pr-review-test-evidence.agent.md) determines what behavior needs evidence and what the suite establishes. Built-in code-review and custom correctness do not run together by default; both need consequential complementary questions. There is no fixed swarm or agent requirement for substantial reviews.

Each receives pinned identity/code, source-distinguished requirement evidence, ambiguity, a neutral bounded question, impact leads, and a finding contract. The packet excludes the parent's gate result and desired verdict. Profiles carry their own compact review discipline and permit only file read/search. Current version-specific documentation, safe checks, and remote retrieval remain parent responsibilities.

Namespaced profiles use the documented CLI `infer: false` control to suppress unrelated automatic selection. The parent requests a named specialist explicitly when the client supports that dispatch; otherwise it covers the question itself without enabling inference. Profile discovery, selection and inference controls vary across surfaces, so setup success alone does not prove delegation support. See [technical details](technical-details.md#copilot-surfaces-and-other-instructions).

Test review can identify exact missing high-value scenarios. For a latest-state rule, older true followed by latest false distinguishes historical inclusion from latest inclusion; single-row true/false tests cannot. An untested consequential action/absent-input combination can likewise merit a finding. Missing tests alone do not prove implementation defects, and branch/line coverage is not a quota.

For Blocking findings or consequential conclusions dependent on nontrivial inference, an independent challenger seeks counter-evidence when isolated investigation can materially test the result. The current `rubber-duck` built-in or another appropriate independent perspective can serve this role. Direct evidence can settle a finding without delegation; agreement is not proof. Conditional security analysis can use the read-only built-in `security-review` when appropriate. See [GitHub's built-in agent documentation](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents).

Rubber-duck can also attack a substantial final behavior/impact model when useful. Built-in confidence/severity output remains candidate input for the parent's evidence and impact rules. General-purpose has no routine role; the parent already owns broad reasoning. The manual `/research` workflow is not an automatic dependency. Current documentation lookup stays with the parent. Planning and implementation do not need redundant mandatory critic calls merely for symmetry.

## Review rounds and existing threads

For re-review, establish the best-supported previous reviewed revision from actual review submissions, reviewer identity and commit evidence. Authenticated viewer identity distinguishes the user's reviews only when available. Missing fields or a rewritten branch do not justify guessing a baseline. Review the new delta, then re-expand contracts where it interacts with unchanged code or invalidates prior conclusions; the current head always gets its own behavior gate.

After independent technical acceptance, compare current findings with submissions, threads, replies, resolved state, outdated anchors and earlier rounds. Substantial history can reuse review-context. Earlier material concerns are revalidated as addressed, partially addressed, still applies, superseded, or unable to establish. Replies and resolved threads are discussion evidence, not proof of a code fix; outdated anchors do not prove the issue disappeared. New evidence can revise both acceptance and the gate.

A valid finding remains in the technical assessment even when someone else already raised it. Usually it needs no additional comment. A reply is useful when it adds a reproduction, current-head confirmation, affected consumer or consequential clarification; no ceremonial +1 replies. Prior concerns that still apply or are only partly fixed normally use the existing thread. Verified fixes are not criticized again and may be acknowledged in the summary. New independent findings receive new inline comments, or a review-level concern when no truthful inline anchor exists. Incomplete discussion retrieval limits duplicate checking; it does not silently turn every candidate into a known-new comment.

## Current disposition

The skill recommends **APPROVE**, **COMMENT**, or **REQUEST CHANGES** after reconciling current findings and discussion. Request changes fits verified merge-unsafe behavior, normally Blocking. Uncertainty warrants it only when that unresolved premise itself prevents safe merge, not merely because the reviewer's environment is unavailable. Comment fits material discussion without an established blocker. Approve fits a current review without blockers or material unresolved concerns that make approval irresponsible; evidenced Suggestions may coexist with it. Actual team policy can affect the judgment, but finding counts and invented policy cannot.

An existing open thread still contributes its verified consequence to the recommendation. A previous Request changes can become Approve after the relevant fix and current review scope are verified. The recommendation never submits a GitHub review.

## Findings and output

Candidates carry a factual issue, evidenced contract, inspected evidence, trigger/consequence, truthful primary anchor, supporting locations, counter-check, severity recommendation, and material gap. The parent tries to falsify each candidate, including its own: another layer may handle it, a path may be unreachable, a contract may be unevidenced, framework semantics may differ, or the proposed alternative may break a constraint.

Only **VERIFIED** candidates enter Findings. Consequential **CONDITIONAL** concerns appear separately with the missing premise. **REJECTED** candidates disappear. Cross-file findings anchor the changed code introducing the issue and cite affected consumers as supporting evidence. Use a changed symbol when line information is unreliable, or an explicit review-level concern when no sensible inline location exists; never invent an inline anchor.

Severity describes impact: **Blocking** means established incorrect behavior or an unsafe merge; **Important** means a material engineering or evidence issue deserves consideration even if behavior works; **Suggestion** means an evidenced benefit while behavior remains sound. All levels need evidence. Confidence, agreement, and fix difficulty do not set severity. Keep every independent accepted finding; zero findings is valid.

A focused review returns all findings or a concrete no-material-findings statement naming checked behavior and impact evidence, with the recommended disposition. FAIL and UNRESOLVED are explicit. It creates no unsolicited artifact or submission-package ceremony.

A substantial technical report contains repository/PR, reviewed-at UTC timestamp, pinned SHAs, evidenced prior reviewed head when applicable, gate/explanation, concise coverage, and all accepted findings with anchors/supporting evidence. It records relevant history reconciliation, findings already covered by threads, and recommended disposition. Include conditional concerns and material gaps only when present. Omit raw reasoning, transcripts, rejected candidates, copied issue descriptions, diaries and generic praise.

The complete report is persisted outside the reviewed repository at `~/.copilot/engineering-workflow/reviews/<host>/<owner>/<repository>/pr-<number>/<head-sha>/<review-run-id>.md`. Each immutable run uses a UTC timestamp with a deterministic suffix if timestamps collide. New discussion or evidence can therefore produce another report on the same head. The skill's report writer validates identity and containment, refuses links/junctions/redirection, creates exclusively without overwriting, normalizes UTF-8/LF and reads back exact bytes. Any failure leaves the complete result in chat with the failure disclosed. Reports are user-owned and survive uninstall.

If identity/base/head cannot be pinned, the skill stops before claiming a PR review. Missing Jira/discussion only limits conclusions that depend on it. A mismatched checkout cannot supply PR runtime evidence. Unavailable runtime or freshness evidence leaves useful static findings intact while material uncertainty stays visible. If delegation fails, the parent covers the question when possible and reports only material lost coverage. Partial work is never presented as comprehensive.

## Comment and publication boundary

Finding discovery and specialist records are style-independent. After acceptance and reconciliation, review summaries, inline comments and thread replies use the existing [writing style](../writing/style.md) and [review examples](../writing/examples/review.md). Substantial technical reports use summary calibration. Publication prose describes current readiness and main concerns naturally, acknowledges verified prior fixes when useful, and avoids repeating each inline comment. No synthetic finding IDs, raw specialist prose, unsupported praise or personal judgments enter that prose.

When preparing submission, the package contains the pinned target/head, recommended disposition, natural summary, new inline comments with complete bodies and anchors, replies with exact thread/comment targets and bodies, and findings needing no new comment. A clean package can contain only an Approve recommendation and short summary.

The parent inspects configured GitHub MCP schemas instead of assuming batch reviews, events, inline comments, replies or thread resolution exist. Unsupported actions remain accurate drafts with a stated limitation; a new top-level comment is not a substitute for an unavailable thread reply.

Review does not post, approve, request changes, resolve threads, edit a PR, or mutate Jira automatically. Requested publication uses the existing [baseline approval policy](../instructions/baseline.md#approval-for-external-changes): preview every intended review event/body, inline comment and reply across all required calls; obtain explicit approval; refresh head, anchors and thread state; execute; read back and verify. A changed head requires refreshed affected evidence/package and renewed approval. Material thread/payload changes are reconciled before writing. Uncertain or partial writes are reconciled before retrying to avoid duplicates.

See [setup](setup.md) for installation and client discovery, and [technical details](technical-details.md) for ownership and compatibility.
