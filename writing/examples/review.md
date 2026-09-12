# Review examples

## Positive: focused comment

`set_quantity` saves the new amount before checking whether it is negative. The request returns a validation error, but the invalid value is already stored. What do you think about validating the quantity before calling `save` so a rejected request leaves the item unchanged?

## Positive: substantial comment

The catalog download now reads the entries in pages, but from what I can tell, each page still queries the live catalog again. I am not sure that gives us a consistent download if someone updates the catalog while the download is in progress.

For example, let's say the first page returns entries A and B, and B is then renamed so that it now sorts after C. The next call to `CatalogRepository.list_entries` uses an offset of two against the updated ordering. In that case, wouldn't we potentially get B again while C has moved before the offset and is never included?

`CatalogDownload.write_page` looks like it just appends each page to the output, so I don't see anything later in the flow that would recover the skipped entry. Even if we remove duplicates at the end, that would only solve one side of the problem since C would already be missing.

Maybe I am missing something here, but is there anything that keeps the same catalog revision across all of these calls?

If not, what do you think about reading all of the pages from the same revision/snapshot so the download sees a consistent set of entries even if the catalog is being updated at the same time?

## Negative

"Concern: pagination robustness. Impact: potential inconsistency. Recommendation: consider enhancing the implementation with appropriate safeguards."

The labels do not explain which edit causes a missing entry or why the proposed correction would help. Use the concrete path and consequence; uncertainty belongs to the unresolved snapshot assumption.
