---
name: implementation
description: Construct a meaningful code change using the affected subsystem's contracts, vocabulary, ownership, and test boundaries. Use during implementation; tiny edits, explanation-only requests, and review-only requests do not need this skill.
---

# Implementation

Construct the requested change coherently in this codebase. Work from the current request and inspected code; a separate spec or plan file is not required. This skill guides construction. [Implementation review](../implementation-review/SKILL.md) challenges the resulting pass.

Read `{{BASELINE_PATH}}` if its full text is absent from the visible context (read it if unsure). It owns engineering judgment, project selection, and authorization. Reuse current evidence rather than restarting discovery.

When a current plan is supplied, read it and confirm its target repository and implementation authorization. A planning request or plan acceptance alone does not authorize coding. Use the plan's intent, owners, dependencies, and verification alongside current code; refresh evidence that can invalidate it without repeating all discovery. Resolve routine details autonomously. If new evidence consequentially invalidates a contract, owner, scope, or step, pause dependent implementation, reconcile the decision through [planning](../planning/SKILL.md), and update the same artifact before continuing. Preserve unrelated plan edits; do not create a competing specification or follow a stale plan literally.

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

## Keep construction and evidence together

Introduce observable behavior in coherent increments and add or adjust proportionate checks as it appears. Use existing meaningful test boundaries; do not distort production interfaces to make mocking easier. Derive expected outcomes from the requirement or an independent example. Inspect the repository's actual check commands and side effects before running them.

Run focused checks soon enough to catch a broken assumption before more code depends on it. Run broader required gates when the affected boundaries warrant them; reuse still-valid results. Neither mandatory TDD nor running everything after every edit is required.

Remove directly obsolete paths when safe and within scope; leave unrelated cleanup separate. Once a meaningful pass delivers its intended behavior, inspect its diff with `implementation-review`, adjust within the authorized scope, and continue only if work remains. Carry forward actual checks and unresolved gaps, not a claim that following this procedure proves correctness.

## Mutation boundary

Requested implementation permits scoped, reversible local edits. This skill grants no independent authority to commit, publish, push, open a PR, mutate an external service, or perform destructive/production actions. Apply the baseline's External-action policy to consequential actions, including checks with such effects. An explanation-only or review-only request does not become an implementation request by loading this skill.
