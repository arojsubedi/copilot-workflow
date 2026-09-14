#!/usr/bin/env python3
"""Persist one immutable private review run; read the complete report body on stdin.

Only the parent review workflow invokes this helper. It does not retrieve PRs,
decide findings, or publish anything. Path checks prevent accidental redirection,
not a hostile process racing filesystem changes.
"""

import argparse
from datetime import datetime, timezone
from itertools import count
from pathlib import Path
import re
import stat
import sys


def component(value):
    if (not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", value)
            or value in (".", "..") or value.endswith(".")
            or re.fullmatch(r"CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9]",
                            value.split(".")[0].upper())):
        raise ValueError("Unsafe report identity component")
    return value


def checked_path(path):
    """Inspect existing components without resolving away links or junctions."""
    path = Path(path)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("Report roots must be absolute and contain no traversal")
    for entry in (*reversed(path.parents), path):
        try:
            info = entry.lstat()
        except FileNotFoundError:
            continue
        if (stat.S_ISLNK(info.st_mode)
                or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
            raise ValueError("Refusing linked or redirected report path: " + str(entry))
        if entry != path and not stat.S_ISDIR(info.st_mode):
            raise ValueError("Report parent is not a directory: " + str(entry))
        if entry == path and not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)):
            raise ValueError("Report path is not a regular file or directory")
    return path


def persist_report(workflow_root, worktree, *, host, owner, repository, pr, base,
                   head, gate, disposition, body, prior_head=None, reviewed_at=None):
    """Create a new UTC run, suffix collisions, then verify its exact UTF-8/LF bytes."""
    identity = [component(value) for value in (host, owner, repository)]
    if not isinstance(pr, str) or not re.fullmatch(r"[1-9][0-9]*", pr):
        raise ValueError("PR number must be a positive decimal integer")
    revisions = (base, head, *([prior_head] if prior_head is not None else []))
    for sha in revisions:
        if not isinstance(sha, str) or not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", sha):
            raise ValueError("Pinned revisions must be full lowercase hexadecimal Git object IDs")
    if len({len(sha) for sha in revisions}) != 1:
        raise ValueError("Pinned revisions must use the same Git object format")
    if gate not in ("PASS", "FAIL", "UNRESOLVED"):
        raise ValueError("Invalid behavior gate")
    if disposition not in ("APPROVE", "COMMENT", "REQUEST CHANGES"):
        raise ValueError("Invalid review disposition")
    if not isinstance(body, str) or not body.strip():
        raise ValueError("A complete nonempty review body is required")
    timestamp = reviewed_at if reviewed_at is not None else datetime.now(timezone.utc)
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("Review timestamp must be timezone-aware")
    timestamp = timestamp.astimezone(timezone.utc)
    reviewed = timestamp.isoformat(timespec="microseconds").replace("+00:00", "Z")
    run_id = timestamp.strftime("%Y%m%dT%H%M%S") + f"{timestamp.microsecond:06d}Z"
    root = checked_path(workflow_root)
    tree = Path(worktree)
    if not tree.is_absolute() or not tree.is_dir():
        raise ValueError("The reviewed worktree must be an existing absolute directory")
    tree = tree.resolve(strict=True)
    directory = root.joinpath("reviews", *identity, "pr-" + pr, head)
    checked_path(directory)
    if root.exists() and not root.is_dir():
        raise ValueError("Workflow root is not a directory")
    if directory.resolve().is_relative_to(tree):
        raise ValueError("Private reports must stay outside the reviewed worktree")
    if not directory.resolve().is_relative_to(root / "reviews"):
        raise ValueError("Report path escapes the private reviews directory")
    header = (f"# Review: {'/'.join(identity)} PR #{pr}\n\n"
              f"Reviewed at: {reviewed}\n\nPinned base: `{base}`\n\nPinned head: `{head}`\n\n")
    if prior_head is not None:
        header += f"Prior reviewed head: `{prior_head}`\n\n"
    header += f"Behavior gate: {gate}\n\nRecommended disposition: {disposition}\n\n"
    data = (header + body.replace("\r\n", "\n").replace("\r", "\n").strip() + "\n").encode("utf-8")
    directory.mkdir(parents=True, exist_ok=True)
    checked_path(directory)
    for suffix in count(1):
        name = run_id + (f"-{suffix}" if suffix > 1 else "") + ".md"
        target = checked_path(directory / name)
        if target.exists() and not target.is_file():
            raise ValueError("Report destination is not a regular file: " + str(target))
        try:
            with target.open("xb") as output:
                output.write(data)
        except FileExistsError:
            checked_path(target)
            continue
        if checked_path(target).read_bytes() != data:
            raise OSError("Report read-back differs from the intended bytes: " + str(target))
        return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflow-root", type=Path, required=True)
    parser.add_argument("--worktree", type=Path, required=True)
    for field in ("host", "owner", "repository", "pr", "base", "head"):
        parser.add_argument("--" + field, required=True)
    parser.add_argument("--prior-head")
    parser.add_argument("--gate", choices=("PASS", "FAIL", "UNRESOLVED"), required=True)
    parser.add_argument("--disposition", choices=("APPROVE", "COMMENT", "REQUEST CHANGES"), required=True)
    args = vars(parser.parse_args())
    try:
        body = sys.stdin.buffer.read().decode("utf-8-sig")
        path = persist_report(**args, body=body)
        print(path)
        return 0
    except (OSError, ValueError, RuntimeError) as error:
        print("Review persistence failed; retain the complete review in chat: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    sys.exit(main())
