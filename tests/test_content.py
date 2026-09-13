"""Check shipped Markdown references and the installed skill contract."""

import json
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
        for folder in ("docs", "instructions", "skills", "writing", "agents", "tests"):
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
                self.assertNotIn(b"{{", data, destination)

    def test_agent_metadata_tools_and_rendered_references(self):
        agents = sorted((SOURCE / "agents").glob("*.agent.md", case_sensitive=True))
        self.assertTrue(agents)
        self.assertEqual(set(agents), set((SOURCE / "agents").rglob("*.md")))
        with tempfile.TemporaryDirectory(prefix="workflow-agents-content-") as temporary:
            home = Path(temporary).resolve()
            files = SETUP.build_files(SOURCE, home, report=False)
            for agent in agents:
                with self.subTest(agent=agent.name):
                    header = re.fullmatch(r"---\n(.*?)\n---\n(.+)",
                                          agent.read_text(encoding="utf-8-sig"), re.DOTALL)
                    self.assertIsNotNone(header)
                    fields = dict(line.split(": ", 1) for line in header[1].splitlines())
                    self.assertEqual(len(fields), len(header[1].splitlines()))
                    self.assertEqual(set(fields), {"name", "description", "tools"})
                    self.assertRegex(agent.name, r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*\.agent\.md$")
                    self.assertEqual(fields["name"] + ".agent.md", agent.name)
                    self.assertTrue(fields["description"].strip())
                    self.assertLessEqual(len(fields["description"]), 1024)
                    allowed = json.loads(fields["tools"])
                    self.assertTrue(allowed)
                    self.assertEqual(len(allowed), len(set(allowed)))
                    self.assertLessEqual(set(allowed), {"read", "search"})
                    rendered = files[".copilot/agents/" + agent.name].decode("utf-8")
                    self.assertNotIn("{{", rendered)
                    for state in ("VERIFIED", "CONDITIONAL", "REJECTED"):
                        self.assertIn(state, header[2])
                    self.assertIn("counter-evidence", header[2])
                    self.assertIn("no source or external mutation", header[2])

    def test_pr_review_retains_parent_owned_gate_and_optional_delegation(self):
        skill = (SOURCE / "skills/pr-review/SKILL.md").read_text(encoding="utf-8")
        for state in ("PASS", "FAIL", "UNRESOLVED", "VERIFIED", "CONDITIONAL", "REJECTED"):
            self.assertRegex(skill, r"\b" + state + r"\b")
        self.assertIn("zero custom subagents", skill)
        self.assertIn("parent owns the impact map", skill)
        self.assertIn("revise it before final output", skill)
        self.assertIn("Do not include the parent's behavior-gate result", skill)
        self.assertIn("missing high-value regression scenarios", skill)
        self.assertIn("explicit approval", skill)
        self.assertIn("outside the resolved reviewed Git worktree", skill)
        self.assertIn("Create a new leaf exclusively", skill)
        self.assertIn("never overwrite different bytes", skill)

    def test_mcp_example_is_valid_source_only_reference(self):
        example = SOURCE / "mcp/mcp.example.json"
        configuration = json.loads(example.read_text(encoding="utf-8"))
        self.assertEqual(set(configuration), {"mcpServers"})
        servers = configuration["mcpServers"]
        self.assertEqual({server["type"] for server in servers.values()}, {"stdio", "http"})
        self.assertTrue(all(server.get("tools") for server in servers.values()))

        with tempfile.TemporaryDirectory(prefix="workflow-mcp-test-") as temporary:
            source = Path(temporary) / "source"
            home = Path(temporary) / "home"
            copy_source(source)
            files = SETUP.build_files(source, home)
            self.assertFalse(any("mcp.example.json" in relative for relative in files))


if __name__ == "__main__":
    unittest.main()
