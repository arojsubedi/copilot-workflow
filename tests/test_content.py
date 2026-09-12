"""Check shipped Markdown references and the installed skill contract."""

import re
import tempfile
import unittest
from pathlib import Path

from test_setup import SOURCE, SETUP, copy_source


def headings(text):
    anchors = set()
    fenced = False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and re.match(r"^#{1,6} ", line):
            title = line.lstrip("# ").lower()
            anchors.add(re.sub(r"[^\w -]", "", title).replace(" ", "-"))
    return anchors


class ContentTests(unittest.TestCase):
    def test_shipped_local_markdown_links_and_anchors_resolve(self):
        paths = [SOURCE / "README.md", SOURCE / "DESIGN.md", SOURCE / "projects/project.example.md"]
        for folder in ("docs", "instructions", "skills", "writing"):
            paths.extend((SOURCE / folder).rglob("*.md"))
        for path in paths:
            text = path.read_text(encoding="utf-8-sig")
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if "://" in link:
                    continue
                relative, _, anchor = link.partition("#")
                target = path.parent / relative if relative else path
                with self.subTest(source=path.relative_to(SOURCE), link=link):
                    self.assertTrue(target.is_file(), str(target))
                    if anchor:
                        self.assertIn(anchor, headings(target.read_text(encoding="utf-8-sig")))

    def test_discovered_skills_have_valid_metadata_and_installed_references(self):
        skill_directories = sorted(path for path in (SOURCE / "skills").iterdir() if path.is_dir())
        skills = sorted((SOURCE / "skills").glob("*/SKILL.md"))
        self.assertTrue(skills)
        self.assertEqual([path.parent for path in skills], skill_directories)
        # Build rendered content without writing into a real Copilot home.
        with tempfile.TemporaryDirectory(prefix="workflow-content-test-") as temporary:
            source = Path(temporary) / "source"
            home = Path(temporary) / "home"
            copy_source(source)
            files = SETUP.build_files(source, home)
            for skill in skills:
                source_text = skill.read_text(encoding="utf-8-sig")
                header = re.match(r"\A---\n(.*?)\n---\n(.+)\Z", source_text, re.DOTALL)
                self.assertIsNotNone(header, str(skill))
                fields = dict(line.split(": ", 1) for line in header[1].splitlines())
                self.assertEqual(len(fields), len(header[1].splitlines()))
                self.assertEqual(set(fields), {"name", "description"})
                self.assertEqual(fields["name"], skill.parent.name)
                self.assertRegex(fields["name"], r"^[a-z]+(?:-[a-z]+)*$")
                description = fields["description"].strip('"').strip()
                self.assertTrue(description)
                self.assertLessEqual(len(description), 1024)
                destination = ".copilot/skills/" + skill.parent.name + "/SKILL.md"
                rendered = files[destination].decode("utf-8")
                self.assertNotIn("{{", rendered)
                for link in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", rendered):
                    if "://" not in link:
                        target = (home / destination).parent.joinpath(link).resolve()
                        self.assertIn(target.relative_to(home.resolve()).as_posix(), files)
            for destination, data in files.items():
                self.assertNotIn(b"{{WORKFLOW_ROOT}}", data, destination)
                self.assertNotIn(b"{{BASELINE_PATH}}", data, destination)


if __name__ == "__main__":
    unittest.main()
