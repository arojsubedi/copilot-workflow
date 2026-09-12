# How the workflow fits together

The workflow separates guidance that should apply everywhere from context needed only for a particular task or project. This keeps routine sessions lean while making specialized work repeatable.

```text
User asks a question or requests work
             |
             v
General engineering defaults apply
             |
             +-- Does the task need a specialized workflow?
             |       -> load the matching skill
             |
             +-- Does the task depend on a configured project?
             |       -> identify the project and load only its profile
             |
             +-- Does the task produce meaningful prose?
                     -> load the writing style and matching example

Current repository + current GitHub/Jira data provide the evidence
```

## The parts and their responsibilities

| Part | Responsibility |
| --- | --- |
| [Engineering defaults](instructions/baseline.md) | General judgment, proportionate verification, project selection, writing triggers, and approval before external changes. |
| Task skills, such as [planning](skills/planning/SKILL.md) | Focused procedures for planning, implementation, self-review, Jira stories, PR preparation, and PR discussion catch-up. A skill is loaded only when its description matches the task. |
| Local project profiles | Private identities and conventions that cannot reliably come from the repository or live tools, such as connection names and preferred reviewers. |
| [Writing guidance](writing/style.md) | Shared voice and presentation rules. One matching fictional example calibrates a substantial artifact. |
| Work repository and tools | Current code, contracts, tests, repository instructions, templates, Git state, GitHub data, Jira data, and tool schemas. These remain the factual source of truth. |
| [Installer](setup.py) | Validates local configuration and makes the workflow available to supported Copilot surfaces. |

README and the files under `docs/` explain the workflow to people; they are not loaded as runtime instructions.

## Project context

A task should not require Copilot to read every private project profile just to find the relevant one. During setup, the workflow builds a small lookup from READY profiles. During a project-dependent task, Copilot compares the explicit target and current repository identity with that lookup, then reads only the selected profile.

The profile supplies stable private facts. It does not cache repository commands, source architecture, Jira board state, or other information that can be inspected live. If identity is missing or ambiguous, only the project-dependent part of the task is blocked.

## Specialized workflows

Normal engineering questions use the general defaults and repository evidence. Substantial planning, implementation, implementation self-review, Jira story preparation, PR preparation, and PR discussion catch-up each have their own skill. Their narrow descriptions let Copilot select the relevant procedure without loading every procedure into every task.

The review-context workflow is deliberately separate from implementation review. It reconstructs what people discussed on an existing PR and, when relevant, linked Jira history. It remains read-only and distinguishes discussion claims from facts observed in code.

## Writing and external changes

Writing guidance is loaded only for meaningful prose, along with the one example that matches the artifact. Repository templates and live required fields take priority over default presentation; project profiles add only genuine private overrides.

Reading, inspecting, and drafting are allowed. Before a consequential action changes a shared or external system, the workflow shows the exact target, payload, and effect and asks for explicit approval. A changed PR, Jira issue, reviewer request, push, merge, comment, destructive operation, or production action requires approval for the current proposal.

For installation mechanics, safe updates and removal, filesystem layout, and Copilot surface differences, see [technical details](docs/technical-details.md).
