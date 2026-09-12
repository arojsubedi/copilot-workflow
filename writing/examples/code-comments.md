# Code-comment examples

## Positive: phases in a substantial business flow

```python
def reconcile_release(
    request: ReleaseRequest,
    packages: PackageRepository,
    transitions: TransitionRepository,
) -> ReconciliationResult:
    """Reconcile a requested release with its currently persisted package state.

    Validation happens before dependent package reads so a rejected release
    cannot be mistaken for a missing package set.

    :param request: Requested release identity and package versions.
    :param packages: Source of the currently persisted package state.
    :param transitions: Destination for state changes produced by reconciliation.
    :return: The applied and rejected transitions for the requested release.
    """
    # Step 1: Validate the release identity before loading dependent state.
    release = validate_release(request)

    # Step 2: Load one consistent view of the packages in this release.
    current = packages.for_release(release.id)

    # Step 3: Reconcile desired versions without mutating persisted state.
    result = compare_packages(current, request.packages)

    # Step 4: Persist only transitions accepted by reconciliation.
    transitions.apply(release.id, result.applied)
    return result
```

The comments mark real phases in a longer flow. They do not narrate the individual calls between those boundaries, and shorter functions would not need the same structure.

## Positive: non-obvious invariant

```python
# Keep the generation record until every page is published. Readers resolve the
# active generation once, so switching it early can mix old and new preview pages.
publisher.publish_pages(generation)
publisher.activate(generation.id)
```

The comment explains why ordering matters and what breaks if it changes.

## Negative

```python
# Look up the selected profile.
selected_profile = profiles[name]
```

The assignment already says this. Ordinary statements and obvious functions need no narration; comments and docstrings should explain a contract, phase, invariant, ownership boundary, or surprising consequence that the code cannot express clearly on its own.
