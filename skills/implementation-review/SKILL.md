---
name: implementation-review
description: Review a meaningful nontrivial implementation pass for grounded behavior, ownership, proportionate complexity, test value, and verification gaps before continuing or finishing the pass. Revisit materially invalidated conclusions as work evolves. Also use for requested implementation self-review; tiny clear edits need only focused checks.
---

# Implementation review

Decide whether the current implementation is a grounded, correct, proportionate solution with enough evidence to continue or finish this pass. Use after a meaningful implementation pass, not after every edit. This is iterative engineering self-review, not exhaustive PR review, specialist audit, or release certification. Do not spawn specialist reviewers or expand into a repository-wide audit.

Read `{{BASELINE_PATH}}` if its full text is absent from the visible context (read it if unsure). It owns engineering defaults and the single External-action policy. Use the applicable repository guidance and, when identity or private conventions matter, `{{WORKFLOW_ROOT}}/projects/index.md` and its selected profile. Reuse context already read and current.

## Bound this pass

Use the requested behavior, current changes, relevant contracts, and any still-valid earlier assessment. Establish what this pass must deliver and what remains in the broader task; do not redefine the pass to excuse a missing obligation or claim the whole request is complete. Identify the before-state or comparison, current content, and included working-tree changes. Distinguish unpublished work when relevant. With no Git history, use an available before-state and disclose comparison limits.

Read the pass's relevant diff and affected context. Revisit prior findings or checks only where changed code, contracts, environment, or new evidence can invalidate them; a new commit SHA alone is not a reason to rerun everything. Conversely, an unchanged hunk is not proof that callers or assumptions stayed valid. Do not restart a whole-branch review each pass.

## Assess behavior and design

Use the following lenses where they can change the engineering decision; they are not a mandatory output checklist. Assess behavior and system fit separately: tests can pass for the wrong behavior, and a requirement can be met at the wrong layer.

- Trace the requested behavior through current code and evidence: is it delivered, missing, or accidentally changing unrelated behavior? Inspect relevant guidance, callers, schemas, tests, and persistence where they affect the answer. A remembered design or an earlier summary is not current evidence by itself.
- Verify responsibility before accepting new logic: does an existing owner or mechanism already normalize, validate, transform, or otherwise provide this behavior? Check for a symptom patch in one caller while the invariant belongs elsewhere. Reuse or adjust the existing owner only if its semantics fit; do not create a second path by default.
- Check evidenced contracts and reachable edge/failure paths. Make intentional contract changes visible. Follow error semantics, API behavior, data invariants, persistence, concurrency, security, accessibility, or consumer effects only where affected. Do not defend states excluded by enforced contracts. Retries, fallbacks, and recovery need real failure modes and safe side-effect semantics.
- Check scope and responsibility clarity, including documentation affected by the change. Identify obsolete paths it creates and unrelated cleanup or redesign mixed into it. Cleanup needs evidence and authorization within scope; larger opportunities stay separate.

## Check what machinery the problem earns

For introduced or materially changed machinery, consider removing behavior or flexibility without an evidenced current need; using a suitable standard-library operation; using an existing repository/framework/platform capability; and expressing the responsibility more directly. Name the actual replacement and check its semantics before recommending it. There is no fixed ranking or deletion target.

Look for speculative parameters, unused configurability, compatibility for hypothetical consumers, unjustified dependencies, forwarding wrappers, duplicate transformations, or helper chains that obscure a small behavior. One implementation or one caller is a prompt to examine responsibility, not proof an abstraction is wrong: a boundary can already earn its place through isolation, testability, or a real contract. Similar-looking code alone is not a reason to extract shared machinery.

Simplification must preserve correctness, readable control flow, diagnostics, evidenced contracts, security, accessibility, reliability, testability, and justified operations. Explicit code can be simpler than clever compression. Do not delete useful safeguards, force reuse across different semantics, or enlarge scope to improve a line count. If already appropriately simple, say so briefly and move on.

## Verify and report

Establish from the current request, plan if present, and implementation state whether this pass is functional construction or has reached test/verification. Apply [implementation's functional-first policy](../implementation/SKILL.md#functional-first-implementation): before test reconciliation, intentionally deferred coverage and expected stale mocks, fixtures, assertions, or wiring are remaining work, not defects by themselves. Do not demand an already-green suite or report missing tests solely because final coverage is deferred. Still report evidence of genuine production defects, preserved-contract violations, bad implementation assumptions exposed by coverage, and test/integration failures that block meaningful functional progress. Investigate the cause; phase labels alone do not establish that a failure is stale.

At test/verification and completion, apply full test-quality scrutiny. Inspect tests for observable behavior with independently justified expectations. For fixes, check that the regression case detects the original defect when practical. Look for stale assertions, meaningful missing failure/edge cases, tautological assertions, implementation-mirroring expectations, or mocks that remove the behavior being tested. Preserve assertions for unchanged contracts; update stale assumptions only for legitimate behavior changes. Prefer useful existing coverage; do not add redundant tests for trivial edits or weaken assertions to obtain green output. Missing meaningful coverage or unresolved broken tests are now verification gaps; functional-first sequencing never excuses finishing with them.

Read check commands before executing them. Use current evidence or run proportionate existing tests and applicable type, lint, build, or UI checks, including required repository gates when due. Repository tooling owns exact commands and mechanically enforceable rules. Inspect results, exit status, and whether intended cases ran; distinguish passed, failed, skipped, empty, not run, and pending CI. Reuse a result only when its checked content and relevant conditions still apply; evidence from an unpublished fix does not verify the remote head. Name any gate still due before the whole task can be called complete.

Probe a consequential suspicion with a concrete trigger or counterexample before calling it a defect. Material findings need location, triggering condition, consequence, and supporting evidence. Distinguish a confirmed defect (demonstrated failure), an unresolved concern (plausible material risk with missing evidence), and an optional improvement. Aesthetic preferences, hypothetical consumers, ungrounded performance worries, or complexity scores without a consequence are not defects.

Report only useful findings, evidence for continuing or completing this pass, checks actually run or reused, and remaining material gaps. A clean review is successful; no finding quota or long report is required. Stop when relevant evidence is inspected, proportionate verification is accounted for, and material concerns are resolved or clearly reported, provided more investigation is unlikely to change the decision. An unresolved concern can block dependent work; reporting it is not permission to claim completion. Do not broaden review merely because more analysis is possible.

## Mutation boundary

A review-only request permits inspection and safe local verification, including ordinary disposable test/build outputs. It does not authorize source fixes, staging, commits, discarding work, or publication. During an already authorized implementation, fix findings within that scope and recheck affected behavior. Apply the baseline policy before any check or action with external, destructive, or production effects.

`prepare-pr` may reuse this assessment or request a bounded reassessment against its pinned comparison, in review-only mode. Use its requirement evidence and comparison without rerouting projects. It owns publication, reviewer selection, and remote verification; this skill supplies implementation evidence, not integration approval or specialist certification. Load writing guidance through the baseline when authoring a substantial review.
