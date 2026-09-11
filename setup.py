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
from pathlib import Path
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
    for folder in ("projects", "writing"):
        for path in sorted((source / folder).rglob("*.md", case_sensitive=True)):
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
    may be replaced. Removed sources need explicit cleanup, never auto-deletion.
    """
    home = home.expanduser().resolve()
    files = build_files(source, home)
    manifest = safe_target(home, ".copilot/engineering-workflow/install-manifest.json")
    legacy_manifest = safe_target(home, ".copilot/personal-workflow/install-manifest.json")
    if legacy_manifest.exists():
        raise ValueError(
            "No files changed. Legacy ownership manifest found: " + str(legacy_manifest)
            + "\nFollow docs/setup.md migration: back up the recorded files and manifest; "
            "relocate this manifest to " + str(manifest)
            + " only if that destination is absent. If both exist, reconcile their "
            "ownership records first; never overwrite either blindly. Then run --check "
            "and explicitly clean up the listed obsolete files and entries."
        )
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
    removed = set(previous) - set(files)
    legacy_bridge = ".copilot/instructions/personal-workflow.instructions.md"
    if legacy_bridge not in previous and safe_target(home, legacy_bridge).exists():
        conflicts.append("Legacy instruction bridge has no ownership record: " + legacy_bridge
                         + "; inspect, back up and remove it before installing its replacement")
    if removed:
        conflicts.append("Previously installed files removed from source; review and remove "
                         "them locally, then remove their manifest entries: "
                         + ", ".join(sorted(removed)))
    if conflicts:
        raise ValueError("No files changed.\n" + "\n".join(conflicts)
                         + "\nMerge wanted content into the private source first. "
                         "Back up and remove conflicting installed files, then rerun setup.")
    if check:
        if outdated or manifest_outdated:
            print("Installation differs from source: "
                  + ", ".join(outdated + (["manifest"] if manifest_outdated else [])))
            return 1
        print("Installed files match the private source. App UI settings are not inspectable by setup.")
        return 0

    for relative in outdated:
        write_atomic(safe_target(home, relative), files[relative])
    if manifest_outdated:
        write_atomic(manifest, manifest_bytes)
    print(f"Installed {len(outdated)} changed files under {home / '.copilot'}.")
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
