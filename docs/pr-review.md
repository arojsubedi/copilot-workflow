# PR review

The [pr-review skill](../skills/pr-review/SKILL.md) reviews an existing PR against a pinned repository, base, and head. It establishes supported behavior, follows affected contracts, and returns findings that survive a counter-check. Review is read-only for contributor code and external systems. A focused review can finish in chat with zero custom subagents.

```text
Pin exact review target
        |
Understand change + reconstruct supported behavior
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
Proportional output + private substantial report
        |
Accepted findings -> optional comment drafts
        |
Exact preview -> explicit approval -> publish -> verify
```

## Behavior and review depth

The skill separates requested behavior, discussion claims, repository obligations, observed code behavior, inference, and ambiguity. Neither Jira, the PR description, current code, nor submitted tests alone establish intent. [Review context](../skills/review-context/SKILL.md) supplies discussion/history only when it can clarify intent, resolution, or duplicate findings.

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

The parent can use [correctness](../agents/review-correctness.agent.md) to independently reconstruct consequential behavior and seek reachable counterexamples; [design and simplicity](../agents/review-design-simplicity.agent.md) to assess proportionate machinery and ownership; and [test evidence](../agents/review-test-evidence.agent.md) to determine what behavior needs evidence and what the suite establishes. There is no fixed swarm or agent requirement for substantial reviews.

Each receives pinned identity/code, source-distinguished requirement evidence, ambiguity, a neutral bounded question, impact leads, and a finding contract. The packet excludes the parent's gate result and desired verdict. Profiles carry their own compact review discipline and permit only file read/search. Current version-specific documentation, safe checks, and remote retrieval remain parent responsibilities.

Test review can identify exact missing high-value scenarios. For a latest-state rule, older true followed by latest false distinguishes historical inclusion from latest inclusion; single-row true/false tests cannot. An untested consequential action/absent-input combination can likewise merit a finding. Missing tests alone do not prove implementation defects, and branch/line coverage is not a quota.

For Blocking findings or consequential conclusions dependent on nontrivial inference, an independent challenger seeks counter-evidence when isolated investigation can materially test the result. The current `rubber-duck` built-in or another appropriate independent perspective can serve this role. Direct evidence can settle a finding without delegation; agreement is not proof. Conditional security analysis can use the read-only built-in `security-review` when appropriate. See [GitHub's built-in agent documentation](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents).

## Findings and output

Candidates carry a factual issue, evidenced contract, inspected evidence, trigger/consequence, truthful primary anchor, supporting locations, counter-check, severity recommendation, and material gap. The parent tries to falsify each candidate, including its own: another layer may handle it, a path may be unreachable, a contract may be unevidenced, framework semantics may differ, or the proposed alternative may break a constraint.

Only **VERIFIED** candidates enter Findings. Consequential **CONDITIONAL** concerns appear separately with the missing premise. **REJECTED** candidates disappear. Cross-file findings anchor the changed code introducing the issue and cite affected consumers as supporting evidence. Use a changed symbol when line information is unreliable, or an explicit review-level concern when no sensible inline location exists; never invent an inline anchor.

Severity describes impact: **Blocking** means established incorrect behavior or an unsafe merge; **Important** means a material engineering or evidence issue deserves consideration even if behavior works; **Suggestion** means an evidenced benefit while behavior remains sound. All levels need evidence. Confidence, agreement, and fix difficulty do not set severity. Keep every independent accepted finding; zero findings is valid.

A focused review returns all findings or a concrete no-material-findings statement naming checked behavior and impact evidence. FAIL and UNRESOLVED are explicit. It creates no unsolicited artifact.

A substantial report contains the repository/PR, pinned SHAs, gate and explanation, concise coverage, and all accepted findings grouped by severity with anchors/supporting evidence. Include conditional concerns and material verification gaps only when present. Coverage identifies behavior, contracts, warranted design/tests concerns, actual checks, and consequential unavailable evidence. Omit raw reasoning, transcripts, rejected candidates, copied issue descriptions, diaries, and generic praise.

The complete substantial report is persisted outside the reviewed repository at `~/.copilot/engineering-workflow/reviews/<host>/<owner>/<repository>/pr-<number>-<head-sha>.md` under the installed workflow root. Identity components and containment are validated; symlinks/junctions and unsafe paths are refused. Existing identical bytes can be reused, but different bytes are never overwritten. Creation is exclusive and read back for verification. Any persistence failure leaves the complete result in chat with the failure disclosed. These user-owned reports survive uninstall.

If identity/base/head cannot be pinned, the skill stops before claiming a PR review. Missing Jira/discussion only limits conclusions that depend on it. A mismatched checkout cannot supply PR runtime evidence. Unavailable runtime or freshness evidence leaves useful static findings intact while material uncertainty stays visible. If delegation fails, the parent covers the question when possible and reports only material lost coverage. Partial work is never presented as comprehensive.

## Comment and publication boundary

Finding discovery and specialist records are style-independent. Only accepted findings become optional PR-comment drafts using existing writing/review calibration; substantial reports use summary calibration. Drafts remain separate from technical findings.

Review does not post, approve, request changes, resolve threads, edit a PR, or mutate Jira automatically. A requested publication uses the existing [baseline approval policy](../instructions/baseline.md#approval-for-external-changes): exact connection/target, operation, commit/anchor and complete payload preview; explicit approval; execution; read-back verification. Material target or payload changes require a refreshed preview and approval.

See [setup](setup.md) for installation and client discovery, and [technical details](technical-details.md) for ownership and compatibility.
