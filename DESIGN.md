# Architecture

This workflow keeps general judgment, task procedure, private identity, and writing calibration separate. Python installs ordinary local files; Copilot loads the relevant context during a task. Existing repository tooling and MCP connections supply current evidence.

## Owners

| Concern | Authoritative owner |
| --- | --- |
| Engineering judgment, context triggers, project selection, authorization | [Baseline](instructions/baseline.md) |
| Research, plan location, in-place revision, artifact-only handoff | [Planning](skills/planning/SKILL.md) |
| Constructing a change and sequencing test reconciliation | [Implementation](skills/implementation/SKILL.md) |
| Bounded assessment of behavior, design, simplicity, and verification | [Implementation review](skills/implementation-review/SKILL.md) |
| PR comparison, proposal, reviewers, publication and readback | [Prepare PR](skills/prepare-pr/SKILL.md) |
| Story requirements, proposal, creation and readback | [Jira story](skills/jira-story/SKILL.md) |
| Voice, default presentation, artifact precedence, matching examples | [Writing style](writing/style.md#artifact-requirements-and-presentation) |
| Private routing, connection identities, sparse project conventions | Local `projects/<name>.md`; [template](projects/project.example.md) |
| Current contracts, commands, templates, schemas, required fields | Work repository and live tools |
| File generation, configuration validation, ownership and drift | [setup.py](setup.py), documented in [setup](docs/setup.md) |
| Host discovery and limitations | [Compatibility](docs/copilot-compatibility.md) |
| Current executable checks and behavioral probes | [Verification](docs/verification.md) |

README is the entry point. Human documentation is not installed as runtime context. Other files summarize or link to these owners rather than defining parallel procedures.

## Operating model

```text
Understand the request and relevant evidence
  |-- question -> grounded answer
  `-- change -> plan when warranted -> authorized implementation
                                          |
                                          v
                                  review and verification
```

Tiny changes need focused checks. A durable plan is optional unless requested or warranted by uncertainty; the [planning skill](skills/planning/SKILL.md#choose-one-artifact) owns its default `<repository-root>/plan.md` location. Review evaluates meaningful passes and reuses evidence that remains valid. A sound partial pass does not establish completion of the whole task.

The baseline's [external-action policy](instructions/baseline.md#external-action-policy) governs consequential actions at every stage. Skills specify their concrete task boundaries and payloads. Host permission is a separate gate; Markdown instructions do not enforce tool permissions.

## Context loading

The active surface supplies or reads the baseline. Skill descriptions support discovery; a selected skill loads its procedure. Writing guidance and only the matching example load for meaningful prose. Private project context is progressive:

```text
Local READY profiles -> setup -> generated routing index
                                          |
                                          v
                                model selects one project
                                          |
                                          v
                                  reads one profile
```

Profiles own routing facts once. Setup reads fixed Routing bullets and generates the index; runtime selection belongs to the baseline. UNCONFIGURED profiles and templates stay in source. Connection credentials stay in the host/tool. Live metadata and repository requirements are read when needed, not cached in profiles.

## Installation and updates

Setup uses Python 3.12+ standard libraries with no network, shell, or package dependencies. It renders machine-local support paths, installs the five skills, and records generated file hashes. Sources accept UTF-8 with a BOM and CRLF/LF; installed bytes use UTF-8/LF. Profile text is copied with newline normalization, while its routing index is generated.

Preflight rejects unsafe paths, ambiguous routing and conflicting installed edits before writes or deletions. Existing desired bytes can be adopted; different content can be replaced only when it matches the last owned hash. Stale files can be deleted only when their bytes match their previous manifest hash; already absent files lose their stale ownership entries. Edited stale files block the update and remain intact with the manifest. Unowned neighbors remain untouched.

Replacement is atomic per file, not across the installation. Run one installer at a time and check/rerun after an interruption. Installed files remain generated state; source edits followed by setup are the update path. [Operational details](docs/setup.md#update-and-recover)
