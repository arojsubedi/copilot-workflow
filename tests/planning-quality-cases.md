# Planning quality cases

These sanitized cases evaluate the [planning workflow](../docs/planning.md) semantically. They are manual evaluation guidance, not automated model scoring, a results log, or design history. Judge evidence paths, ownership, scope, readiness, and final artifact coherence, not exact wording or deterministic worker selection.

## Run and assess

Use a fresh session and disposable fixture repository for each case. Give the planner the request and raw repository evidence below, withholding the evaluator's expected behavior and pitfalls. Materialize the listed evidence as fixture files when testing actual repository navigation; supplied snippets alone do not establish that exploration occurred. No unlisted consumer is implied. Do not contact real GitHub/Jira targets or modify work repositories.

Request: "Use /eng-planning to propose this change from the supplied fixture repository. Write its current plan.md and stop before implementation." The tempting direction is an evaluator-only challenge seed: introduce it in parent context only, never in an accessible file, requirement, or independent packet. For existing-file leakage probes, verify real exclusion or honest unavailable-independence handling. Also exercise the neutral request without a seeded draft. The independent pass receives outcome, neutral evidence, and constraints, with no rubric, draft, chosen mechanism, or other worker conclusions.

Inspect actual delegation, supplied context, file reads, and final plan. A same-direction independent result is valid; agent agreement is not evidence of correctness. Verify that only the selected active plan changes, that revisions replace prior directions, and that no critique/history artifact appears. Plan acceptance alone must not begin implementation. Missing material evidence stays visible rather than becoming invented scope or a readiness claim.

Repeat a substantial case with delegation unavailable and with a draft accidentally inherited/read: require honest lost-independence disclosure, a fresh neutral context when supported, and parent evidence challenges. A still-unresolved consequential assumption prevents readiness for dependent implementation. Repeat with rubber-duck unavailable; do not label parent reasoning complementary-model critique. Installation in a temporary home alone does not prove Copilot discovery or isolation; inspect the actual client's selected skill and context.

## Existing interface owns the change

- **Request:** expose the display unit for each metric variant.
- **Evidence:** `domain/metric.py` defines `ExistingInterface` with variant identity, value resolution, and display precision; its implementations own variant-specific formatting data. `ui/metric.py` and `api/metrics.py` consume that interface. There is no independent unit lifecycle or provider contract.
- **Tempting draft:** create `NewInterface` plus unit-provider implementations and wiring.
- **Evidence path:** search metric resolution/formatting responsibility, inspect interface implementations and both consumers, and compare unit behavior with the existing contract. The independent solver starts with the outcome, not the proposed interface.
- **Expected:** falsification discovers the existing interface; independent reasoning considers extending it. The final plan assigns units there unless inspection establishes an independent responsibility. Consumer integration and meaningful unit behavior are covered.
- **Avoid:** extending an unrelated interface merely to reduce file count, or retaining the new interface because the draft designed it coherently.

## Invented persistence requirement

- **Request:** add a UI selection between standard and weighted metrics.
- **Evidence:** `ui/MetricPanel.tsx` owns temporary panel choices; mounting resets them. `product/panel.md` specifies panel-session behavior for comparable choices. No request or product convention establishes cross-session persistence. No preference consumer exists in the supplied repository.
- **Tempting draft:** add a preference store, database field, and reload behavior.
- **Evidence path:** inspect selection lifetime, comparable controls, callers, and storage contracts; establish the source of the persistence premise.
- **Expected:** identify persistence as speculative and omit it. Express selection through the existing panel owner and verify selection/reset behavior. Preserve actual implicit product contracts even though the request is brief.
- **Avoid:** a user question for an already-resolved routine lifetime choice, an "alternative rejected" section, or deleting persistence when a variant fixture explicitly establishes it as a contract.

## Over-engineered extensibility

- **Request:** offer the weighted counterpart where available.
- **Evidence:** `domain/metric.py` models a standard metric with an optional weighted counterpart. All callers consume this pair; no runtime registration or other modes exist.
- **Tempting draft:** create an arbitrary plugin/provider architecture with mode discovery and configuration.
- **Evidence path:** inspect model, variant creation, consumers, and actual sources of variability.
- **Expected:** represent the evidenced pair in its natural owner; challenge configuration and registration without a current responsibility.
- **Avoid:** claiming flexibility itself is a requirement, or treating one implementation as universal proof that an abstraction is invalid.

## Under-designed existing variability

- **Request:** add forecast metric selection alongside supported variants.
- **Evidence:** `domain/variants.py` owns standard, weighted, and normalized variants through one typed resolution registry. `ui/VariantPicker.tsx` enumerates that registry and `api/metrics.py` resolves by variant identity.
- **Tempting draft:** add an `isForecast` boolean and a parallel conditional branch in each caller.
- **Evidence path:** trace variant identity from UI and API to implementations and inspect the registry's domain contract.
- **Expected:** extend the actual general owner and integrate forecast semantics through existing consumers. Existing variability defeats the extra special-case path.
- **Avoid:** YAGNI-only simplification that removes a justified model, or expanding the registry into an unrelated universal plugin system.

