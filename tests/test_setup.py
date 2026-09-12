"""Installer boundary checks; no Copilot sessions or network access."""

from contextlib import redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SOURCE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("workflow_setup", SOURCE / "setup.py")
SETUP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SETUP)


def copy_source(destination):
    """Use distribution files only, never the developer's local project facts."""
    def ignore(directory, names):
        if Path(directory) == SOURCE / "projects":
            return set(names) - {"index.example.md", "project.example.md"}
        return {".git", "__pycache__"}
    shutil.copytree(SOURCE, destination, ignore=ignore)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="copilot-workflow-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "home with spaces caf\u00e9 \u5de5\u4f5c"
        self.source = self.root / "distribution"
        copy_source(self.source)

    def install(self, source=None, check=False):
        with redirect_stdout(io.StringIO()):
            return SETUP.install(source or self.source, self.home, check)

    def configure(self, names, source=None):
        source = source or self.source
        table = (source / "projects/index.example.md").read_text(encoding="utf-8")
        separator = "| --- | --- | --- | --- | --- |"
        rows = "\n".join(f"| {name} | fixture | github.example.com/org/repo | ABC | (unset) |"
                         for name in names)
        (source / "projects/index.md").write_text(
            table.replace(separator, separator + "\n" + rows), encoding="utf-8", newline="\n")
        for name in names:
            (source / "projects" / name).write_text(
                "Configuration status: READY\nFixture " + name + "\n", encoding="utf-8", newline="\n")

    def test_install_is_repeatable_and_preserves_unrelated_configuration(self):
        copilot = self.home / ".copilot"
        copilot.mkdir(parents=True)
        unrelated = copilot / "mcp-config.json"
        unrelated.write_text('{"unrelated":true}', encoding="utf-8")
        work = self.home / "work" / "company-repo"
        work.mkdir(parents=True)
        (work / "tracked.txt").write_text("original", encoding="utf-8")
        preserved = {
            "work/company-repo/AGENTS.md": b"Repository guidance",
            "work/company-repo/.github/copilot-instructions.md": b"Team defaults",
            "work/company-repo/.github/instructions/api.instructions.md": b"API rules",
            "work/company-repo/.github/skills/implementation/SKILL.md": b"Repository skill",
            ".copilot/skills/karpathy/SKILL.md": b"Third-party skill",
            ".agents/skills/another/SKILL.md": b"Shared skill",
            ".copilot/instructions/other.instructions.md": b"Other defaults",
            ".copilot/settings.json": b"Existing settings",
            ".vscode/settings.json": b"Editor configuration",
            ".copilot/personal-workflow/unrelated.md": b"Unowned legacy neighbor",
        }
        for relative, data in preserved.items():
            path = self.home / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.assertEqual(self.install(), 0)
        before = {p.relative_to(self.home): p.read_bytes()
                  for p in self.home.rglob("*") if p.is_file()}
        self.assertEqual(self.install(), 0)
        after = {p.relative_to(self.home): p.read_bytes()
                 for p in self.home.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(unrelated.read_text(), '{"unrelated":true}')
        self.assertEqual((work / "tracked.txt").read_text(), "original")
        for relative, data in preserved.items():
            self.assertEqual((self.home / relative).read_bytes(), data)
        self.assertEqual(self.install(check=True), 0)

    def test_check_on_missing_install_writes_nothing(self):
        self.assertEqual(self.install(check=True), 1)
        self.assertFalse(self.home.exists())

    def test_existing_baseline_blocks_all_writes(self):
        existing = self.home / ".copilot/copilot-instructions.md"
        existing.parent.mkdir(parents=True)
        existing.write_text("Keep my existing instructions", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "No files changed"):
            self.install()
        self.assertEqual(existing.read_text(), "Keep my existing instructions")
        self.assertFalse((self.home / ".copilot/skills").exists())

    def test_locally_edited_skill_blocks_update(self):
        self.install()
        target = self.home / ".copilot/skills/prepare-pr/SKILL.md"
        target.write_text("A local edit to preserve", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "locally edited"):
            self.install()
        self.assertEqual(target.read_text(), "A local edit to preserve")

    def test_existing_same_name_skill_blocks_fresh_install_without_writes(self):
        target = self.home / ".copilot/skills/implementation/SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"Existing third-party implementation skill")
        before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
        for check in (True, False):
            with self.assertRaisesRegex(ValueError, "No files changed"):
                self.install(check=check)
            self.assertEqual(before, {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()})

    def test_new_planning_files_upgrade_an_existing_install(self):
        source = self.root / "private clone"
        copy_source(source)
        additions = {
            "skills/planning/SKILL.md": ".copilot/skills/planning/SKILL.md",
            "writing/examples/plan.md": ".copilot/engineering-workflow/writing/examples/plan.md",
        }
        for relative in additions:
            (source / relative).unlink()
        self.assertEqual(self.install(source), 0)
        for relative, destination in additions.items():
            self.assertFalse((self.home / destination).exists())
            shutil.copyfile(SOURCE / relative, source / relative)
        self.assertEqual(self.install(source, check=True), 1)
        self.assertEqual(self.install(source), 0)
        self.assertEqual(self.install(source, check=True), 0)
        installed = self.home / additions["skills/planning/SKILL.md"]
        self.assertIn("# Planning", installed.read_text(encoding="utf-8"))
        self.assertNotIn("{{", installed.read_text(encoding="utf-8"))
        self.assertEqual(
            (self.home / additions["writing/examples/plan.md"]).read_bytes(),
            (SOURCE / "writing/examples/plan.md").read_bytes(),
        )
        self.assertEqual(
            list(self.home.rglob("plan.md")),
            [self.home / additions["writing/examples/plan.md"]],
        )  # Setup installs a writing example, not a project plan.

    def test_active_projects_and_updates_install_only_referenced_files(self):
        self.install()  # Upgrade the generated empty state to one real profile.
        for names in (["sre-api.md"], ["sre-api.md", "portal-ui.md", "reporting.md"]):
            self.configure(names)
            (self.source / "projects/unused.md").write_bytes(b"Private unused fixture")
            self.assertEqual(self.install(check=True), 1)
            self.assertEqual(self.install(), 0)
            installed = self.home / ".copilot/engineering-workflow/projects"
            self.assertEqual({p.name for p in installed.iterdir()}, {"index.md", *names})
            for name in ("index.md", *names):
                self.assertEqual((installed / name).read_bytes(),
                                 (self.source / "projects" / name).read_bytes())
            self.assertEqual(self.install(check=True), 0)
        profile = self.source / "projects/sre-api.md"
        profile.write_bytes(b"Configuration status: UNCONFIGURED\nRevised fixture\n")
        self.assertEqual(self.install(check=True), 1)
        self.assertEqual(self.install(), 0)
        self.assertEqual((installed / profile.name).read_bytes(), profile.read_bytes())
        self.assertEqual(self.install(check=True), 0)

    def test_fresh_clone_installs_explicit_empty_state_without_writing_source(self):
        before = {p: p.read_bytes() for p in self.source.rglob("*") if p.is_file()}
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(SETUP.install(self.source, self.home), 0)
        self.assertIn("not initialized", output.getvalue())
        self.assertIn("projects/index.example.md", output.getvalue())
        projects = self.home / ".copilot/engineering-workflow/projects"
        self.assertEqual([p.name for p in projects.iterdir()], ["index.md"])
        self.assertIn("Configuration status: UNCONFIGURED", (projects / "index.md").read_text())
        self.assertEqual(self.install(check=True), 0)
        self.assertEqual(before, {p: p.read_bytes() for p in self.source.rglob("*") if p.is_file()})

    def test_empty_local_index_and_duplicate_backtick_references(self):
        self.configure([])
        self.assertEqual(self.install(), 0)
        self.configure(["sre-api.md"])
        index = self.source / "projects/index.md"
        index.write_text(index.read_text(encoding="utf-8").replace("| sre-api.md |", "| `sre-api.md` |")
                         + "\n| sre-api.md | another alias | host/repo | ABC | (unset) |\n",
                         encoding="utf-8")
        self.assertEqual(self.install(), 0)
        self.assertEqual(self.install(check=True), 0)
        self.assertEqual(len(list((self.home / ".copilot/engineering-workflow/projects").iterdir())), 2)

    def test_invalid_index_or_profile_preflights_before_writes(self):
        self.configure(["sre-api.md"])
        index = self.source / "projects/index.md"
        original = index.read_text(encoding="utf-8")
        invalid = ["../outside.md", "sub/profile.md", "/absolute.md", "C:/outside.md",
                   r"..\outside.md", "project.example.md", "PROJECT.EXAMPLE.md", "index.md",
                   "README.md", "CON.md", "file:stream.md", "profile.MD", "absent.md",
                   "SRE-API.md", "[profile](sre-api.md)"]
        for reference in invalid:
            index.write_text(original.replace("| sre-api.md |", "| " + reference + " |"), encoding="utf-8")
            for check in (True, False):
                with self.subTest(reference=reference, check=check):
                    with self.assertRaisesRegex(ValueError, "Invalid project configuration"):
                        self.install(check=check)
                    self.assertFalse(self.home.exists())
        for malformed in ("", "# No table\n", original.replace("| Profile |", "| File |"),
                          original.replace("| sre-api.md |", "| sre-api.md | extra |"),
                          original.replace("| sre-api.md |", "sre-api.md |"),
                          original.replace("| --- | --- | --- | --- | --- |", "| --- |"),
                          original + "\n| broken row\n"):
            index.write_text(malformed, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Invalid project configuration"):
                self.install()
            self.assertFalse(self.home.exists())

    def test_unreadable_index_and_linked_source_are_not_unconfigured_fallbacks(self):
        self.configure(["sre-api.md"])
        index = self.source / "projects/index.md"
        original = SETUP.render
        def unreadable(path, root):
            if path == index:
                raise PermissionError("fixture denial")
            return original(path, root)
        with patch.object(SETUP, "render", side_effect=unreadable):
            with self.assertRaisesRegex(ValueError, "fixture denial"):
                self.install()
        for relative in ("projects", "projects/index.md", "projects/sre-api.md"):
            with patch.object(Path, "is_junction", autospec=True,
                              side_effect=lambda path: path == self.source / relative):
                with self.assertRaisesRegex(ValueError, "linked install path"):
                    self.install()
        self.assertFalse(self.home.exists())

    def test_profile_rename_and_removal_require_explicit_owned_cleanup(self):
        self.configure(["sre-api.md"])
        self.install()
        installed = self.home / ".copilot/engineering-workflow/projects"
        old = installed / "sre-api.md"
        old.write_bytes(b"Installed edit to preserve")
        neighbor = installed / "unowned.md"
        neighbor.write_bytes(b"Unowned neighbor")
        self.configure(["portal-ui.md"])
        for obsolete in ("sre-api.md", "portal-ui.md"):
            before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
            for check in (True, False):
                with self.assertRaisesRegex(ValueError, "removed from source"):
                    self.install(check=check)
                self.assertEqual(before, {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()})
            (installed / obsolete).unlink()
            # Even an already removed file still needs its manifest entry handled.
            with self.assertRaisesRegex(ValueError, "removed from source"):
                self.install()
            manifest = installed.parent / "install-manifest.json"
            entries = json.loads(manifest.read_text(encoding="utf-8"))
            del entries[".copilot/engineering-workflow/projects/" + obsolete]
            manifest.write_text(json.dumps(entries), encoding="utf-8")
            self.assertEqual(self.install(), 0)
            self.assertEqual(self.install(check=True), 0)
            self.assertEqual(neighbor.read_bytes(), b"Unowned neighbor")
            # Missing source index after configuration selects empty state,
            # but may not silently discard the previously owned profile.
            (self.source / "projects/index.md").unlink(missing_ok=True)

    def test_installed_index_and_profile_edits_block_updates(self):
        self.configure(["sre-api.md"])
        self.install()
        for name in ("index.md", "sre-api.md"):
            target = self.home / ".copilot/engineering-workflow/projects" / name
            original = target.read_bytes()
            target.write_bytes(b"Preserve installed edit")
            for check in (True, False):
                with self.assertRaisesRegex(ValueError, "locally edited"):
                    self.install(check=check)
            target.write_bytes(original)

    def test_profile_case_aliases_are_rejected_before_writes(self):
        self.configure(["sre-api.md"])
        index = self.source / "projects/index.md"
        index.write_text(index.read_text(encoding="utf-8")
                         + "\n| SRE-API.md | alias | host/repo | ABC | (unset) |\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "collide across platforms"):
            self.install()
        self.assertFalse(self.home.exists())

    def test_portable_profile_names_and_bom_newlines(self):
        names = ["service_2.md", "my service.md", "caf\u00e9.md"]
        self.configure(names)
        for path in (self.source / "projects").glob("*.md"):
            content = path.read_text(encoding="utf-8")
            path.write_bytes(b"\xef\xbb\xbf" + content.replace("\n", "\r\n").encode("utf-8"))
        self.assertEqual(self.install(), 0)
        self.assertEqual(self.install(check=True), 0)
        installed = self.home / ".copilot/engineering-workflow/projects"
        for name in ("index.md", *names):
            actual = (installed / name).read_bytes()
            self.assertFalse(actual.startswith(b"\xef\xbb\xbf"))
            self.assertNotIn(b"\r", actual)

    def test_invalid_project_configuration_cli_returns_actionable_error(self):
        self.configure(["sre-api.md"])
        (self.source / "projects/sre-api.md").unlink()
        env = os.environ.copy()
        env.pop("COPILOT_HOME", None)
        for option in ([], ["--check"]):
            result = subprocess.run([sys.executable, str(self.source / "setup.py"),
                                     "--home", str(self.home), *option], cwd=self.root,
                                    env=env, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn(b"sre-api.md", result.stderr)
            self.assertIn(b"create it from project.example.md or correct the index row", result.stderr)
            self.assertFalse(self.home.exists())

    def test_git_ignores_local_configuration_and_pull_preserves_it(self):
        upstream = self.root / "upstream"
        upstream.mkdir()
        def git(directory, *args):
            return subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                                   "-c", "core.autocrlf=false", *args], cwd=directory,
                                  capture_output=True, check=True).stdout
        git(upstream, "init")
        shutil.copyfile(SOURCE / ".gitignore", upstream / ".gitignore")
        shutil.copytree(self.source / "projects", upstream / "projects")
        git(upstream, "add", ".")
        git(upstream, "commit", "-m", "Generic distribution fixture")
        clone = self.root / "local clone"
        git(self.root, "clone", str(upstream), str(clone))
        ignored = ["projects/index.md", "projects/foo.md", "projects/sre-api.md", "projects/my-project.md"]
        for relative in ignored:
            (clone / relative).write_bytes(b"Private local fixture")
        paths = ignored + ["projects/index.example.md", "projects/project.example.md", "projects/docs/guide.md"]
        result = git(clone, "check-ignore", "--no-index", *paths).decode().splitlines()
        self.assertEqual(result, ignored)
        tracked = git(clone, "ls-files", "projects").decode().splitlines()
        self.assertEqual(tracked, ["projects/index.example.md", "projects/project.example.md"])
        self.assertEqual(git(clone, "status", "--porcelain"), b"")
        (upstream / "projects/project.example.md").write_bytes(b"Updated generic template\n")
        git(upstream, "add", ".")
        git(upstream, "commit", "-m", "Template update fixture")
        git(clone, "pull", "--ff-only")
        for relative in ignored:
            self.assertEqual((clone / relative).read_bytes(), b"Private local fixture")
        self.assertEqual((clone / "projects/project.example.md").read_bytes(), b"Updated generic template\n")
        self.assertEqual(git(clone, "status", "--porcelain"), b"")

    def test_legacy_migration_preserves_ownership_and_requires_explicit_cleanup(self):
        # Recreate the preceding installer's destination contract, independent of
        # the new path builder. Existing same-name skill ownership must survive.
        legacy_files = {
            ".copilot/copilot-instructions.md": b"Old baseline",
            ".copilot/personal-workflow/baseline.md": b"Old baseline",
            ".copilot/personal-workflow/app-instructions.md": b"Old baseline",
            ".copilot/instructions/personal-workflow.instructions.md": b"Old bridge",
            ".copilot/personal-workflow/projects/index.md": b"Old index",
            ".copilot/skills/prepare-pr/SKILL.md": b"Old owned skill",
        }
        for relative, data in legacy_files.items():
            path = self.home / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        entries = {p: SETUP.digest(b) for p, b in legacy_files.items()}
        legacy = self.home / ".copilot/personal-workflow/install-manifest.json"
        legacy.write_text(json.dumps(entries), encoding="utf-8")
        before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
        for check in (True, False):
            with self.assertRaisesRegex(ValueError, "Legacy ownership manifest"):
                self.install(check=check)
            self.assertEqual(before, {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()})
        manifest = self.home / ".copilot/engineering-workflow/install-manifest.json"
        manifest.parent.mkdir()
        manifest.write_bytes(b"{}")
        with self.assertRaisesRegex(ValueError, "If both exist"):
            self.install()
        self.assertEqual(manifest.read_bytes(), b"{}")
        manifest.unlink()
        legacy.rename(manifest)  # Simulate the documented maintainer migration.
        with self.assertRaisesRegex(ValueError, "removed from source"):
            self.install()
        obsolete = set(entries) - {".copilot/copilot-instructions.md", ".copilot/skills/prepare-pr/SKILL.md"}
        # A local edit to an obsolete file is retained until the user handles it.
        edited = self.home / ".copilot/personal-workflow/baseline.md"
        edited.write_bytes(b"Preserve these local notes")
        with self.assertRaisesRegex(ValueError, "removed from source"):
            self.install()
        self.assertEqual(edited.read_bytes(), b"Preserve these local notes")
        for relative in obsolete:
            (self.home / relative).unlink()
            del entries[relative]
        manifest.write_text(json.dumps(entries), encoding="utf-8")
        self.assertEqual(self.install(check=True), 1)
        self.assertEqual(self.install(), 0)
        self.assertEqual(self.install(check=True), 0)
        self.assertFalse((self.home / ".copilot/instructions/personal-workflow.instructions.md").exists())
        self.assertTrue((self.home / ".copilot/instructions/engineering-workflow.instructions.md").exists())

    def test_unrecorded_legacy_bridge_blocks_duplicate_activation(self):
        legacy = self.home / ".copilot/instructions/personal-workflow.instructions.md"
        legacy.parent.mkdir(parents=True)
        legacy.write_bytes(b"Unrecorded old bridge")
        with self.assertRaisesRegex(ValueError, "no ownership record"):
            self.install()
        self.assertEqual(legacy.read_bytes(), b"Unrecorded old bridge")
        self.assertFalse((self.home / ".copilot/copilot-instructions.md").exists())

    def test_canonical_update_and_new_example_are_installed(self):
        source = self.root / "private clone"
        copy_source(source)
        self.install(source)
        style = source / "writing/style.md"
        style.write_text(style.read_text(encoding="utf-8") + "\nPrefer concrete verbs.\n", encoding="utf-8")
        review = source / "skills/implementation-review/SKILL.md"
        review.write_text(review.read_text(encoding="utf-8") + "\nReview fixture update.\n", encoding="utf-8")
        baseline = source / "instructions/baseline.md"
        baseline.write_text(baseline.read_text(encoding="utf-8") + "\nBaseline fixture update.\n", encoding="utf-8")
        untouched = self.home / ".copilot/skills/jira-story/SKILL.md"
        untouched_bytes = untouched.read_bytes()
        example = source / "writing/examples/installation-fixture.md"
        example.write_bytes(b"Illustrative installation fixture\n")
        self.assertEqual(self.install(source, check=True), 1)
        self.assertEqual(self.install(source), 0)
        installed = self.home / ".copilot/engineering-workflow/writing/style.md"
        self.assertTrue(installed.read_text(encoding="utf-8").endswith("Prefer concrete verbs.\n"))
        installed_review = self.home / ".copilot/skills/implementation-review/SKILL.md"
        self.assertTrue(installed_review.read_bytes().endswith(b"Review fixture update.\n"))
        for relative in (".copilot/copilot-instructions.md",):
            with self.subTest(relative=relative):
                self.assertTrue((self.home / relative).read_bytes().endswith(b"Baseline fixture update.\n"))
        self.assertEqual(untouched.read_bytes(), untouched_bytes)
        installed_example = self.home / ".copilot/engineering-workflow/writing/examples" / example.name
        self.assertEqual(installed_example.read_bytes(), example.read_bytes())
        self.assertEqual(self.install(source, check=True), 0)

    def test_removed_source_is_not_silently_left_active(self):
        source = self.root / "private clone"
        copy_source(source)
        self.install(source)
        (source / "skills/jira-story/SKILL.md").unlink()
        with self.assertRaisesRegex(ValueError, "removed from source"):
            self.install(source)

    def test_paths_render_and_surface_adapters_reference_shared_baseline(self):
        self.install()
        root = self.home / ".copilot/engineering-workflow"
        skill = (self.home / ".copilot/skills/jira-story/SKILL.md").read_text(encoding="utf-8")
        self.assertIn(root.as_posix() + "/projects/index.md", skill)
        self.assertNotIn("{{WORKFLOW_ROOT}}", skill)
        baseline = self.home / ".copilot/copilot-instructions.md"
        self.assertFalse((root / "baseline.md").exists())
        self.assertFalse((root / "app-instructions.md").exists())
        adapter = (self.home / ".copilot/instructions/engineering-workflow.instructions.md").read_text(encoding="utf-8")
        self.assertTrue(adapter.startswith('---\napplyTo: "**"\n---\n'))
        self.assertIn(baseline.as_posix(), adapter)
        self.assertFalse((root / "vscode-settings.json").exists())
        self.assertFalse((root / "README.md").exists())
        self.assertFalse((root / "DESIGN.md").exists())
        review = self.home / ".copilot/skills/implementation-review/SKILL.md"
        self.assertTrue(review.is_file())
        self.assertIn(baseline.as_posix(), review.read_text(encoding="utf-8"))

    def test_path_escape_is_rejected(self):
        self.home.mkdir()
        for relative in ("../outside.txt", "/absolute.txt", "C:/outside.txt",
                         "C:relative.txt", "\\\\server\\share\\file", "a\\..\\outside",
                         "a/./b", "a//b", "a/CON.md", "a/file:stream", "a/file.", "a/file "):
            with self.subTest(relative=relative):
                with self.assertRaisesRegex(ValueError, "Invalid install path"):
                    SETUP.safe_target(self.home.resolve(), relative)

    def test_source_newlines_and_bom_produce_identical_utf8_lf(self):
        source = self.root / "private clone"
        copy_source(source)
        self.install(source)
        before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
        for path in source.rglob("*.md"):
            text = path.read_text(encoding="utf-8-sig")
            path.write_bytes(b"\xef\xbb\xbf" + text.replace("\n", "\r\n").encode("utf-8"))
        self.assertEqual(self.install(source, check=True), 0)
        for path, data in before.items():
            self.assertNotIn(b"\r", data)
            self.assertFalse(data.startswith(b"\xef\xbb\xbf"))
            self.assertEqual(path.read_bytes(), data)

    def test_installed_newline_edit_is_preserved_as_drift(self):
        self.install()
        target = self.home / ".copilot/engineering-workflow/writing/style.md"
        changed = target.read_bytes().replace(b"\n", b"\r\n")
        target.write_bytes(changed)
        for check in (True, False):
            with self.subTest(check=check):
                with self.assertRaisesRegex(ValueError, "locally edited"):
                    self.install(check=check)
                self.assertEqual(target.read_bytes(), changed)

    def test_missing_or_stale_manifest_entries_are_detected_and_repaired(self):
        self.install()
        manifest = self.home / ".copilot/engineering-workflow/install-manifest.json"
        for contents in ({}, {".copilot/copilot-instructions.md": "0" * 64}):
            with self.subTest(contents=contents):
                manifest.write_text(json.dumps(contents), encoding="utf-8")
                before = manifest.read_bytes()
                self.assertEqual(self.install(check=True), 1)
                self.assertEqual(manifest.read_bytes(), before)
                self.assertEqual(self.install(), 0)
                self.assertEqual(self.install(check=True), 0)

    def test_malformed_manifest_blocks_writes(self):
        manifest = self.home / ".copilot/engineering-workflow/install-manifest.json"
        manifest.parent.mkdir(parents=True)
        for contents in ('{"broken":', '[]', '{"x": 1}', '{"x": "bad hash"}',
                         json.dumps({"../outside": "0" * 64})):
            with self.subTest(contents=contents):
                manifest.write_text(contents, encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.install()
                self.assertEqual(manifest.read_text(encoding="utf-8"), contents)
                self.assertFalse((self.home / ".copilot/skills").exists())

    def test_colliding_sources_fail_before_writes_on_every_os(self):
        # Simulate a case-sensitive source checkout on either host filesystem.
        source = self.root / "private clone"
        for first, second in (("prepare-pr", "PREPARE-PR"), ("caf\u00e9", "cafe\u0301")):
            with self.subTest(first=first, second=second):
                with patch.object(Path, "rglob", autospec=True) as glob:
                    def paths(directory, pattern, **kwargs):
                        if directory == source / "skills":
                            return [source / "skills" / first / "SKILL.md",
                                    source / "skills" / second / "extra.md"]
                        return []
                    glob.side_effect = paths
                    with patch.object(SETUP, "render", return_value=b"content"):
                        with self.assertRaisesRegex(ValueError, "collide across platforms"):
                            self.install(source)
        self.assertFalse(self.home.exists())

    def test_markdown_extension_selection_is_case_sensitive_on_every_os(self):
        source = self.root / "private clone"
        copy_source(source)
        (source / "writing/examples/not-selected.MD").write_text("human notes", encoding="utf-8")
        self.install(source)
        self.assertFalse((self.home / ".copilot/engineering-workflow/writing/examples/not-selected.MD").exists())

    def test_failed_replace_preserves_original_and_cleans_temporary_file(self):
        target = self.root / "owned.md"
        target.write_bytes(b"original")
        with patch.object(SETUP.os, "replace", side_effect=PermissionError("file in use")):
            with self.assertRaises(PermissionError):
                SETUP.write_atomic(target, b"new")
        self.assertEqual(target.read_bytes(), b"original")
        self.assertEqual(set(self.root.iterdir()), {self.source, target})

    def test_interrupted_update_can_be_checked_and_rerun(self):
        source = self.root / "private clone"
        copy_source(source)
        self.install(source)
        baseline = source / "instructions/baseline.md"
        baseline.write_bytes(baseline.read_bytes() + b"\nNew source instruction.\n")
        real_write = SETUP.write_atomic
        calls = 0

        def interrupt(path, data):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("interrupted")
            real_write(path, data)

        with patch.object(SETUP, "write_atomic", side_effect=interrupt):
            with self.assertRaisesRegex(OSError, "interrupted"):
                self.install(source)
        self.assertEqual(self.install(source, check=True), 1)
        self.assertEqual(self.install(source), 0)
        self.assertEqual(self.install(source, check=True), 0)

    def test_legacy_vscode_adapter_requires_explicit_cleanup(self):
        self.install()
        root = self.home / ".copilot/engineering-workflow"
        legacy = root / "vscode-settings.json"
        legacy.write_bytes(b"{}\n")
        manifest = root / "install-manifest.json"
        entries = json.loads(manifest.read_text(encoding="utf-8"))
        relative = legacy.relative_to(self.home).as_posix()
        entries[relative] = SETUP.digest(legacy.read_bytes())
        manifest.write_text(json.dumps(entries), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "removed from source"):
            self.install()
        self.assertEqual(legacy.read_bytes(), b"{}\n")
        legacy.unlink()
        del entries[relative]
        manifest.write_text(json.dumps(entries), encoding="utf-8")
        self.assertEqual(self.install(), 0)

    def test_cli_works_from_another_directory_without_a_shell(self):
        env = os.environ.copy()
        env.pop("COPILOT_HOME", None)
        env["PYTHONIOENCODING"] = "ascii:strict"

        def run(*args):
            return subprocess.run([sys.executable, str(self.source / "setup.py"),
                                   "--home", str(self.home), *args], cwd=self.root,
                                  env=env, capture_output=True)

        self.assertEqual(run("--check").returncode, 1)
        self.assertFalse(self.home.exists())
        self.assertEqual(run().returncode, 0)
        self.assertEqual(run("--check").returncode, 0)
        env["COPILOT_HOME"] = str(self.home / ".copilot")
        self.assertEqual(run("--check").returncode, 0)
        env["COPILOT_HOME"] = str(self.root / "different config")
        result = run()
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"COPILOT_HOME differs", result.stderr)
        self.assertFalse((self.root / "different config").exists())

    def test_junction_detection_blocks_writes_without_requiring_link_privileges(self):
        junction = self.home / ".copilot"
        with patch.object(Path, "is_junction", autospec=True,
                          side_effect=lambda path: path == junction):
            with self.assertRaisesRegex(ValueError, "linked install path"):
                self.install()
        self.assertFalse(self.home.exists())

    def test_file_in_parent_path_blocks_all_writes(self):
        copilot = self.home / ".copilot"
        copilot.mkdir(parents=True)
        (copilot / "skills").write_text("preserve this file", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "parent is not a directory"):
            self.install()
        self.assertFalse((copilot / "copilot-instructions.md").exists())

    def test_linked_copilot_directory_is_rejected(self):
        self.home.mkdir()
        elsewhere = self.root / "elsewhere"
        elsewhere.mkdir()
        try:
            (self.home / ".copilot").symlink_to(elsewhere, target_is_directory=True)
        except OSError:
            self.skipTest("This account cannot create symlinks")
        with self.assertRaisesRegex(ValueError, "linked install path"):
            self.install()
        self.assertEqual(list(elsewhere.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
