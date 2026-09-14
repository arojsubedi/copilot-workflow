---
name: eng-implementation
description: Construct a meaningful code change from repository evidence and contracts. Use for implementation; not for tiny edits, explanations, or review-only requests.
---

# Implementation

Construct the requested change coherently in this codebase. Work from the current request and inspected code; a separate spec or plan file is not required. This skill guides construction. [Implementation review](../eng-implementation-review/SKILL.md) challenges the resulting pass.

Read `{{BASELINE_PATH}}` if its full text is absent from the visible context (read it if unsure). It owns engineering judgment, project selection, and authorization. Reuse current evidence rather than restarting discovery.

When a current plan is supplied, read the validated proposal from its actual active surface: native session plan, explicit destination, repository plan, or identified in-chat proposal. Confirm its target repository, current artifact/source, and implementation authorization; do not require a repository copy or consume another plan merely because it is named plan.md. A planning request or plan acceptance alone does not authorize coding. Use the plan's intent, owners, dependencies, and verification alongside current code; refresh evidence that can invalidate it without repeating all discovery. Resolve routine details autonomously. If new evidence consequentially invalidates a contract, owner, scope, or step, pause dependent implementation, reconcile the decision through [planning](../eng-planning/SKILL.md), and update the same artifact before continuing. Preserve unrelated plan edits; do not create a competing specification or follow a stale plan literally.

## Learn the affected subsystem

Before choosing a local pattern, inspect neighboring implementations, applicable repository guidance, affected interfaces/data, and relevant tests. Identify the domain terms, behavior owner, boundary contracts, and observable result this change must provide. Keep a short scope outline when it helps hold the work together; do not impose a file or line quota.

Treat precedent as evidence. Preserve an established contract or convention unless intentionally changing it. When a historical accident directly causes the problem, correct the affected responsibility instead of reproducing it. Explain an intentional departure and verify affected callers. Surface a larger redesign separately unless the requested behavior requires it; reconsider upstream decisions when new evidence invalidates them.

## Build around responsibility

Locate existing validation, normalization, conversion, and business logic before adding another path. Compare actual semantics, including errors and side effects, before reusing an owner. Inspect suitable repository mechanisms, language/standard-library features, framework/platform facilities, and installed dependencies when they can replace custom machinery; none wins by category alone.

Keep functions and modules centered on a coherent responsibility. Extract when it gives business knowledge one owner, defines a useful boundary, or makes reasoning materially clearer. Similar syntax and length alone do not justify extraction. Avoid generic utility collections and chains of forwarding helpers. Expose what callers need without leaking internal orchestration or adding unused options.

Use the subsystem's sound domain vocabulary. Name the responsibility or transformation rather than hiding it behind a vague manager/helper name; keep obvious local names concise. Prefer direct control flow a reader can follow without reconstructing tricks.

## Preserve meaning at boundaries

Validate where the contract is enforced; keep error categories and actionable diagnostics meaningful. Catch a failure only where it can be handled or translated correctly. Add retries or fallbacks only for an identified failure with safe side-effect semantics.

Represent an important invariant in the existing type/schema/data model when practical. Keep transformations explicit enough to check and avoid wrappers that add no constraint or responsibility. Do not widen an API merely to make this implementation convenient.

Use comments for an invariant, surprising constraint, or rationale the code cannot express; document public semantics and non-obvious contracts where readers need them. Follow repository documentation requirements. Do not narrate ordinary statements or mechanically add docstrings. Update nearby documentation when behavior makes it stale.

When authoring or substantially revising non-trivial comments, public/non-obvious docstrings, or embedded configuration documentation, read `{{WORKFLOW_ROOT}}/writing/style.md` and its `examples/code-comments.md` if present. Reuse current reads. Ordinary code edits and trivial comments do not trigger this calibration.

## Functional-first implementation

Build the requested production functionality to a coherent state before reconciling test code with the completed intended behavior. This is the normal sequencing policy for meaningful features, including work without a phased plan. Test execution can provide feedback during construction; test maintenance normally waits until the functionality is coherent enough to exercise across its affected production paths. Final coverage and verification remain required; TDD is not mandatory.

During functional construction:

- Prioritize production behavior in coherent increments and preserve real contracts. Remove directly obsolete production paths within scope; keep unrelated cleanup separate. Do not distort interfaces or retain obsolete production structure to satisfy mocks or tests.
- Inspect actual check commands and side effects before running them. Use existing tests or type, build, runtime, smoke, API, or UI checks diagnostically when they can expose a bad assumption before more code depends on it. Investigate failures against intended behavior and preserved contracts; fix genuine production defects or blocking integration failures when discovered. Do not assume a failure is stale merely because behavior is evolving.
- Defer repairs to stale assertions, mocks, fixtures, test data, and wiring caused by intentional changes, and defer final behavioral/regression coverage while that behavior is still changing. Recognize expected fallout and note it in the current plan if material; do not rewrite tests for each intermediate state or repeatedly interrupt functional phases to keep the suite green. If stale test plumbing blocks meaningful diagnostic progress, make only the repair needed to regain that feedback.

Once the functional implementation is coherent, complete a dedicated test/verification phase (a direct step suffices for a contained change):

- Inspect affected tests and reconcile stale mocks, fixtures, test data, and wiring. Update or remove assertions only where behavior legitimately changed; retain assertions for preserved contracts. Never weaken assertions just to obtain green output.
- Add missing meaningful behavioral/regression coverage at existing useful test boundaries. Derive expected outcomes from requirements or independent examples, including relevant edge/failure cases, rather than mirroring the implementation.
- Run focused tests and broader required repository gates; inspect results and distinguish stale test assumptions from implementation defects. Fix genuine production bugs revealed by verification and recheck affected behavior. Reuse still-valid results rather than duplicating runs.

Use `eng-implementation-review` after meaningful passes, with the current phase clear; it can run during functional construction. After test reconciliation and verification, review the completed implementation, adjust within authorized scope, and recheck affected behavior. Deferred maintenance must be resolved before completion: missing meaningful coverage, unresolved broken tests, or required checks still due remain gaps, not a completed feature. Carry forward actual results and unavailable verification honestly; following this procedure is not proof of correctness.

## Mutation boundary

Requested implementation permits scoped, reversible local edits. This skill grants no independent authority to commit, publish, push, open a PR, mutate an external service, or perform destructive/production actions. Apply the baseline's approval rules to consequential actions, including checks with such effects. An explanation-only or review-only request does not become an implementation request by loading this skill.
