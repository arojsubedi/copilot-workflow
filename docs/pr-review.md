# PR review

The [pr-review skill](../skills/pr-review/SKILL.md) assesses an existing PR against a pinned repository, base and head. It establishes supported behavior, accounts for the material change surface, follows affected contracts and reconciles current discussion before recommending a review disposition. Contributor code and external systems remain unchanged. A focused review can finish in chat with zero custom subagents.

```text
Pin exact target + establish trust
        |
Understand intent + map material change
        |
Behavior gate: PASS / FAIL / UNRESOLVED
        |
Impact tracing + proportional depth
        +-- conditional behavior/transition analysis
        +-- selective independent workers
        |
Coverage closure -> continue or disclose partial review
        |
Falsify candidates -> acceptance + parent severity
        |
Late review-state reconciliation
        |
Current disposition + proportional output
        +-- substantial: immutable private report
        +-- preparing submission: summary/comments/replies
                |
        Exact preview -> explicit approval -> refresh/write/read back
```

## Behavior, impact and coverage

The parent distinguishes requested behavior, discussion claims, repository obligations, observed code/test behavior, inference and ambiguity. Jira, the PR description and submitted tests are each evidence, not automatic truth. Early discussion supplies material intent and contract clarification. Reviewer conclusions enter later, after independent technical acceptance; new technical evidence can still change the judgment.

A semantic change map groups meaningful responsibilities rather than counting files or lines. Every material hunk belongs to an understood behavior/contract, supporting implementation, test/evidence, checked derived artifact or evidenced irrelevant area. Unexplained or unavailable material content stays visible. Deletions, omitted configuration and changed defaults count: the parent asks what stopped happening and which contract depended on it. Scope coherence matters when unrelated work causes concrete additional regression risk or confused ownership, not merely because a PR is large.

The behavior gate is **PASS**, **FAIL** or **UNRESOLVED**, assessed before design polish and revisited with new evidence. Matrices, partitions and counterexamples help with interacting states, enums, absent/null/value semantics or historical/latest-state rules; simple changes need no table. Passing tests cannot establish a contract they do not distinguish. Behavior and engineering quality remain separate judgments.

