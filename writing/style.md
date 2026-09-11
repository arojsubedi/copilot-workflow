# Writing style

Write for a teammate who has not read the conversation. Start with the concrete problem, changed behavior, or requested decision. Name the component and action; explain why it matters only as far as the reader needs.

Use direct subjects and verbs. Prefer short paragraphs with one main point. Use bullets for parallel items and steps for a sequence. Keep the necessary technical detail: triggers, before/after behavior, contracts, limitations, and evidence. Use one term consistently for one thing.

Avoid ceremonial openings, vague benefits, self-praise, and corporate filler. Words such as "robust" or "enhance" are not forbidden, but they need a precise meaning. Prefer "Reject expired tokens" to "Enhance the robustness of token validation." Do not turn a small fix into a product announcement.

State what the change does, not what it aims to do. Keep uncertainty where it belongs: "Not run; the test database is unavailable." Never upgrade an inference into a fact to make a draft read smoothly. Do not invent benefits, requirements, test results, metrics, or the author's experiences.

A PR explains the final diff and useful validation. A story describes the problem and observable acceptance criteria. A review comment identifies the location, triggering case, consequence, and suggested correction; label optional preferences. A plan names the approach, material decisions, and verification. A design describes the current system and its boundaries in present tense. An explanation answers the question, grounds the mechanism in evidence, and adds detail only as needed. A summary reports the outcome, checks, and unresolved limits. Omit empty sections unless the project's template requires them.

Use a compact Mermaid diagram, plain-text flow, or comparison table when relationships, execution flow, state, lifecycle, or a comparison become materially easier to understand. Simple answers remain prose. Repository inspection owns the facts; visualization presents already-grounded understanding and must not invent components, edges, or sequencing. Label observed behavior, inference, and proposed designs distinctly. Keep the answer understandable without a renderer; use readable plain text when rendering is unavailable or uncertain. Custom HTML, CodeTour, or Excalidraw output needs a suitable viewer and an actual artifact request, not merely an explanation question.

## Examples

Resolve example paths relative to this style file, not the work repository. Read only `examples/<kind>.md` for the output being authored, if present:

| Output | Kind |
| --- | --- |
| PR title/body | `pr` |
| Jira story | `jira` |
| Review comment | `review` |
| Implementation plan | `plan` |
| Design note | `design` |
| Substantial engineering explanation | `explanation` |
| Substantial summary | `summary` |

If that file is absent, use this style without fallback examples or a collection search. Keep each example file small: at most two positive examples and one negative example. For distinct artifacts in one task, load each matching file only when authoring that artifact. Reuse guidance already read in the same context; do not load examples during code-only work or brief factual replies.

Examples marked USER-APPROVED are the strongest style signal when compatible with the current request and project format. ILLUSTRATIVE examples are starting points, not evidence of the user's voice. Learn phrasing and information density, not their project facts. Never copy another project's names, identifiers, requirements, or test claims. Add sanitized examples here over time; ordinary prompts need no extra attachments.
