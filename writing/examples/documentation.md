# Documentation example

USER-CALIBRATED. The component and contracts below are fictional. This models a standalone guide, not a mandatory section layout.

## Positive

```markdown
# Measurement import profiles

An import profile maps a file's column names and units to the measurement fields stored by the application. The same import path handles each supported file format; the profile supplies the differences between them.

The parser keeps the original value and unit alongside the normalized value. This allows someone investigating an unexpected result to compare what was received with what was stored, without reconstructing the input from the conversion.

## When a column is not recognized

An unknown column stops the import before any measurements are saved. It is not silently ignored, since a renamed measurement column could otherwise look like an empty reading. The error identifies the column and the selected profile so the mapping can be checked against the file.

## Adding a format

Add a profile with the incoming column names and their units, then exercise it with a representative file. Unit conversion belongs to `MeasurementNormalizer`; profiles select a supported unit rather than supplying their own conversion formula.

Changing a mapping affects future imports only. Previously imported measurements retain both their original and normalized values.
```