## Existing framework capability

- **Request:** propagate cancellation from the request boundary to an outgoing operation.
- **Evidence:** the fixture's locked framework version exposes a native cancellation token; `services/export` already passes it through a native client overload. `services/preview` uses the same client but omits that overload. Required cancellation and error behavior are documented in `api/cancellation.md`.
- **Tempting draft:** add a cancellation dependency and wrapper service.
- **Evidence path:** inspect the installed version, client overload, precedent's side effects/error mapping, and current authoritative version documentation when local evidence is insufficient.
- **Expected:** use the native path if its semantics match; plan verification for cancellation propagation and boundary error behavior. If documentation is unavailable and semantics remain consequentially uncertain, disclose that premise.
- **Avoid:** deleting a dependency because a similarly named native feature exists, upgrading the framework without need, or claiming an executed check from documentation alone.

## Missing behavioral partition

- **Request:** allow clearing an optional delivery message without changing it when omitted.
- **Evidence:** `api/contract.md` defines absent as unchanged, null as clear, and a supplied nonempty string as replacement. `api/schema.json` preserves all three states. `domain/delivery.py` owns updates; its caller currently tests only supplied text.
- **Tempting draft:** use one truthiness condition for optional input.
- **Evidence path:** trace parsed request values through the update owner and persisted representation, comparing each meaningful partition with the contract.
- **Expected:** account for absent/null/supplied semantics before implementation and name distinguishing verification for preserving versus clearing the value.
- **Avoid:** an exhaustive combination matrix for unrelated fields or a new validation layer when the current boundary can enforce the contract.

## Missed consumer and transition

- **Request:** replace persisted `pending` status with `queued`.
- **Evidence:** `deploy/rollout.md` specifies migration before sequential replica replacement, so old/new workers coexist. `worker/claim.py` accepts only `pending` in the old release. `jobs/export.sql` also filters `pending`. Deployment policy is forward-fix only; dispatch can reach either worker generation during replacement.
- **Tempting draft:** update only migration and model, then verify new steady-state behavior.
- **Evidence path:** follow serialized status through workers, raw SQL, dispatch, and deployment ordering; derive reachable intermediate states.
- **Expected:** include the surviving consumer and a safe transition sequence grounded in actual coexistence. Name integration evidence that exercises the intermediate state as well as final behavior.
- **Avoid:** invented rollback guarantees or a generic compatibility framework. In a variant where deployment demonstrably stops every consumer for migration, do not retain mixed-version ceremony.

## Weak verification plan

- **Request:** make eligibility depend on the latest event's enabled state.
- **Evidence:** `schema/events.sql` retains history with unique increasing per-entity sequence. `api/contract.md` excludes entities whose latest event is false regardless of older events. The API forwards the query result. Existing tests contain one true row and one false row in separate histories.
- **Tempting draft:** correctly select latest state but verify only the two existing single-row cases.
- **Evidence path:** compare the intended rule and a plausible `ANY historical true` implementation against the planned inputs; inspect query-to-API integration.
- **Expected:** plan the counterexample older=true/latest=false, which must exclude the entity, and relevant integration evidence. Explain what this proves without inventing an exhaustive test list.
- **Avoid:** treating passing single-row tests as proof, calling a correct design defective solely because coverage is incomplete, or forcing test-first sequencing.

## Simple change stays simple

- **Request:** set preview retention to 14 days, matching nightly retention.
- **Evidence:** `config/channels.json` contains preview=7 and nightly=14. `config/schema.json` permits integer days 1..30. The only consumer, `src/retention.py`, adds the configured days to creation time. No changed contract or additional policy is implicated.
- **Tempting draft:** none is needed; a direct owner edit is supported.
- **Evidence path:** inspect config, schema, consumer, and existing config check command.
- **Expected:** a concise plan with an internal evidence sanity check and relevant verification; no unnecessary independent plan, rubber-duck ceremony, or user decision. Stop before changing the config.
- **Avoid:** designing a policy service, requiring workers merely because a validation stage exists, or inventing retention/rollout obligations.

## Evidence defeats the challenge

- **Request:** deduplicate payment delivery retries durably across worker restarts.
- **Evidence:** `cache/display.py` owns a process-local, evictable display cache. Its documented contract permits lost entries and concurrent recomputation. `payments/contract.md` requires durable operation identity across workers; `db/operations.py` provides transactional unique-key persistence for payment operations.
- **Tempting challenge:** an independent worker suggests using the existing display cache to avoid durable operation state.
- **Evidence path:** inspect cache lifetime, eviction and concurrency semantics against payment obligations, then trace transactional operation persistence and retry boundaries.
- **Expected:** the parent rejects cache reuse on contract evidence even if several workers endorse it. A draft based on the durable operation owner remains if still supported. Verify restart and ambiguous retry behavior appropriate to the actual provider contract.
- **Avoid:** accepting a worker as authority, inventing exactly-once provider guarantees, or retaining the challenge and model discussion in final plan.md.

