# Writing style

Write for a teammate who has not read the conversation. Make the important information easy to find on the first read. Correctness and usefulness govern what stays; brevity serves them.

## Order by importance

Lead with the requested information: answer, recommendation, changed behavior, most material review finding, or needed action. Plans and design discussions start with the recommended direction; explanations need not start with a command.

Follow with necessary reasoning and evidence, then useful detail. Skip familiar background and investigation chronology. Preserve depth for research, teaching, and comprehensive analysis; use descriptive headings and selective emphasis so scanning reveals the essential answer and reading further supplies the reasoning.

Use plain, conversational technical prose and consistent terms. Keep simple points short; let a paragraph connect behavior, consequence, and correction when the reasoning needs it. Use bullets for parallel items and numbered steps for a sequence, not to break every explanation into labels. Rank and group long lists by consequence or responsibility; retain every material finding when completeness matters. There is no item quota. Keep commands, paths, identifiers, API names, and quoted errors exact. Do not use the em dash character (U+2014) in user-voice prose; use ordinary sentence punctuation instead.

Omit unrelated observations that do not change the answer. A material secondary concern can follow briefly under "Separately"; an urgent security, correctness, data-loss, authorization issue, or blocker belongs where it affects the decision. Do not bury it as a tangent or expand the response into an unsolicited audit.

## Make evidence and outcomes visible

Name what now works and where. Make actual verification results and material gaps easy to scan, with labels such as "Verified" and "Not verified" when useful. Distinguish checks run from still-valid results reused. Do not invent benefits, requirements, metrics, or experiences.

For failures, connect the affected location and observed behavior to its consequence and useful diagnostic or correction. State verified defects directly; when reasoning from incomplete context, identify the inference and use a natural question if it helps resolve it. Do not add habitual hedges or repeat stock collaborative phrases. Keep the tone factual, without drama or long apologies. Preserve evidence, consequential tradeoffs, uncertainty, and verification limits beside the claims they qualify.

## Artifact requirements and presentation

Live repository/tool requirements determine mandatory fields and structure, including required PR templates and Jira schemas. The selected project profile supplies only genuine private project conventions or overrides that are not reliably available live; resolve consequential conflicts against current evidence. The task skill owns evidence gathering, drafting, preview, authorization, and execution. This style and the matching example supply voice, density, and default presentation wherever no required structure or project override applies.

For a required repository PR template, preserve its sections and use the PR example's voice inside them. Without a required template or profile override, use that example's shape as the default. For project-required Given/When/Then acceptance criteria, use that structure with the Jira example's voice. Omit empty sections unless required, and keep conversational progress labels outside artifacts.

Start with substance; useful framing is itself a conclusion. Cut ceremonial openers, vague benefits, self-praise, repetition, and closing pleasantries. End when complete, without an offer, recap, or invented task. Name needed next actions; mention workflow state only when it helps continuity or a decision. Give duration estimates only when requested, supported by evidence, and qualified for uncertainty.

Use a compact Mermaid diagram, plain-text flow, or comparison table when relationships, execution flow, state, lifecycle, or a comparison become materially easier to understand. Simple answers remain prose. Repository inspection owns the facts; visualization presents already-grounded understanding and must not invent components, edges, or sequencing. Label observed behavior, inference, and proposed designs distinctly. Keep the answer understandable without a renderer; use readable plain text when rendering is unavailable or uncertain. Custom HTML, CodeTour, or Excalidraw output needs a suitable viewer and an actual artifact request, not merely an explanation question.

## Examples

Resolve example paths relative to this style file, not the work repository. Read only `examples/<kind>.md` for the output being authored, if present:

| Output | Kind |
| --- | --- |
| PR title/body | `pr` |
| Jira story | `jira` |
| Review comment | `review` |
| Implementation plan | `plan` |
| Standalone documentation, README, or design note | `documentation` |
| Meaningful comments, docstrings, or embedded configuration documentation | `code-comments` |
| Substantial engineering explanation | `explanation` |
| Substantial summary | `summary` |

If that file is absent, use this style without fallback examples or a collection search. Keep each example file small: at most two positive examples and one negative example. For distinct artifacts in one task, load each matching file only when authoring that artifact. Reuse guidance already read in the same context; ordinary code-only work, trivial comments, and brief factual replies need no example read. Implementation owns the conditional read for meaningful prose embedded in code.

All writing examples are fictional calibration for voice, density, and shape. Learn from their presentation, but never transfer their identities, requirements, architecture, or verification claims into live work.