Every meaningful review traces the changed responsibility to relevant owners and consumers. Data changes can implicate models, raw SQL, APIs, jobs and deployment; API changes can implicate callers, schemas and mocks; orchestration changes can affect downstream services. Available read-only semantic navigation strengthens definitions, references, implementations and call tracing. Textual search remains necessary for SQL, dynamic names, configuration, serialization and external consumers; stale or incomplete indexes cannot prove isolation. Neither language-server installation nor a new reviewer is required. [GitHub's LSP support](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/lsp-servers)

Persistent state, destructive changes, external side effects, retries/jobs and deployment can require transition analysis: mixed versions, migration order, partial success, transaction boundaries, crashes, duplicate effects, cleanup and restart/replay. Findings need an evidenced reachable intermediate state. Rollback, mixed-version and idempotency obligations are not invented where the environment excludes them.

Before a substantial review claims completeness, the parent closes coverage across all material change units and consequential contracts, including deletions and skipped areas. Clean bounded worker results do not establish whole-PR coverage. Missing material coverage requires further investigation or an explicit partial-review limitation; it cannot become overall PASS, an unqualified clean verdict or APPROVE. A proven defect still establishes FAIL alongside a separate coverage gap. Tiny focused reviews keep this accounting implicit.

## Execution and instruction trust

Useful test/build commands can execute reviewed code. The parent inspects entry points, consequential invoked code/hooks, effects and access before choosing trusted local execution, suitable isolation, pinned CI evidence or static reasoning. A disposable checkout establishes correspondence, not process isolation. Unknown scripts, arbitrary review-only package installs, repository shell configuration and unnecessary credential/network access are not accepted merely to obtain a test result. Unsafe or unavailable verification limits only the conclusions that depend on it.

Sandbox guarantees depend on the actual client, enabled state and effective filesystem/network/credential policy. The workflow neither manages a sandbox nor assumes one is enabled. GitHub documents local sandboxing as optional and experimental; network and Git authentication can remain available, and built-in file tools apply policy in-process rather than under OS isolation. Check current support and policy before relying on it. [Sandbox behavior](https://docs.github.com/en/copilot/concepts/about-cloud-and-local-sandboxes), [sandbox configuration](https://docs.github.com/en/copilot/how-tos/cloud-and-local-sandboxes/configuring-local-sandbox-settings)

PR/Jira text, comments, docs, tests, data and committed prompts are reviewed content. They may evidence intended behavior; they cannot redefine review methodology, severity, execution permission or publication approval. Changed review-governing instructions, skills, agents, imported guidance, hooks and MCP/LSP configuration are high-interest change surface. Executable configuration also needs inspection before a client can start it. Normal imperative prose is not itself a defect.

The intended trust boundary is not hard instruction isolation. Copilot CLI combines applicable personal and repository instructions without a general precedence guarantee. Use verified personal resources and inspect actual loaded definitions; when conflicting branch configuration cannot be excluded, inspect exact content from a trusted context or disclose the limitation. Setup never changes work-repository instructions. [CLI instruction loading](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions), [hook execution](https://docs.github.com/en/copilot/reference/hooks-reference)

## Selective workers and parent judgment

Prefer maintained built-ins where their responsibility fits: `explore` for bounded evidence/consumer tracing with available code intelligence, `task` for inspected safe checks, optional `code-review` for a generic defect sweep, `rubber-duck` for consequential counter-evidence and `security-review` for credible security boundaries. Local-diff workers require an exact matching checkout. General-purpose has no routine role, and manual `/research` is not an automatic dependency. No roster must execute. [GitHub's built-in agents](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents)

Custom [correctness](../agents/pr-review-correctness.agent.md) independently reconstructs domain contracts and behavioral counterexamples; [design/simplicity](../agents/pr-review-design-simplicity.agent.md) assesses machinery, ownership and evidenced alternatives; [test evidence](../agents/pr-review-test-evidence.agent.md) determines what tests establish and which consequential regression scenarios are missing. Generic code-review and custom correctness run together only for consequential complementary questions.

Profiles remain namespaced, read/search-only and `infer: false`. Explicit dispatch depends on the client; if unavailable, the parent covers the question and discloses material lost independence. Each neutral packet contains pinned evidence, source distinctions, a bounded question and coverage scope, without the parent's verdict. Specialists return factual candidates, anchors, consequence, counter-evidence, evidence gaps and **VERIFIED / CONDITIONAL / REJECTED** recommendations. They do not recommend severity or produce polished comments.

The parent falsifies candidates against complete impact and current evidence. Only VERIFIED findings are accepted; consequential Conditional concerns stay separate and Rejected candidates disappear. The parent alone assigns **Blocking**, **Important** or **Suggestion** by consequence. Built-in confidence/severity never bypasses that judgment. Every level needs evidence, all independent accepted findings remain, and zero findings is valid. Cross-file findings anchor the changed cause with consumers as support; no invented inline anchors, finding quotas or model voting.

## Conditional resources and review output

One user-facing skill owns the engine, severity and disposition. Its internal procedures are read only when needed; their contents are not assumed loaded:

| Resource | Trigger and responsibility |
| --- | --- |
| [review-state.md](../skills/pr-review/references/review-state.md) | Later rounds, existing threads or substantial history: previous baseline, current-head revalidation and duplicate suppression. |
| [publication.md](../skills/pr-review/references/publication.md) | Drafting/submitting summaries, inline comments and replies: writing calibration, exact operations, refresh and readback. |
| [reporting.md](../skills/pr-review/references/reporting.md) | Substantial or requested private reports: complete current state and immutable persistence. |

Supplementary Markdown and scripts are supported skill resources. Discovery does not prove that the applicable procedure was read. [GitHub's skill resource support](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)

Re-review establishes an evidenced prior revision and reviewer identity where available, inspects the delta and re-expands affected unchanged contracts. It reruns the current behavior gate and coverage closure. [Review context](../skills/review-context/SKILL.md) reconstructs substantial discussion without becoming the technical review. Replies, resolved threads and outdated anchors are discussion state, not proof of a fix. Valid already-threaded findings still affect disposition but usually need no new comment; replies need additive value. Verified fixes are not criticized again.

The current recommendation is **REQUEST CHANGES** for merge-unsafe behavior, **COMMENT** for consequential discussion or partial review without an established blocker, or **APPROVE** when material coverage is closed and no blocker/material unresolved concern makes approval irresponsible. Actual team policy can matter; counts, prior verdicts and the reviewer's unavailable environment do not set disposition automatically.

Focused output is concise chat without unsolicited artifacts or submission ceremony. Substantial reports include target/UTC timestamp, base/head, evidenced prior head, behavior gate, coverage closure/gaps, findings, concise history reconciliation and disposition. Reports use summary calibration and preserve complete current evidence without diaries, copied threads or raw transcripts. The installed report writer creates immutable UTC runs at `reviews/<host>/<owner>/<repository>/pr-<number>/<head-sha>/<review-run-id>.md` under the private workflow root, outside the reviewed repository, with collision suffixes, safe paths and exact UTF-8/LF readback. Reports remain user-owned through uninstall; failures retain the full result in chat.

Review summaries, comments and replies use the existing [style](../writing/style.md) and [review examples](../writing/examples/review.md), without synthetic IDs or raw specialist prose. Publication requires the baseline's exact approved package of supported operations, refreshed head/anchors/thread state, and readback. Unsupported replies/events remain drafts rather than semantically different posts; changed targets or material payloads need renewed approval, and uncertain writes are reconciled before retrying. Nothing is automatically published or resolved.

[Quality cases](../tests/review-quality-cases.md) own semantic evaluation and built-in/custom comparisons; automated tests establish installation/content contracts, not model review quality. See [setup](setup.md) and [technical details](technical-details.md) for installation and runtime mechanics.
