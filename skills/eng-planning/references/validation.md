# Plan validation

Read this procedure for normal meaningful and substantial planning before accepting the draft. The [core skill](../SKILL.md#validate-the-proposal) owns depth selection and handoff. Validation tests the framing as well as the proposed implementation; polishing the first design cannot establish that it belongs in the system.

## Falsify consequential commitments

Identify the few choices that can change implementation direction: introducing an owner, state, persistence, a dependency, compatibility, configuration, variability, a contract change, or rollout ordering. No formal IDs or exhaustive checklist are needed. For each, seek evidence that could defeat its necessity or chosen owner.

**Requirement reality.** Separate explicit requests, established repository contracts, actual caller needs, current platform constraints, inference, and speculation. Preserve implicit requirements established by contracts; current code alone may not establish intended behavior. Remove speculative persistence, compatibility for nonexistent consumers, arbitrary configuration, future variants, and unsupported rollout obligations. Missing evidence alone proves neither presence nor absence; investigate material uncertainty.

**Semantic ownership and earned machinery.** Search by domain responsibility, not just the draft's new symbol. Inspect existing interfaces, services, providers, stores/contexts, helpers, validation, configuration, persistence, and orchestration boundaries that could own it. Compare real semantics, errors, side effects, and consumers. Prefer changing, extending, reusing, or removing an existing mechanism when it naturally represents the responsibility. A new owner needs an independent responsibility; forcing unrelated behavior into an existing abstraction to save a file is also wrong.

Apply the same test to new state/refs, classes, wrappers, dependencies, caches, queues, retries, flags, and generic frameworks: what present problem requires them, where does existing machinery fail, and what ownership or synchronization burden follows? Check suitable native/framework capabilities and installed dependencies; research the applicable version only when their semantics are not established locally. Similar capability names do not prove equivalence.

**Variability in both directions.** Several current variants sharing a domain mechanism can justify extending its general owner instead of another boolean branch. A standard metric and optional weighted counterpart alone do not establish arbitrary plugin modes. Choose the simplest design that represents evidenced variability; "more extensible" and minimum line count are not independent reasons.

**Behavior, impact, and transition.** Examine meaningful partitions where they can change the design: absent/null/supplied, enum/state transitions, latest versus historical state, old/new representations, permission boundaries, error semantics, retry and partial failure. Trace affected callers and consumers, including dynamic/configuration/serialized relationships. Establish migration/deployment order, coexistence, duplicate effects, security, accessibility, and operational obligations from the actual environment. Ordinary domains need no exhaustive matrix; do not invent mixed-version or rollback needs where deployment excludes them.

**Verification and sequence.** Name what behavior must be proved and a plausible wrong implementation. Would the planned check distinguish them? Single true/false rows cannot distinguish latest-state inclusion from any historical true; an older true followed by latest false can. Include high-value boundary or integration evidence without an exhaustive test inventory. Ensure phases follow ownership and real dependencies, with transitions safe when reached. Preserve functional-first sequencing and final test reconciliation; validation does not impose TDD or mechanical backend/frontend/tests buckets.

## Bounded repository exploration

Use maintained `explore` selectively for factual questions that could falsify an assumption, such as:

- Find the current owner of metric variant resolution and existing interfaces/implementations representing it.
- Trace consumers and validation boundaries for the field whose contract changes.
- Locate configuration, retry/idempotency, or installed capabilities already responsible for the requested behavior.

Give the repository identity/root, relevant neutral evidence, a bounded question, and read-only scope. Ask for paths/symbols, actual semantics, counter-evidence, and search limits. Do not ask it to prove the plan good or vote on a design. Use available semantic definitions, references, implementations, and call tracing; supplement with text search for dynamic names, strings, configuration, SQL, and external consumers. An incomplete index or bounded negative search does not prove no owner exists.

GitHub documents `explore` as a non-editing codebase worker and `general-purpose` as a worker with main-agent capabilities in a separate context window. Explicitly request the intended subagent through the active client's supported delegation mechanism; a name in prose or switching the main agent is not evidence that delegation occurred. Confirm actual dispatch and returned scope. [Built-in agents and subagent contexts](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents), [explicit invocation](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents), [semantic navigation](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/lsp-servers)

## Independent alternative seeking

When a consequential design commitment or framing question warrants independent discovery, after repository falsification, delegate a fresh `general-purpose` context only if both mutation protection and draft exclusion below are established. Derive an approach independently. It is a solver before it is a reviewer. Supply only:

- The original requested outcome, separating any user-suggested means from explicit constraints.
- Evidenced requirements/constraints with their sources, relevant repository identity/context, and neutral repository evidence already established.
- Unresolved material questions, without presupposing the draft's chosen implementation.

Do not send the draft plan, chosen implementation, proposed symbol names, parent's verdict, alternative comparison, or other worker conclusions. Do not forward the full parent conversation. Pass the requested outcome separately from optional user-suggested means; preserve explicit constraints. Source paths/symbols already observed are evidence, not proposed names. Do not prime the solver with "we create NewInterface; find a better alternative."

Before dispatch, ensure no persisted accessible draft contains the provisional direction. Keep it in parent context until the independent result returns, including when using a native session plan. Instructions not to read `plan.md` do not create filesystem isolation. For a plan already present from this or a previous pass, preserve it and concurrent edits; use a supported context whose effective read scope excludes all draft-bearing files, session artifacts/history, and inherited conclusions. Do not move/delete a user's plan just to manufacture independence. If native tooling automatically persists or supplies the draft and cannot exclude it, use the fallback below.

The bounded task is to determine the smallest coherent implementation approach from the outcome and evidenced constraints; inspect the natural owner and existing mechanisms before introducing state, interfaces, abstractions, dependencies, persistence, or configuration. Return the supported direction, anchors, material consequences, evidence gaps, and a materially different approach only if discovered. Do not invent options to fill a quota. The same owner/direction with no better mechanism found is a valid result. Require read-only reasoning, no code/plan writes, commands with mutation effects, implementation, or nested delegation; main-agent capabilities are not a read-only permission boundary.

Only after the independent result returns should the parent compare it with the draft and investigate material differences. Independence requires a neutral input and draft-free reasoning, not merely a different worker name or model.

### Capability and isolation limits

Establish two separate conditions before full-capability dispatch:

- **Mutation protection:** prefer already-active native Plan mode, where delegated project-edit restrictions are inherited. Inspect effective tools/permissions and restrict work to repository reading/search. Plan mode still permits some uncertain shell commands and connected external tools; prohibit those mutation paths and do not grant broad approvals. Outside native Plan mode, dispatch only through a supported context with effective read-only tool/permission restrictions preserving the planning boundary. Read-only prose alone is insufficient.
- **Draft exclusion:** a separate context window alone does not establish a clean packet or filesystem isolation. Verify that inherited conversation, automatic context, readable drafts/session logs, and worker communications do not expose the provisional direction. Use a fresh restricted context if supported. Do not use a context that already critiqued the proposal for independent discovery.

If a worker saw the draft, treat its output as anchored critique, not independent discovery. Rerun cleanly only when practical and both conditions can be met. If safe independent dispatch or draft exclusion cannot be established, retain repository falsification and useful supported read-only evidence mechanisms. Disclose the missing independent perspective at handoff; never call parent reasoning equivalent validation. A consequential assumption left unresolved prevents readiness for dependent implementation. Do not install a custom validator to mask unsupported client capability.

GitHub documents native Plan-mode restrictions and their limits, including inheritance by delegated subtasks. It is project mutation protection, not a complete sandbox or draft-read boundary. Use local subagent dispatch; `/delegate` sends work to the cloud and can create a PR, so it is not a planning research substitute. [Plan-mode boundary](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#plan-mode), [session plan and cloud delegation](https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-best-practices)

## Adversarial critique

After repository falsification and comparison/reconciliation of any warranted independent approach, use maintained `rubber-duck` when adversarial critique can materially change a consequential conclusion. No worker is required solely because a task is large. It may now see the original outcome, evidenced constraints, current draft, relevant repository evidence, and a material alternative discovered independently. Ask it to attack the problem framing, owner, requirement reality, unnecessary machinery, both over-generalization and under-designed current variability, omitted behavioral scenarios, affected consumers/transitions, and whether verification would catch a plausible defect. Request concrete evidence and consequences, not stylistic improvement or automatic approval.

GitHub documents a read-only critic on a complementary model, currently available with Claude/GPT main-session models when a suitable critic model is available. Use actual client support and enabled availability; do not pin a model or assume every surface exposes it. If unavailable, apply the capability fallback above and report the missing complementary critique. [Rubber-duck behavior and availability](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/rubber-duck)

Rubber-duck is a challenger, not an authority or sole validator. It cannot replace repository falsification or unanchored solution discovery.

## Reconcile and converge

For each material challenge, identify the exact disputed assumption, inspect the cited evidence and relevant counter-evidence, then determine whether the plan holds. The parent may reject a proposed reuse when it violates another contract. Repository/contract evidence decides, never model voting, number of agreeing agents, numeric confidence, or "rubber-duck said so."

Revise defeated assumptions and dependent scope, owners, scenarios, phases, and verification in the same plan. Recheck affected commitments after a material revision. If a consequential choice remains undecidable from evidence, ask the user and leave dependent work unsettled; routine details remain autonomous. Stop when material challenges are resolved and further exploration is unlikely to change the direction, or hand off explicit readiness limits.

Keep only the current chosen proposal and rationale needed to prevent an implementation mistake. Persist no critique transcript, alternative comparison, validation history, second plan, or validation report. Return to the core skill for coverage closure, evidence refresh, persistence of the one active plan, final coherence, and the implementation authorization boundary.
