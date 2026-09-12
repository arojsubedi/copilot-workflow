# PR examples

USER-CALIBRATED. All Jira keys, components, behavior, and verification evidence are fictional. These are two scales of description, not required templates.

## Positive: focused change

Title: `[APP-1842] Keep the selected measurement unit when reopening a chart`

This PR saves the chart's selected measurement unit with the user's display preferences. Previously, reopening the chart restored the default unit even when the user had selected a different one.

The chart now reads the saved unit when it opens. Charts without a saved preference continue to use the existing default.

Verified locally by selecting a unit, closing the chart, and reopening it. The saved-preference and first-visit tests also passed.

## Positive: substantial change

Title: `[DOC-2317] Render document previews outside the upload request`

This PR moves document preview rendering into a background worker. Today, an upload request waits for every preview page to finish before returning, so a large document can keep the request open even though the original file has already been stored.

The upload now returns the document identifier once storage succeeds and a render task has been recorded. `PreviewCoordinator` tracks that task and exposes its state to the document page. While rendering is in progress, the page shows the original document details and a processing indicator. Preview pages become available together when the completed generation is published.

The worker handles:

- claiming pending render tasks
- creating a separate working directory for each attempt
- passing the document to `PageRenderer`
- publishing the completed generation and removing temporary output

`PageRenderer` still owns page layout and image generation. Task state and publication stay in `PreviewCoordinator`, so the renderer does not need to know how a document was uploaded or how its progress is displayed.

### Scope

This changes when previews are produced, not which document formats are accepted. Existing previews remain readable. Documents uploaded before this change are not automatically queued for another render.

### Verification

The coordinator, renderer, and document-page tests passed. In a local worker run, I uploaded a multi-page document and confirmed that the upload returned before rendering finished, then checked that the preview appeared after publication.

I also verified that a failed render leaves the original file available and shows the failure state without exposing partial preview pages.

Production worker capacity has not been measured, so the local run does not establish throughput under concurrent uploads.

## Negative

Title: `Improve document preview processing`

"This enhancement delivers a robust preview solution that seamlessly optimizes the document experience through a scalable processing framework."

Name what changed, explain the behavior that matters, and keep unsupported capacity or reliability claims out.