## Draft leakage and preexisting artifacts

- **Request:** expose variant units through /eng-planning using the existing-interface fixture above.
- **Evidence:** the raw outcome, existing owner, implementations and callers from that fixture. Give only the parent a provisional `NewInterface` direction in private context.
- **Evidence path:** inspect the independent packet, actual reads, inherited context and accessible filesystem/session artifacts. The evaluator keeps the expected owner out of the solver's prompt.
- **Expected:** independent discovery happens before persisting proposed symbols/design to either repository or session plan. It derives from raw outcome/evidence; comparison happens after its return. Repeat with a preexisting or automatically generated draft: establish actual exclusion using supported read scope, or report missing independent discovery. A worker that consumed it is anchored critique.
- **Avoid:** treating a no-read instruction as isolation, deleting an existing user plan, or hiding the leaked draft in a differently named notes file.

## Native Plan mode and one active artifact

- **Request:** plan the variant change using /eng-planning while supported native Plan mode is active, with no explicit file destination.
- **Evidence:** the client reports its actual current session plan; project-edit restrictions also apply to delegated work. Ordinary repository files and any unrelated plan are present.
- **Evidence path:** inspect client mode, actual artifact location, effective helper permissions and safe read-only dispatch. In a disposable client fixture, verify a direct attempted project edit is refused; do not infer this from a prose instruction or installer test.
- **Expected:** use one session plan, persisting design after warranted independent discovery. No competing repository plan or application edit appears. Uncertain shell/external operations remain outside authorization. Repeat with an explicitly requested repository-local plan: expose native write restrictions and preserve pending destination or use a supported artifact-only transfer with one active source. Implementation can later consume that active plan directly.
- **Avoid:** selecting an implementation action merely to copy the plan, automatic plan-then-autopilot, or assuming native mode also isolates draft reads.

## Coverage closure catches an omitted requirement

- **Request:** expose variant units in the UI and CSV exports, preserving existing API precision.
- **Evidence:** `ui/metric.py`, `exports/metrics.py`, and `api/metrics.py` consume the same variant owner. CSV units are explicitly required for exported rows, and API precision is a preserved contract.
- **Tempting draft:** correctly extend the variant owner and UI, with sound tests for both, while forgetting CSV exports.
- **Evidence path:** compare the full request/constraints with owner-to-consumer paths and distinguishing verification, not just choices already investigated.
- **Expected:** closure catches the missing export path/verification and accounts for API preservation before readiness. If export semantics cannot be established, the plan remains explicitly limited.
- **Avoid:** a giant traceability matrix or calling the plan ready because its included steps are coherent.

## Repository changes during planning

- **Request:** add unit display to a metric panel.
- **Evidence:** initial inspection traces `MetricVariant` to two consumers. During planning, a concurrent unstaged edit changes unit normalization in that owner and adds a relevant untracked consumer. HEAD and the short status categories need not change.
- **Evidence path:** retain initial inspected content/revision and relevant local state, then inspect affected content and newly relevant paths before handoff. Repeat with a materially updated issue contract.
- **Expected:** refresh invalidated owner/consumer assumptions, relevant validation and coverage, preserving concurrent edits. The final plan reflects the new semantics or explicitly unresolved conflict. Unchanged HEAD alone does not establish freshness.
- **Avoid:** restarting unrelated research, overwriting the concurrent work, or claiming stale initial evidence is current.

## Large mechanically determined change

- **Request:** replace a deprecated generated field name across all generated bindings after an already settled schema rename.
- **Evidence:** a pinned generator/config owns all outputs; the schema mapping and migration contract uniquely determine the replacement. The complete consumer inventory has no alternate ownership or unresolved transition question. Many generated files change.
- **Evidence path:** inspect generator/input contract, consumer completeness, regeneration command/trust and integration verification.
- **Expected:** perform repository falsification, coverage closure and freshness checks. No independent architecture search or rubber-duck pass is required solely because the output is large. Use dependency-oriented functional sequencing.
- **Avoid:** inventing provider abstractions, competing schemas or a worker roster to match diff size.

## Small design-consequential change

- **Request:** remember the selected metric mode between sessions.
- **Evidence:** the apparent change is one storage call, but `account/preferences.py` already owns synchronized per-user preferences; panel-local storage has different user/device semantics. The request does not establish the intended persistence boundary.
- **Tempting draft:** add browser storage as a new source of truth.
- **Evidence path:** inspect actual preference owner, login/account transitions, consumers and established product conventions; independently derive the owner from neutral constraints where safe dispatch supports it.
- **Expected:** scrutinize the state/ownership commitment despite the tiny diff. Resolve scope from evidence or ask the consequential user question, then use useful adversarial critique and distinguishing cross-session/user verification. Unsafe or draft-exposed delegation is disclosed rather than counted as independent.
- **Avoid:** accepting the first storage call as obvious, or automatically expanding scope to synchronization absent an evidenced requirement.
