# Technical details

This document describes the current installer and runtime integration. It is optional depth for maintainers; ordinary configuration and operations are in [setup.md](setup.md).

## Installed layout

Setup resolves the selected home through Python and manages these destinations:

| Source | Destination under the selected home |
| --- | --- |
| `instructions/baseline.md` | `.copilot/copilot-instructions.md` |
| Generated VS Code instruction adapter | `.copilot/instructions/engineering-workflow.instructions.md` |
| READY profiles and generated project lookup | `.copilot/engineering-workflow/projects/` |
| `writing/**/*.md` | `.copilot/engineering-workflow/writing/` |
| `skills/**/*.md` | `.copilot/skills/<name>/` |
| Generated ownership data | `.copilot/engineering-workflow/install-manifest.json` |

Human documentation and `projects/project.example.md` remain source-only. Setup renders workflow and personal-instruction paths into runtime Markdown. Source Markdown accepts UTF-8 with an optional BOM and ordinary platform newlines; installed files use UTF-8 with LF newlines.

## Project lookup generation

`setup.py` scans only Markdown files directly under `projects/`, excludes `*.example.md`, and installs profiles marked READY. It reads the `Project`, `Git remote`, `Jira prefix`, and optional `Local root` bullets from the Routing section. The rest of each profile remains free Markdown and is copied without interpreting reviewer or convention semantics.

The generated `projects/index.md` contains routing facts only. It lets runtime guidance select one profile without reading all private profiles. Project names and Git identities must be unique after case and Unicode normalization. Jira prefixes may be shared because several repositories can belong to one Jira project.

READY profiles reject exact template placeholders, reserved example domains, malformed Git identities, invalid Jira keys, unsafe filenames, and relative local roots. At least one Git remote or Jira prefix must identify the project. UNCONFIGURED profiles are not installed.

## Ownership and safe replacement

The manifest maps each managed relative path to the SHA-256 digest of the bytes last installed by this workflow. It is an ownership record, not a security signature.

Before install, update, or removal, setup validates all relevant paths and file states. A desired file may be created, adopted when its bytes already match, or replaced when its current bytes match the previously recorded digest. A stale managed file may be removed only when it still matches its recorded digest. Missing stale files require only manifest cleanup. A locally changed managed file blocks all mutation so the user can preserve it first.

Uninstall performs the same kind of full preflight against every manifest entry. It removes unchanged managed files and the manifest, treats absent managed files as already gone, and stops without deleting anything if a target differs or is not a regular file. It does not recursively remove `.copilot`, `.copilot/skills`, `.copilot/instructions`, or other shared directories.

Writes use a closed temporary sibling followed by `os.replace`, which is atomic per file. The entire installation is not one atomic transaction. Run one setup process at a time; after interruption, `--check` and a rerun reconcile the remaining state.

## Path safety and portability

The implementation uses only Python 3.12+ standard-library APIs and makes no network or shell calls. It rejects manifest path escapes, absolute manifest paths, unsafe path components, reserved device names, and links or junctions below the selected home. It also rejects source destinations that would collide on common case-folding or Unicode-normalizing filesystems.

The selected home itself is resolved before these checks. The checks prevent accidental redirection and cross-platform ambiguity; they are not a defense against a hostile process racing filesystem changes.

## Copilot surfaces and other instructions

GitHub documents personal CLI instructions at `~/.copilot/copilot-instructions.md`, personal skills at `~/.copilot/skills/`, and repository instruction forms including `.github/copilot-instructions.md`, `AGENTS.md`, and `CLAUDE.md`. Support differs by Copilot surface, so inspect the capabilities of the client in use. [GitHub's support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support) lists current combinations.

Personal skills are installed in GitHub's documented Copilot skill location. The clients expose different discovery and inspection controls; use the current client's instruction or skill view rather than assuming that installation proves loading. [GitHub's customization reference](https://docs.github.com/en/copilot/reference/customization-cheat-sheet)

For Copilot CLI, GitHub says applicable personal and repository instructions are combined and does not define a general precedence order. The CLI `/instructions` command shows discovered files. [CLI custom-instruction documentation](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)

This workflow installs personal/user-level instructions. Work repositories may also contain `AGENTS.md`, `CLAUDE.md`, or Copilot repository instructions. Relevant instructions may be combined depending on the surface, so avoid duplicating generic behavior in both places; repository files should contain repository-specific knowledge and instructions. This repository does not add an `AGENTS.md` because its maintainership rules are already expressed by its source, design, and tests.

The generated `engineering-workflow.instructions.md` adapter points VS Code clients to the shared personal defaults when their full text is not already visible. The Copilot app uses a manual paste into its app-instructions UI because setup cannot edit that setting. Restart or open a fresh session after changes; discovery alone does not prove that a particular file was loaded.

## Validation and tests

`python setup.py --check` builds the expected file set and performs the same configuration, path, ownership, and drift preflight without writing. It returns `0` when installed state matches, `1` for safe differences, and `2` for conflicts or invalid input.

Run the automated suite with:

```text
python -m unittest discover -s tests -v
```

The tests use temporary source copies and homes. They cover READY and UNCONFIGURED profiles, single and multiple projects, project lookup changes, template exclusion, routing validation, reviewer preservation, unrelated-file preservation, ownership conflicts, stale files, interruption recovery, path safety, encoding/newlines, install/check/update/uninstall/reinstall behavior, skill metadata/rendering, and Markdown links. A symlink-specific test can skip when the local account cannot create symlinks.

Automated filesystem tests do not establish that a Copilot client loaded the intended instruction, selected the correct project, followed writing calibration, or honored a conversational approval boundary. Verify those behaviors in the clients you actually use by inspecting discovered instructions, selected skills/profile, MCP target, and proposed external action.
