# Code-comment examples

USER-CALIBRATED. The code and configuration contracts are fictional; these examples demonstrate prose, not reusable implementations.

## Positive: ordering and caller semantics

```python
def make_preview(source, selection, size):
    """Return an independent image; changes to it do not affect source."""
    # The selection uses coordinates from the original image. Crop before
    # resizing so those coordinates still refer to the pixels the user selected.
    # Resizing first would move the selection and could include a different area.
    selected = source.crop(selection)
    return selected.resize(size)
```

## Positive: embedded configuration documentation

```toml
# Print profiles define sheet dimensions and default margins for saved reports.
# The export request selects a profile by name; it does not supply layout rules.
#
# PROFILE BOUNDARY
# ReportLayout owns pagination and overflow handling. Values here describe the
# available space, so adding a paper size does not require another layout path.
#
# WHEN VALUES CHANGE
# Each new export copies the selected profile into its saved layout. Updating a
# profile affects later exports; it does not reformat an already saved report.
# Removing a name still used by a saved preference makes new exports fail profile
# lookup, so migrate those preferences before removing that entry.
#
# ADDING A PAPER SIZE
# Give it a distinct name and supply dimensions and margins in millimeters.
# ReportLayout subtracts both margins from each dimension. The remaining width
# and height must be positive or the profile is rejected before rendering.

[profiles.pocket]
width_mm = 110
height_mm = 170
margin_mm = 8
```

## Negative

```python
# Set the selected profile.
selected_profile = profiles[name]
```

The assignment already says this. Explain a non-obvious constraint when one exists; sectioned documentation belongs where readers need it, not above every lookup.
