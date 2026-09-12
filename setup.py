#!/usr/bin/env python3
"""Render, install, and check engineering workflow context using Python 3.12+ only.

Source Markdown is canonical; installed bytes are managed by an ownership
manifest. Preflight precedes all writes. Replacement is atomic per file, not
across the installation; run one installer at a time. No shell or network calls.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import sys
import tempfile
import unicodedata


def digest(data):
    return hashlib.sha256(data).hexdigest()


def render(source, root):
    """Accept UTF-8 with optional BOM and universal newlines; emit UTF-8/LF."""
    return source.read_text(encoding="utf-8-sig").replace(
        "{{WORKFLOW_ROOT}}", root.as_posix()
    ).replace(
        "{{BASELINE_PATH}}", (root.parent / "copilot-instructions.md").as_posix()
    ).encode("utf-8")


def read_routing(text):
    """Parse one fixed bullet section; the rest of a profile stays free Markdown."""
    sections = text.split("\n## Routing\n")
    if len(sections) != 2:
        raise ValueError("Expected one '## Routing' section; use project.example.md")
    routing = {}
    for line in sections[1].splitlines():
        if line.startswith("#"):
            break
        if not line.strip():
            continue
        match = re.fullmatch(r"- (Aliases|Git remote|Jira prefix|Local root): (.+)", line)
        if not match or match[1] in routing:
            raise ValueError("Routing needs unique labeled bullets: Aliases, Git remote, Jira prefix, optional Local root")
        value = match[2].strip()
        if value.startswith("`") and value.endswith("`"):
            value = value[1:-1]
        if not value or re.search(r"[<>|`\x00-\x1f]", value):
            raise ValueError("Invalid or placeholder routing value for " + match[1])
        routing[match[1]] = value
    if not {"Aliases", "Git remote", "Jira prefix"} <= routing.keys():
        raise ValueError("Routing requires Aliases, Git remote and Jira prefix (use unset where inapplicable)")
    return routing


def project_files(source):
    """Generate compact routing from READY local profiles; never write source."""
    projects = safe_target(source.resolve(), "projects")
    template = safe_target(source.resolve(), "projects/project.example.md").read_text(encoding="utf-8-sig")
    placeholders = set(re.findall(r"<[A-Za-z][A-Za-z0-9_-]*>", template))
    destination = ".copilot/engineering-workflow/projects/"
    files, rows, identities = {}, [], {}
    for path in sorted(projects.iterdir()):
        if path.suffix.lower() != ".md" or path.name.lower().endswith(".example.md"):
            continue
        try:
            safe_target(source.resolve(), "projects/" + path.name)
            if (path.suffix != ".md" or path.name.casefold() in ("index.md", "readme.md")
                    or "`" in path.name):
                raise ValueError("Use a .md profile filename; index.md and README.md are reserved")
            text = path.read_text(encoding="utf-8-sig")
            statuses = re.findall(r"^Configuration status: (.*)$", text, re.MULTILINE)
            if len(statuses) != 1 or statuses[0] not in ("READY", "UNCONFIGURED"):
                raise ValueError("Expected one 'Configuration status: READY' or 'Configuration status: UNCONFIGURED'")
            if statuses[0] == "UNCONFIGURED":
                print("Skipping UNCONFIGURED profile: " + path.name)
                continue
            if (any(token in text for token in placeholders)
                    or re.search(r"\bexample\.(com|org|net)\b|\.invalid\b", text, re.IGNORECASE)):
                raise ValueError("READY profile contains template placeholders; replace them or mark UNCONFIGURED")
            routing = read_routing(text)
            aliases = [alias.strip() for alias in routing["Aliases"].split(",")]
            if any(not alias or alias.casefold() == "unset" for alias in aliases):
                raise ValueError("Supply at least one nonempty alias; separate aliases with commas")
            remote, prefix = routing["Git remote"], routing["Jira prefix"]
            if remote != "unset":
                if (not re.fullmatch(r"[A-Za-z0-9.-]+/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", remote)
                        or any(part in (".", "..") for part in remote.split("/"))):
                    raise ValueError("Git remote must be host/owner/repository, without scheme or credentials")
                remote = remote.lower().removesuffix(".git")
                if remote.rsplit("/", 1)[1] in ("", ".", ".."):
                    raise ValueError("Git remote needs a repository name")
            if prefix != "unset" and not re.fullmatch(r"[A-Z][A-Z0-9_]*", prefix):
                raise ValueError("Jira prefix must be an uppercase project key or unset")
            if remote == prefix == "unset":
                raise ValueError("Supply a Git remote or Jira prefix to identify the project")
            local_root = routing.get("Local root", "unset")
            if local_root != "unset" and not (PureWindowsPath(local_root).is_absolute()
                                             or PurePosixPath(local_root).is_absolute()):
                raise ValueError("Local root must be an absolute Windows/macOS Git root or unset")
            # Prefixes can be shared by several repos; they are cross-checks only.
            keys = [("alias", alias) for alias in aliases]
            if remote != "unset":
                keys.append(("Git remote", remote))
            for kind, value in keys:
                key = (kind, unicodedata.normalize("NFC", value).casefold())
                if key in identities:
                    raise ValueError("Duplicate " + kind + " in " + identities[key] + " and " + path.name)
                identities[key] = path.name
            cells = [path.name, ", ".join(aliases), remote, prefix, local_root]
            rows.append("| " + " | ".join(cell.replace("\\", "\\\\") for cell in cells) + " |")
            files[destination + path.name] = text.encode("utf-8")
        except (OSError, ValueError) as error:
            raise ValueError("Invalid project profile " + str(path) + ": " + str(error)) from error
    index = "# Project routing\n\nGenerated by setup.py. Do not edit.\n\n"
    if rows:
        index += ("| Profile | Aliases | Git remote | Jira prefix | Local root |\n"
                  "| --- | --- | --- | --- | --- |\n" + "\n".join(rows) + "\n")
    else:
        index += "Configuration status: UNCONFIGURED\n\nNo READY projects.\n"
        print("No READY projects. Configure projects/<name>.md from project.example.md and rerun setup.")
    files[destination + "index.md"] = index.encode("utf-8")
    return files


def build_files(source, home):
    """Return home-relative destinations and bytes, without modifying the disk.

    This workflow packages Markdown only. Human documentation stays in source.
    Forward slashes serialize paths for Markdown/JSON, not shell execution.
    """
    root = home / ".copilot" / "engineering-workflow"
    baseline = render(source / "instructions" / "baseline.md", root)
    files = {
        ".copilot/copilot-instructions.md": baseline,
        ".copilot/instructions/engineering-workflow.instructions.md": (
            '---\napplyTo: "**"\n---\n\n'
            f'Engineering defaults: `{(root.parent / "copilot-instructions.md").as_posix()}`. '
            'If the full defaults are absent from the visible instruction context, '
            'read this file before proceeding. If unsure, read it; report access failures.\n'
        ).encode("utf-8"),
    }
    files.update(project_files(source))
    for path in sorted((source / "writing").rglob("*.md", case_sensitive=True)):
        relative = path.relative_to(source).as_posix()
        files[".copilot/engineering-workflow/" + relative] = render(path, root)
    for path in sorted((source / "skills").rglob("*.md", case_sensitive=True)):
        relative = path.relative_to(source / "skills").as_posix()
        files[".copilot/skills/" + relative] = render(path, root)
    # Default macOS/Windows volumes may fold case or Unicode normalization.
    # Fail everywhere rather than produce different file sets on each machine.
    seen = {}
    for relative in files:
        parts = relative.split("/")
        for end in range(1, len(parts) + 1):
            prefix = "/".join(parts[:end])
            key = unicodedata.normalize("NFC", prefix).casefold()
            if key in seen and seen[key] != prefix:
                raise ValueError("Install paths collide across platforms: " + relative)
            seen[key] = prefix
    return files


def safe_target(home, relative):
    """Validate a portable manifest path under an already resolved home.

    Refuse symlinks and Windows junctions below that root, including dangling
    links. This prevents accidental redirected writes, not concurrent hostile
    filesystem changes. The user-selected home itself may resolve through a link.
    """
    parts = relative.split("/")
    if any(
        part in ("", ".", "..") or part.endswith((" ", "."))
        or re.search(r'[<>:"\\|?*\x00-\x1f]', part)
        # Use the same filename subset on both OSes, including Python 3.12.
        # os.path.isreserved is Windows-only and was added in Python 3.13.
        or re.fullmatch(r"CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[1-9\u00b9\u00b2\u00b3]|LPT[1-9\u00b9\u00b2\u00b3]",
                        part.split(".")[0].rstrip(" ").upper())
        for part in parts
    ):
        raise ValueError("Invalid install path: " + relative)
    path = home / relative
    if not path.is_relative_to(home) or ".." in Path(relative).parts:
        raise ValueError("Invalid install path: " + relative)
    for entry in (path, *path.parents):
        if entry == home:
            break
        if entry.is_symlink() or entry.is_junction():
            raise ValueError("Refusing linked install path: " + str(entry))
        if entry != path and entry.exists() and not entry.is_dir():
            raise ValueError("Install parent is not a directory: " + str(entry))
    if not path.resolve().is_relative_to(home):
        raise ValueError("Install path escapes the selected home: " + relative)
    return path


def write_atomic(path, data):
    """Replace one file with a closed sibling temporary file; clean up failures.

    Closing before os.replace is required on Windows. Use ordinary data files;
    executable bits and source ACLs are not part of the installation contract.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temp_name = handle.name
            handle.write(data)
        os.replace(temp_name, path)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def install(source, home, check=False):
    """Preflight ownership, then update files (0), or check for drift (0/1).

    Conflicts raise before mutation. Exact expected bytes can be adopted even
    without a manifest. Otherwise only bytes matching the last recorded digest
    may be replaced or removed when no longer desired.
    """
    home = home.expanduser().resolve()
    files = build_files(source, home)
    manifest = safe_target(home, ".copilot/engineering-workflow/install-manifest.json")
    previous = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else {}
    if not isinstance(previous, dict) or any(
        not isinstance(k, str) or not isinstance(v, str)
        or re.fullmatch(r"[0-9a-f]{64}", v) is None
        for k, v in previous.items()
    ):
        raise ValueError("Invalid install manifest; inspect " + str(manifest))
    for relative in previous:
        safe_target(home, relative)
    expected_manifest = {p: digest(b) for p, b in files.items()}
    manifest_bytes = (json.dumps(expected_manifest, indent=2) + "\n").encode("utf-8")
    manifest_outdated = previous != expected_manifest or not manifest.exists()

    conflicts, outdated = [], []
    for relative, expected in files.items():
        target = safe_target(home, relative)
        if target.exists() and not target.is_file():
            conflicts.append(str(target) + " is not a file")
            continue
        actual = target.read_bytes() if target.exists() else None
        if actual == expected:
            continue
        outdated.append(relative)
        if actual is not None and digest(actual) != previous.get(relative):
            conflicts.append(str(target) + " has existing or locally edited content")
    stale = sorted(set(previous) - set(files))
    removable = []
    for relative in stale:
        target = safe_target(home, relative)
        if not target.exists():
            continue
        if not target.is_file():
            conflicts.append(str(target) + " is not a file")
        elif digest(target.read_bytes()) != previous[relative]:
            conflicts.append(str(target) + " is stale and no longer matches the last owned hash")
        else:
            removable.append(relative)
    if conflicts:
        raise ValueError("No files changed.\n" + "\n".join(conflicts)
                         + "\nMerge wanted content into the source first. "
                         "Back up and remove conflicting installed files, then rerun setup.")
    if check:
        if outdated or manifest_outdated:
            print("Installation differs from source: "
                  + ", ".join(outdated + ["stale: " + p for p in stale]
                              + (["manifest"] if manifest_outdated else [])))
            return 1
        print("Installed files match the source. App UI settings are not inspectable by setup.")
        return 0

    for relative in removable:
        safe_target(home, relative).unlink()
    changed = 0
    for relative, data in files.items():
        target = safe_target(home, relative)
        # A case-only rename can share the stale file's path on Windows/macOS.
        if relative in outdated or not target.exists():
            write_atomic(target, data)
            changed += 1
    if manifest_outdated:
        write_atomic(manifest, manifest_bytes)
    print(f"Installed {changed} changed files and removed {len(removable)} stale files under {home / '.copilot'}.")
    print("App: paste " + str(home / ".copilot/copilot-instructions.md")
          + " into Settings > Sessions > App instructions.")
    print("VS Code: verify engineering-workflow in Instructions and all workflow skills in Skills.")
    print("Start a fresh session and verify context. Configure the relevant project profiles before live use.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path,
                        help="Destination home directory; use a temporary directory for testing")
    parser.add_argument("--check", action="store_true", help="Compare files without writing")
    args = parser.parse_args()
    try:
        home = (args.home if args.home is not None else Path.home()).expanduser().resolve()
        override = os.environ.get("COPILOT_HOME")
        if override and Path(override).expanduser().resolve() != home / ".copilot":
            raise ValueError("COPILOT_HOME differs from the installation target. "
                             "Use the default layout; shared discovery in other surfaces "
                             "is not documented for a relocated Copilot home.")
        return install(Path(__file__).resolve().parent, home, args.check)
    except (OSError, ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    # A redirected Windows console may not encode the selected Unicode home.
    # Preserve file bytes and the operation's exit status; escape display only.
    sys.stdout.reconfigure(errors="backslashreplace")
    sys.stderr.reconfigure(errors="backslashreplace")
    sys.exit(main())
