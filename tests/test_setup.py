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
            return set(names) - {"project.example.md"}
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

    def uninstall(self):
        with redirect_stdout(io.StringIO()):
            return SETUP.uninstall(self.home)

    def status(self, source=None):
        output = io.StringIO()
        with redirect_stdout(output):
            result = SETUP.status(source or self.source, self.home)
        return result, output.getvalue()

    def configure(self, names, source=None):
        source = source or self.source
        for number, name in enumerate(names):
            (source / "projects" / name).write_text(
                f"# Fixture {number}\n\nConfiguration status: READY\n\n## Routing\n\n"
                f"- Project: Project {number}\n"
                f"- Git remote: git.test/team/service{number}\n"
                f"- Jira prefix: ABC{number}\n\n## Connections\n\n"
                "- GitHub MCP connection: github-fixture\n"
                "- Jira MCP connection: jira-fixture\n"
                "- Jira site: https://jira.test\n\n## Pull requests\n\n"
                f"- Reviewers: reviewer{number}, backup{number}\n", encoding="utf-8", newline="\n")

    def test_fresh_clone_and_unconfigured_profiles_do_not_write_source(self):
        draft = self.source / "projects/draft.md"
        shutil.copyfile(self.source / "projects/project.example.md", draft)
        before = {p: p.read_bytes() for p in self.source.rglob("*") if p.is_file()}
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(SETUP.install(self.source, self.home), 0)
        self.assertIn("No READY projects", output.getvalue())
        self.assertIn("Skipping UNCONFIGURED profile: draft.md", output.getvalue())
        projects = self.home / ".copilot/engineering-workflow/projects"
        self.assertEqual([p.name for p in projects.iterdir()], ["index.md"])
        self.assertIn("Configuration status: UNCONFIGURED", (projects / "index.md").read_text())
        self.assertNotIn("Copy", (projects / "index.md").read_text())
        self.assertEqual(self.install(check=True), 0)
        self.assertEqual(before, {p: p.read_bytes() for p in self.source.rglob("*") if p.is_file()})

    def test_generated_index_matches_any_number_of_ready_profiles_and_updates(self):
        self.install()
        for names in (["sre-api.md"], ["sre-api.md", "portal.md", "navigator.md"],
                      ["sre-api.md", "portal.md", "navigator.md", *[f"service-{i}.md" for i in range(9)]]):
            self.configure(names)
            self.assertFalse((self.source / "projects/index.md").exists())
            self.assertEqual(self.install(check=True), 1)
            self.assertEqual(self.install(), 0)
            installed = self.home / ".copilot/engineering-workflow/projects"
            self.assertEqual({p.name for p in installed.iterdir()}, {"index.md", *names})
            index = (installed / "index.md").read_text(encoding="utf-8")
            expected_rows = [f"| {name} | Project {i} | git.test/team/service{i} | ABC{i} | unset |"
                             for i, name in enumerate(names)]
            self.assertEqual(index.splitlines()[6:], sorted(expected_rows))
            self.assertNotIn("github-fixture", index)
            for name in names:
                self.assertEqual((installed / name).read_bytes(), (self.source / "projects" / name).read_bytes())
                self.assertIn("- Reviewers: reviewer", (installed / name).read_text(encoding="utf-8"))
            self.assertEqual(self.install(check=True), 0)
        profile = self.source / "projects/sre-api.md"
        profile.write_text(profile.read_text(encoding="utf-8").replace("Project 0", "Service API"), encoding="utf-8")
        self.assertEqual(self.install(check=True), 1)
        self.assertEqual(self.install(), 0)
        self.assertIn("| sre-api.md | Service API |", (installed / "index.md").read_text())
        self.assertEqual(self.install(check=True), 0)

    def test_routing_errors_block_install_and_check_before_writes(self):
        self.configure(["sre-api.md"])
        profile = self.source / "projects/sre-api.md"
        original = profile.read_text(encoding="utf-8")
        bad = [
            ("Configuration status: READY", ""),
            ("Configuration status: READY", "Configuration status: ready"),
            ("Configuration status: READY", "Configuration status: READY\nConfiguration status: READY"),
            ("## Routing", "## Routes"),
            ("## Connections", "## Routing"),
            ("- Project: Project 0", ""),
            ("- Project: Project 0", "- Project: Project 0\n- Project: Another"),
            ("- Project: Project 0", "- Aliases: Project 0"),
            ("- Jira prefix: ABC0", ""),
            ("- Jira prefix: ABC0", "- Jira prefix: abc"),
            ("- Jira prefix: ABC0", "- Jira prefix: ABC0\n- Jira prefix: ABC1"),
            ("- Jira prefix: ABC0", "- Jira project: ABC0"),
            ("- Project: Project 0", "- Project: unset"),
            ("- Project: Project 0", "- Project: api|portal"),
            ("git.test/team/service0", "https://git.test/team/service0"),
            ("git.test/team/service0", "git@host:team/service0"),
            ("git.test/team/service0", "https://user:private-token@git.test/team/service0"),
            ("git.test/team/service0", "host/../service"),
            ("git.test/team/service0", "host/team/.git"),
            ("git.test/team/service0", "host/team/..git"),
            ("git.test/team/service0", "<GIT-HOST>/<ORG>/<REPOSITORY>"),
            ("github-fixture", "<github-mcp-connection>"),
            ("https://jira.test", "https://jira.example.com"),
            ("- Jira prefix: ABC0", "- Jira prefix: ABC0\n- Local root: relative/path"),
        ]
        for old, new in bad:
            profile.write_text(original.replace(old, new), encoding="utf-8")
            for check in (False, True):
                with self.subTest(old=old, new=new, check=check):
                    with self.assertRaisesRegex(ValueError, "Invalid project profile") as error:
                        self.install(check=check)
                    self.assertNotIn("private-token", str(error.exception))
                    self.assertFalse(self.home.exists())
        profile.write_text(original.replace("git.test/team/service0", "unset").replace("ABC0", "unset"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Supply a Git remote or Jira prefix"):
            self.install()

    def test_duplicate_project_names_and_remote_identities_are_rejected(self):
        self.configure(["sre-api.md", "portal.md"])
        first = self.source / "projects/sre-api.md"
        second = self.source / "projects/portal.md"
        original = second.read_text(encoding="utf-8")
        replacements = [("Project 1", "PROJECT 0"),
                        ("git.test/team/service1", "GIT.TEST/TEAM/SERVICE0.git")]
        for old, new in replacements:
            second.write_text(original.replace(old, new), encoding="utf-8")
            for check in (False, True):
                with self.assertRaisesRegex(ValueError, "Duplicate"):
                    self.install(check=check)
                self.assertFalse(self.home.exists())
        first.write_text(first.read_text(encoding="utf-8").replace("Project 0", "caf\u00e9"), encoding="utf-8")
        second.write_text(original.replace("Project 1", "cafe\u0301"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate project"):
            self.install()

    def test_shared_jira_prefix_and_sparse_git_or_jira_routing(self):
        self.configure(["sre-api.md", "portal.md"])
        profile = self.source / "projects/portal.md"
        original = profile.read_text(encoding="utf-8").replace("ABC1", "ABC0")
        profile.write_text(original, encoding="utf-8")
        self.assertEqual(self.install(), 0)
        self.assertEqual(self.install(check=True), 0)
        for remote, prefix in (("unset", "ABC0"), ("git.test/team/service1", "unset")):
            profile.write_text(original.replace("git.test/team/service1", remote).replace("ABC0", prefix), encoding="utf-8")
            self.assertEqual(self.install(), 0)
            self.assertEqual(self.install(check=True), 0)

    def test_optional_absolute_roots_and_title_tokens(self):
        self.configure(["sre-api.md"])
        profile = self.source / "projects/sre-api.md"
        original = profile.read_text(encoding="utf-8")
        for root in (r"C:\Work\Service", "/Users/fixture/work/service", "unset"):
            profile.write_text(original.replace("## Connections", "- Local root: `" + root + "`\n\n## Connections")
                               + "\nPR title: `[<JIRA-KEY>] <JIRA-SUMMARY>`\n", encoding="utf-8")
            self.assertEqual(self.install(), 0)
            self.assertEqual(self.install(check=True), 0)
            index = self.home / ".copilot/engineering-workflow/projects/index.md"
            self.assertIn(root.replace("\\", "\\\\"), index.read_text())

    def test_ready_profiles_reject_exact_template_placeholders(self):
        self.configure(["sre-api.md"])
        profile = self.source / "projects/sre-api.md"
        original = profile.read_text(encoding="utf-8")
        template = self.source / "projects/project.example.md"
        template.write_bytes(template.read_bytes() + b"\nPrivate field: <NEW-TEMPLATE-FIELD>\n")
        for token in ("<PROJECT-NAME>", "<github-mcp-connection>", "<JIRA-HOST>", "<NEW-TEMPLATE-FIELD>"):
            profile.write_text(original + "\n" + token + "\n", encoding="utf-8")
            for check in (False, True):
                with self.subTest(token=token, check=check):
                    with self.assertRaisesRegex(ValueError, "template placeholders"):
                        self.install(check=check)
                    self.assertFalse(self.home.exists())

    def test_ready_profiles_allow_free_markdown_and_convention_tokens(self):
        self.configure(["sre-api.md"])
        profile = self.source / "projects/sre-api.md"
        prose = ("\n## Conventions\n\n<details>\n<summary>Title format</summary>\n\n"
                 "Use `[<JIRA-KEY>] <JIRA-SUMMARY>` or `<SUMMARY>`.\n\n"
                 "Literal documentation token: `<service-name>`.\n</details>\n")
        profile.write_text(profile.read_text(encoding="utf-8") + prose, encoding="utf-8")
        self.assertEqual(self.install(), 0)
        self.assertEqual(self.install(check=True), 0)
        installed = self.home / ".copilot/engineering-workflow/projects/sre-api.md"
        self.assertEqual(installed.read_text(encoding="utf-8"), profile.read_text(encoding="utf-8"))

    def test_unreadable_profiles_and_linked_sources_fail(self):
        self.configure(["sre-api.md"])
        profile = self.source / "projects/sre-api.md"
        original_read = Path.read_text
        def unreadable(path, *args, **kwargs):
            if path == profile:
                raise PermissionError("fixture denial")
            return original_read(path, *args, **kwargs)
        with patch.object(Path, "read_text", autospec=True, side_effect=unreadable):
            with self.assertRaisesRegex(ValueError, "fixture denial"):
                self.install()
        for relative in ("projects", "projects/sre-api.md"):
            with patch.object(Path, "is_junction", autospec=True,
                              side_effect=lambda path: path == self.source / relative):
                with self.assertRaisesRegex(ValueError, "linked install path"):
                    self.install()
        self.assertFalse(self.home.exists())

    def test_reserved_filenames_and_uppercase_extensions_fail(self):
        self.configure(["sre-api.md"])
        profile = self.source / "projects/sre-api.md"
        for name in ("index.md", "README.md", "profile.MD", "back`tick.md"):
            renamed = profile.rename(profile.with_name(name))
            with self.assertRaisesRegex(ValueError, "profile filename"):
                self.install()
            renamed.rename(profile)
        self.assertFalse(self.home.exists())

    def test_profile_rename_and_disable_clean_up_unchanged_owned_files(self):
        self.configure(["sre-api.md"])
        self.install()
        installed = self.home / ".copilot/engineering-workflow/projects"
        neighbor = installed / "unowned.md"
        neighbor.write_bytes(b"Unowned neighbor")
        profile = self.source / "projects/sre-api.md"
        for next_name in ("api.md", "API.md", None):
            old_name = profile.name
            if next_name:
                profile = profile.rename(profile.with_name(next_name))
            else:
                profile.write_text(profile.read_text(encoding="utf-8").replace(
                    "status: READY", "status: UNCONFIGURED"), encoding="utf-8")
            before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
            with patch.object(SETUP, "write_atomic", side_effect=AssertionError("check wrote")), \
                    patch.object(Path, "unlink", side_effect=AssertionError("check deleted")):
                self.assertEqual(self.install(check=True), 1)
            self.assertEqual(before, {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()})
            self.assertEqual(self.install(), 0)
            self.assertEqual(self.install(check=True), 0)
            self.assertEqual(neighbor.read_bytes(), b"Unowned neighbor")
            entries = json.loads((installed.parent / "install-manifest.json").read_text(encoding="utf-8"))
            self.assertNotIn(".copilot/engineering-workflow/projects/" + old_name, entries)
            expected = {"index.md", "unowned.md"}
            index = (installed / "index.md").read_text(encoding="utf-8")
            self.assertNotIn(old_name, index)
            if next_name:
                expected.add(next_name)
                self.assertIn(".copilot/engineering-workflow/projects/" + next_name, entries)
                self.assertIn("| " + next_name + " | Project 0 |", index)
                self.assertEqual((installed / next_name).read_bytes(), profile.read_bytes())
            else:
                self.assertIn("Configuration status: UNCONFIGURED", index)
            self.assertEqual({p.name for p in installed.iterdir()}, expected)

    def test_absent_stale_target_only_needs_manifest_cleanup(self):
        self.configure(["sre-api.md"])
        self.install()
        relative = ".copilot/engineering-workflow/projects/sre-api.md"
        (self.source / "projects/sre-api.md").unlink()
        (self.home / relative).unlink()
        before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
        self.assertEqual(self.install(check=True), 1)
        self.assertEqual(before, {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()})
        self.assertEqual(self.install(), 0)
        manifest = self.home / ".copilot/engineering-workflow/install-manifest.json"
        self.assertNotIn(relative, json.loads(manifest.read_text(encoding="utf-8")))
        self.assertEqual(self.install(check=True), 0)

    def test_stale_and_ordinary_conflicts_block_all_mutation(self):
        self.configure(["a.md", "z.md"])
        self.install()
        for name in ("a.md", "z.md"):
            (self.source / "projects" / name).unlink()
        installed = self.home / ".copilot/engineering-workflow/projects"
        for target, message in ((installed / "z.md", "stale and no longer matches the last owned hash"),
                                (installed / "index.md", "locally edited")):
            original = target.read_bytes()
            target.write_bytes(b"Preserve this local edit")
            before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
            for check in (True, False):
                with self.subTest(target=target.name, check=check):
                    with self.assertRaisesRegex(ValueError, message) as error:
                        self.install(check=check)
                    self.assertIn("Back up and remove conflicting installed files", str(error.exception))
                    self.assertEqual(before, {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()})
            target.write_bytes(original)
        self.assertEqual(self.install(), 0)
        self.assertEqual({p.name for p in installed.iterdir()}, {"index.md"})
        self.assertEqual(self.install(check=True), 0)

    def test_stale_paths_reject_directories_and_links_before_mutation(self):
        self.configure(["a.md", "z.md"])
        self.install()
        for name in ("a.md", "z.md"):
            (self.source / "projects" / name).unlink()
        target = self.home / ".copilot/engineering-workflow/projects/z.md"
        target.unlink()
        target.mkdir()
        for check in (False, True):
            with self.assertRaisesRegex(ValueError, "is not a file"):
                self.install(check=check)
            self.assertTrue(target.is_dir())
            self.assertTrue(target.with_name("a.md").is_file())
        with patch.object(Path, "is_junction", autospec=True, side_effect=lambda path: path == target):
            for check in (False, True):
                with self.assertRaisesRegex(ValueError, "linked install path"):
                    self.install(check=check)
                self.assertTrue(target.with_name("a.md").is_file())

    def test_interrupted_stale_cleanup_keeps_ownership_for_retry(self):
        self.configure(["sre-api.md"])
        self.install()
        target = self.home / ".copilot/engineering-workflow/projects/sre-api.md"
        manifest = target.parent.parent / "install-manifest.json"
        before = manifest.read_bytes()
        (self.source / "projects/sre-api.md").unlink()
        real_write = SETUP.write_atomic

        def interrupt(path, data):
            if path == manifest:
                raise OSError("interrupted manifest update")
            real_write(path, data)

        with patch.object(SETUP, "write_atomic", side_effect=interrupt):
            with self.assertRaisesRegex(OSError, "interrupted manifest update"):
                self.install()
        self.assertFalse(target.exists())
        self.assertEqual(manifest.read_bytes(), before)
        self.assertEqual(self.install(check=True), 1)
        self.assertEqual(self.install(), 0)
        self.assertEqual(self.install(check=True), 0)

    def test_invalid_profile_cli_error_is_actionable_and_read_only(self):
        self.configure(["sre-api.md"])
        profile = self.source / "projects/sre-api.md"
        profile.write_text(profile.read_text(encoding="utf-8").replace("- Jira prefix: ABC0", ""), encoding="utf-8")
        env = os.environ.copy()
        env.pop("COPILOT_HOME", None)
        for option in ([], ["--check"]):
            result = subprocess.run([sys.executable, str(self.source / "setup.py"),
                                     "--home", str(self.home), *option], cwd=self.root,
                                    env=env, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn(b"sre-api.md", result.stderr)
            self.assertIn(b"Routing requires", result.stderr)
            self.assertFalse(self.home.exists())

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
            ".copilot/other-workflow/unrelated.md": b"Unowned neighbor",
            ".copilot/agents/personal.agent.md": b"Personal agent",
            ".copilot/engineering-workflow/reviews/git.test/team/repo/pr-1/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/20260912T120000000000Z.md": b"User report",
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
        ignored = ["projects/foo.md", "projects/sre-api.md", "projects/my-project.md", "projects/draft.MD"]
        for relative in ignored:
            (clone / relative).write_bytes(b"Private local fixture")
        paths = ignored + ["projects/project.example.md", "projects/docs/guide.md"]
        result = git(clone, "check-ignore", "--no-index", *paths).decode().splitlines()
        self.assertEqual(result, ignored)
        tracked = git(clone, "ls-files", "projects").decode().splitlines()
        self.assertEqual(tracked, ["projects/project.example.md"])
        self.assertEqual(git(clone, "status", "--porcelain"), b"")
        (upstream / "projects/project.example.md").write_bytes(b"Updated generic template\n")
        git(upstream, "add", ".")
        git(upstream, "commit", "-m", "Template update fixture")
        git(clone, "pull", "--ff-only")
        for relative in ignored:
            self.assertEqual((clone / relative).read_bytes(), b"Private local fixture")
        self.assertEqual((clone / "projects/project.example.md").read_bytes(), b"Updated generic template\n")
        self.assertEqual(git(clone, "status", "--porcelain"), b"")


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

    def test_removed_skills_and_writing_follow_manifest_ownership(self):
        self.install()
        paths = {"skills/jira-story/SKILL.md": ".copilot/skills/jira-story/SKILL.md",
                 "writing/examples/pr.md": ".copilot/engineering-workflow/writing/examples/pr.md"}
        for source, installed in paths.items():
            (self.source / source).unlink()
        # Even a formerly generated path is unowned once omitted from the manifest.
        manifest = self.home / ".copilot/engineering-workflow/install-manifest.json"
        unowned = ".copilot/engineering-workflow/writing/examples/jira.md"
        original = (self.home / unowned).read_bytes()
        (self.source / "writing/examples/jira.md").unlink()
        entries = json.loads(manifest.read_text(encoding="utf-8"))
        del entries[unowned]
        manifest.write_text(json.dumps(entries), encoding="utf-8")
        self.assertEqual(self.install(check=True), 1)
        self.assertEqual(self.install(), 0)
        entries = json.loads(manifest.read_text(encoding="utf-8"))
        for relative in paths.values():
            self.assertFalse((self.home / relative).exists())
            self.assertNotIn(relative, entries)
        self.assertEqual((self.home / unowned).read_bytes(), original)
        self.assertEqual(self.install(check=True), 0)

    def test_paths_render_and_surface_adapters_reference_shared_baseline(self):
        self.install()
        root = self.home / ".copilot/engineering-workflow"
        skill = (self.home / ".copilot/skills/jira-story/SKILL.md").read_text(encoding="utf-8")
        self.assertIn(root.as_posix() + "/projects/index.md", skill)
        self.assertNotIn("{{WORKFLOW_ROOT}}", skill)
        baseline = self.home / ".copilot/copilot-instructions.md"
        adapter = (self.home / ".copilot/instructions/engineering-workflow.instructions.md").read_text(encoding="utf-8")
        self.assertTrue(adapter.startswith('---\napplyTo: "**"\n---\n'))
        self.assertIn(baseline.as_posix(), adapter)
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

    def test_uninstall_removes_only_unchanged_owned_files_and_allows_reinstall(self):
        self.configure(["my-project.md"])
        self.install()
        manifest = self.home / ".copilot/engineering-workflow/install-manifest.json"
        entries = json.loads(manifest.read_text(encoding="utf-8"))
        already_absent = self.home / ".copilot/skills/planning/SKILL.md"
        already_absent.unlink()
        unrelated = self.home / ".copilot/skills/unrelated/SKILL.md"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("Unrelated skill", encoding="utf-8")

        self.assertEqual(self.uninstall(), 0)
        self.assertFalse(manifest.exists())
        for relative in entries:
            self.assertFalse((self.home / relative).exists(), relative)
        self.assertEqual(unrelated.read_text(encoding="utf-8"), "Unrelated skill")

        self.assertEqual(self.install(), 0)
        self.assertEqual(self.install(check=True), 0)
        self.assertEqual(unrelated.read_text(encoding="utf-8"), "Unrelated skill")

    def test_uninstall_preflight_preserves_everything_when_managed_file_changed(self):
        self.install()
        target = self.home / ".copilot/engineering-workflow/writing/style.md"
        target.write_text("Locally edited guidance", encoding="utf-8")
        before = {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()}

        with self.assertRaisesRegex(ValueError, "No files removed"):
            self.uninstall()

        self.assertEqual(before, {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()})

    def test_uninstall_without_manifest_is_a_safe_noop(self):
        unrelated = self.home / ".copilot/settings.json"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("{}", encoding="utf-8")
        self.assertEqual(self.uninstall(), 0)
        self.assertEqual(unrelated.read_text(encoding="utf-8"), "{}")

    def test_uninstall_rejects_manifest_claim_on_unrelated_configuration(self):
        self.install()
        unrelated = self.home / ".copilot/settings.json"
        unrelated.write_text("{}", encoding="utf-8")
        manifest = self.home / SETUP.MANIFEST_RELATIVE
        entries = json.loads(manifest.read_text(encoding="utf-8"))
        entries[".copilot/settings.json"] = SETUP.digest(unrelated.read_bytes())
        manifest.write_text(json.dumps(entries), encoding="utf-8")
        before = {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()}

        with self.assertRaisesRegex(ValueError, "Invalid install manifest"):
            self.uninstall()

        self.assertEqual(before, {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()})

    def test_status_reports_not_installed_without_creating_files(self):
        result, output = self.status()
        self.assertEqual(result, 0)
        self.assertIn("Installation: not installed", output)
        self.assertIn("Manifest: not present", output)
        self.assertFalse(self.home.exists())

    def test_status_reports_current_without_changing_installed_files(self):
        self.install()
        before = {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()}
        result, output = self.status()
        self.assertEqual(result, 0)
        self.assertIn("Installation: current", output)
        self.assertIn("Engineering defaults: installed", output)
        self.assertEqual(before, {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()})

    def test_status_reports_safe_update_without_changing_installed_files(self):
        self.install()
        baseline = self.source / "instructions/baseline.md"
        baseline.write_text(
            baseline.read_text(encoding="utf-8") + "\nUpdated source guidance.\n",
            encoding="utf-8",
        )
        before = {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()}
        result, output = self.status()
        self.assertEqual(result, 0)
        self.assertIn("Installation: safe update available", output)
        self.assertIn("Engineering defaults: out of date", output)
        self.assertEqual(before, {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()})

    def test_status_reports_local_conflict_without_changing_installed_files(self):
        self.install()
        target = self.home / ".copilot/engineering-workflow/writing/style.md"
        target.write_text("Locally edited guidance", encoding="utf-8")
        before = {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()}
        result, output = self.status()
        self.assertEqual(result, 0)
        self.assertIn("Installation: conflict", output)
        self.assertIn("Writing: conflict", output)
        self.assertIn("locally edited content", output)
        self.assertEqual(before, {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()})

    def test_status_reports_ready_projects_dynamically(self):
        self.configure(["first.md", "second.md"])
        self.install()
        result, output = self.status()
        self.assertEqual(result, 0)
        self.assertIn("Projects: 2 READY in source", output)
        self.assertIn("Project 0", output)
        self.assertIn("Project 1", output)

    def test_status_discovers_skill_inventory_from_source(self):
        expected = len(list((self.source / "skills").glob("*/SKILL.md"))) + 1
        skill = self.source / "skills/status-fixture/SKILL.md"
        skill.parent.mkdir()
        skill.write_text(
            "---\nname: status-fixture\ndescription: Fixture used to verify dynamic status discovery.\n---\n\n# Fixture\n",
            encoding="utf-8",
        )
        result, output = self.status()
        self.assertEqual(result, 0)
        self.assertIn(f"Skills: {expected} discovered in source", output)
        self.assertFalse(self.home.exists())

    def test_agents_are_discovered_rendered_adopted_updated_and_reported(self):
        agents = self.source / "agents"
        fixture = agents / "fixture.agent.md"
        fixture.write_bytes(b"\xef\xbb\xbf---\r\nname: fixture\r\ndescription: Fixture.\r\n"
                            b'tools: ["read", "search"]\r\n---\r\n{{BASELINE_PATH}}\r\n{{WORKFLOW_ROOT}}\r\n')
        (agents / "notes.md").write_bytes(b"Not a profile")
        (agents / "ignored.agent.MD").write_bytes(b"Wrong extension")
        (agents / "nested").mkdir()
        (agents / "nested/ignored.agent.md").write_bytes(b"Not direct")
        definitions = sorted(agents.glob("*.agent.md", case_sensitive=True))
        relatives = {".copilot/agents/" + p.name for p in definitions}
        self.assertEqual(self.status()[0], 0)
        self.assertIn(f"Agents: {len(definitions)} discovered in source; missing", self.status()[1])
        self.assertFalse(self.home.exists())
        expected = (f"---\nname: fixture\ndescription: Fixture.\n"
                    f'tools: ["read", "search"]\n---\n'
                    f"{self.home.as_posix()}/.copilot/copilot-instructions.md\n"
                    f"{self.home.as_posix()}/.copilot/engineering-workflow\n").encode("utf-8")
        target = self.home / ".copilot/agents/fixture.agent.md"
        target.parent.mkdir(parents=True)
        target.write_bytes(expected)
        self.assertEqual(self.install(), 0)  # Adopt exact bytes without prior ownership.
        self.assertEqual(target.read_bytes(), expected)
        manifest = self.home / SETUP.MANIFEST_RELATIVE
        entries = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual({p for p in entries if p.startswith(".copilot/agents/")}, relatives)
        self.assertEqual(entries[".copilot/agents/fixture.agent.md"], SETUP.digest(expected))
        self.assertEqual(self.install(check=True), 0)
        self.assertIn(f"Agents: {len(definitions)} discovered in source; installed", self.status()[1])
        fixture.write_bytes(fixture.read_bytes() + b"Updated source\r\n")
        before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
        self.assertEqual(self.install(check=True), 1)
        self.assertIn(f"Agents: {len(definitions)} discovered in source; out of date", self.status()[1])
        self.assertEqual(before, {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()})
        self.assertEqual(self.install(), 0)
        self.assertEqual(target.read_bytes(), expected + b"Updated source\n")
        self.assertEqual(self.install(check=True), 0)

    def test_stale_agents_missing_targets_and_user_reports_survive_lifecycle(self):
        self.install()
        definitions = sorted((self.source / "agents").glob("*.agent.md"))
        self.assertTrue(definitions)
        relatives = [".copilot/agents/" + path.name for path in definitions]
        preserved = {
            ".copilot/agents/personal.agent.md": b"Personal agent",
            ".copilot/engineering-workflow/reviews/git.test/team/repo/pr-1/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/20260912T120000000000Z.md": b"User report",
        }
        for relative, data in preserved.items():
            target = self.home / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        originals = {p: p.read_bytes() for p in definitions}
        for path in definitions:
            path.unlink()
        (self.home / relatives[0]).unlink()  # An absent stale target still needs manifest cleanup.
        self.assertEqual(self.install(check=True), 1)
        self.assertIn("Agents: 0 discovered in source; not configured", self.status()[1])
        self.assertEqual(self.install(), 0)
        entries = json.loads((self.home / SETUP.MANIFEST_RELATIVE).read_text(encoding="utf-8"))
        for relative in relatives:
            self.assertNotIn(relative, entries)
            self.assertFalse((self.home / relative).exists())
        for relative in preserved:
            self.assertNotIn(relative, entries)
        self.assertEqual(self.install(check=True), 0)
        self.assertEqual(self.uninstall(), 0)
        for path, data in originals.items():
            path.write_bytes(data)
        self.assertEqual(self.install(), 0)
        self.assertEqual(self.install(check=True), 0)
        for relative, data in preserved.items():
            self.assertEqual((self.home / relative).read_bytes(), data)

    def test_active_and_stale_agent_conflicts_refuse_all_mutation(self):
        self.install()
        source = next((self.source / "agents").glob("*.agent.md"))
        relative = ".copilot/agents/" + source.name
        target = self.home / relative
        target.write_bytes(b"Preserve local agent changes")
        # Ensure a different desired update is also pending when preflight fails.
        style = self.source / "writing/style.md"
        style.write_bytes(style.read_bytes() + b"\nNew source guidance\n")
        for stale in (False, True):
            if stale:
                source.unlink()
            with self.subTest(stale=stale):
                before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
                for check in (False, True):
                    with self.assertRaisesRegex(ValueError, "No files changed"):
                        self.install(check=check)
                with self.assertRaisesRegex(ValueError, "No files removed"):
                    self.uninstall()
                result, output = self.status()
                self.assertEqual(result, 0)
                self.assertIn("Installation: conflict", output)
                self.assertIn(str(target), output)
                if not stale:
                    count = len(list((self.source / "agents").glob("*.agent.md")))
                    self.assertIn(f"Agents: {count} discovered in source; conflict", output)
                self.assertEqual(before, {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()})

    def test_new_agent_collision_blocks_fresh_install(self):
        source = next((self.source / "agents").glob("*.agent.md"))
        target = self.home / ".copilot/agents" / source.name
        target.parent.mkdir(parents=True)
        target.write_bytes(b"Unowned existing agent")
        before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
        for check in (False, True):
            with self.assertRaisesRegex(ValueError, "No files changed"):
                self.install(check=check)
        self.assertEqual(before, {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()})

    def test_manifest_rejects_nonprofile_agent_paths_and_runtime_reports(self):
        self.install()
        manifest = self.home / SETUP.MANIFEST_RELATIVE
        entries = json.loads(manifest.read_text(encoding="utf-8"))
        for relative in (".copilot/agents/settings.json", ".copilot/agents/nested/x.agent.md",
                         ".copilot/agents/../other.agent.md", ".copilot/agents/x.agent.MD",
                         ".copilot/engineering-workflow/reviews/report.md",
                         ".copilot/engineering-workflow/Reviews/report.md"):
            with self.subTest(relative=relative):
                manifest.write_text(json.dumps({**entries, relative: "0" * 64}), encoding="utf-8")
                before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
                for operation in (self.install, self.uninstall, self.status):
                    with self.assertRaises(ValueError):
                        operation()
                self.assertEqual(before, {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()})

    def test_agent_source_collisions_and_links_are_rejected(self):
        agents = self.source / "agents"
        original_glob = Path.glob
        for first, second in (("review", "REVIEW"), ("caf\u00e9", "cafe\u0301")):
            def paths(directory, pattern, **kwargs):
                if directory == agents:
                    return [agents / (first + ".agent.md"), agents / (second + ".agent.md")]
                return original_glob(directory, pattern, **kwargs)
            with patch.object(Path, "glob", autospec=True, side_effect=paths), \
                    patch.object(SETUP, "render", return_value=b"content"):
                with self.assertRaisesRegex(ValueError, "collide across platforms"):
                    self.install()
        for linked in (agents, next(agents.glob("*.agent.md")), self.home / ".copilot/agents"):
            with patch.object(Path, "is_junction", autospec=True,
                              side_effect=lambda path: path == linked):
                with self.assertRaisesRegex(ValueError, "linked install path"):
                    self.install()
        self.assertFalse(self.home.exists())

    def test_namespaced_agent_update_removes_only_unchanged_old_managed_names(self):
        agents = self.source / "agents"
        current = {path.name: path.read_bytes() for path in agents.glob("pr-review-*.agent.md")}
        self.assertTrue(current)
        old_names = []
        for name, data in current.items():
            old = name.removeprefix("pr-")
            old_names.append(old)
            (agents / name).unlink()
            (agents / old).write_bytes(data.replace(name.removesuffix(".agent.md").encode(),
                                                   old.removesuffix(".agent.md").encode()))
        self.install()
        unrelated = self.home / ".copilot/agents/user-notes.agent.md"
        unrelated.write_bytes(b"Personal agent")
        for name in old_names:
            (agents / name).unlink()
        for name, data in current.items():
            (agents / name).write_bytes(data)
        conflict = self.home / ".copilot/agents" / old_names[0]
        original = conflict.read_bytes()
        conflict.write_bytes(b"Preserve locally modified old agent")
        before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
        for check in (False, True):
            with self.assertRaisesRegex(ValueError, "stale and no longer matches"):
                self.install(check=check)
        self.assertEqual(before, {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()})
        conflict.write_bytes(original)
        self.assertEqual(self.install(check=True), 1)
        self.assertEqual(self.install(), 0)
        entries = json.loads((self.home / SETUP.MANIFEST_RELATIVE).read_text(encoding="utf-8"))
        for name in old_names:
            self.assertFalse((self.home / ".copilot/agents" / name).exists())
            self.assertNotIn(".copilot/agents/" + name, entries)
        for name, data in current.items():
            self.assertEqual((self.home / ".copilot/agents" / name).read_bytes(), data)
            self.assertIn(".copilot/agents/" + name, entries)
        self.assertEqual(unrelated.read_bytes(), b"Personal agent")
        self.assertEqual(self.install(check=True), 0)

    def test_runtime_script_is_rendered_owned_and_protected(self):
        script = self.source / "skills/pr-review/scripts/persist_report.py"
        original = script.read_text(encoding="utf-8")
        script.write_bytes(b"\xef\xbb\xbf" + original.replace("\n", "\r\n").encode("utf-8"))
        self.install()
        relative = ".copilot/skills/pr-review/scripts/persist_report.py"
        target = self.home / relative
        self.assertEqual(target.read_bytes(), original.encode("utf-8"))
        entries = json.loads((self.home / SETUP.MANIFEST_RELATIVE).read_text(encoding="utf-8"))
        self.assertIn(relative, entries)
        target.write_bytes(target.read_bytes() + b"# Local edit\n")
        with self.assertRaisesRegex(ValueError, "locally edited"):
            self.install()
        with self.assertRaisesRegex(ValueError, "locally modified"):
            self.uninstall()

    def test_status_manifest_error_uses_exit_two_without_mutation(self):
        self.install()
        manifest = self.home / SETUP.MANIFEST_RELATIVE
        manifest.write_text("{invalid", encoding="utf-8")
        before = {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()}
        env = os.environ.copy()
        env.pop("COPILOT_HOME", None)
        result = subprocess.run(
            [sys.executable, str(self.source / "setup.py"), "--home", str(self.home), "--status"],
            cwd=self.root,
            env=env,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"Unable to inspect engineering workflow status", result.stderr)
        self.assertIn(b"install-manifest.json", result.stderr)
        self.assertEqual(before, {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()})

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
        source = self.source
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
        self.assertEqual(run("--check", "--status").returncode, 2)
        self.assertEqual(run("--status", "--uninstall").returncode, 2)
        uninstall = run("--uninstall")
        self.assertEqual(uninstall.returncode, 0)
        self.assertIn(b"clear them manually", uninstall.stdout)
        self.assertEqual(run("--check").returncode, 1)
        self.assertEqual(run().returncode, 0)
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
