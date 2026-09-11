# Plan examples

ILLUSTRATIVE: fictional repository, symbols, and checks; these examples demonstrate density, structure, and voice. They are not required templates or evidence about a real project.

## Positive — focused change

```markdown
# Cancel queued exports

## Problem

Users can cancel running exports but cannot cancel queued ones. Allow cancellation before a worker starts while preserving the existing behavior for running and completed exports.

## Current system and approach

`src/exports/service.py` — `ExportService.cancel` owns cancellation and validates state.

`ExportRepository.transition` performs conditional state changes, and workers already use it when claiming queued exports. Extend the cancellation path through the same transition owner so cancellation and worker claims resolve the race consistently rather than introducing another locking or cancellation mechanism.

## Implementation plan

1. Extend `ExportService.cancel` to allow queued exports through `ExportRepository.transition`. Preserve the existing running/completed behavior and verify that cancellation winning the transition prevents a later worker claim.

2. Expose queued cancellation in `src/ui/ExportActions.tsx` after the service behavior exists. If the worker wins the race, refresh the current export state rather than reporting cancellation success.

3. Update the affected service and UI behavioral tests for queued cancellation and the lost-race case.

## Verification

Run the existing export service and UI checks documented in `CONTRIBUTING.md`. Exercise a queued cancellation through the UI and confirm that a successfully cancelled export is not subsequently claimed by a worker.

These are planned checks, not passing results.
```

This change is contained enough that named phases would add ceremony without clarifying the implementation.

## Positive — substantial change

```markdown
# Unify case-status transitions

## Problem

API requests and background reconciliation currently update case status through separate paths. The paths duplicate transition rules and can produce different validation and error behavior.

Use the existing persisted transition mechanism as the common owner while preserving the current API contract and reconciliation behavior.

## Current system

`src/cases/service.py` — `CaseService.update_status` validates API status changes and writes them directly.

`src/cases/events.py` — `CaseEventProcessor.apply_transition` owns persisted transitions used by background reconciliation.

`src/cases/repository.py` — `CaseRepository.transition` performs the conditional database update and detects stale state.

The duplicated responsibility is above the repository: both the API service and event processor currently decide which transitions are valid before persistence.

## Approach

Use the existing event transition path as the shared owner of domain transition rules and route API updates through it.

Keep `CaseRepository.transition` responsible for atomic persistence and stale-state detection. Keep request validation and API-specific response/error mapping at the service/API boundary.

This removes duplicate transition ownership without adding another abstraction.

## Implementation plan

### Phase 1 — Establish the shared transition behavior

Extend `CaseEventProcessor.apply_transition` to support the transition cases currently accepted through `CaseService.update_status`.

Preserve existing domain validation and distinguish invalid transitions from stale-state conflicts. Use existing transition checks diagnostically if needed to test that assumption before routing the API path; correct production contract violations when found.

### Phase 2 — Route API updates through the shared owner

Update `CaseService.update_status` to delegate domain transition decisions through `CaseEventProcessor` instead of maintaining its own transition logic.

Keep API request validation and boundary-specific error mapping in the service layer. Remove the duplicated service transition logic once no caller depends on it.

### Phase 3 — Complete dependent production paths

Update production callers that depend on `CaseService` writing status directly.

Preserve background reconciliation behavior. Existing reconciliation callers should continue through the event path without new compatibility branches or forwarding wrappers.

Remove only transition code made obsolete by the shared path; keep unrelated case-status cleanup outside this change. The API and reconciliation paths should now be coherent enough to exercise together.

### Phase 4 — Reconcile tests and verify the feature

Repair affected fixtures, mocks, test data, and wiring that assume direct service writes. Preserve assertions for the unchanged API and reconciliation contracts; update stale internal assumptions. Add behavioral/regression coverage for the API-required transitions through the shared owner and meaningful failure cases.

Run the existing case-service, event-processor, repository, API, type, and lint checks required by the repository.

Exercise:

- a successful API transition
- an invalid transition
- a stale-state conflict
- the existing reconciliation transition path

Confirm that both API and reconciliation persist through `CaseRepository.transition` while retaining their existing boundary-specific error behavior.

Distinguish stale test assumptions from real production failures, fix defects, and recheck affected behavior. These are planned checks, not passing results.
```

The functional phases follow real dependency and ownership boundaries: establish the common behavior, migrate the API path, and complete dependents. Diagnostic checks may guide construction; test maintenance and new coverage belong in the final verification phase once production behavior is coherent.

## Positive — revision converges in place

Suppose the first draft proposed a new `StatusTransitionService`, but further repository inspection establishes that `CaseEventProcessor` already owns the same responsibility.

Update the current plan to:

```markdown
## Approach

Use the existing `CaseEventProcessor` transition path as the shared owner. Keep atomic persistence in `CaseRepository.transition` and API-specific response mapping in `CaseService`.
```

Then replace any implementation phases that created or migrated callers to `StatusTransitionService`.

Do not retain:

> Previous approach: create `StatusTransitionService`.

The plan should read as though the current approach had been selected coherently from the beginning.

## Negative — planning history

```markdown
## Implementation plan

### Phase 1 — Create a new transition service

...

## Update 1

After discussion we may use the event processor instead.

## Update 2

We decided to use the event processor. Keep Phase 1 above for context.

## Decision log

1. Originally considered direct repository calls.
2. Then considered a new service.
3. Finally chose the event processor.
```

Replace the obsolete approach and dependent phases with the current proposal. The planning conversation contains the exploration; `plan.md` should not become its archive.

## Negative — fake phasing

```markdown
## Implementation plan

### Phase 1 — Backend

Change backend files.

### Phase 2 — Frontend

Change frontend files.

### Phase 3 — Tests

Write tests.
```

File type alone is not an implementation boundary. Use phases only when they clarify real ownership, dependency order, or verification.

## Negative — over-prescription

```markdown
### Phase 2

1. Open `service.py`.
2. Go to line 147.
3. Create a variable named `transition_result`.
4. Add a helper named `_validate_status`.
5. Call the helper from line 162.
```

Plan behavior, ownership, important constraints, and useful symbols. Leave routine local implementation choices to the implementation phase unless a specific detail is consequential to correctness.
