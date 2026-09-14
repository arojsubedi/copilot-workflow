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
                self.assertTrue(fields["name"].startswith("eng-"))
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
                    self.assertEqual(set(fields), {"name", "description", "tools", "infer"})
                    self.assertIs(json.loads(fields["infer"]), False)
                    self.assertTrue(fields["name"].startswith("pr-review-"))
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
        skill = (SOURCE / "skills/eng-pr-review/SKILL.md").read_text(encoding="utf-8")
        for state in ("PASS", "FAIL", "UNRESOLVED", "VERIFIED", "CONDITIONAL", "REJECTED"):
            self.assertRegex(skill, r"\b" + state + r"\b")
        self.assertIn("zero custom subagents", skill)
        self.assertIn("parent owns the impact map", skill)
        self.assertIn("revise it before final output", skill)
        self.assertIn("Do not include the parent's behavior-gate result", skill)
        self.assertIn("missing high-value regression scenarios", skill)
        self.assertIn("explicit approval", skill)
        self.assertIn("existing thread", skill)
        self.assertIn("recommended disposition", skill)
        self.assertIn("APPROVE", skill)
        self.assertIn("COMMENT", skill)
        self.assertIn("REQUEST CHANGES", skill)
        self.assertIn("Do not delete a valid technical finding", skill)
        # Conditional procedures own these rules; the entrypoint routes to them.
        for resource, contracts in {
            "review-state": ("A reply is not proof of a fix",),
            "publication": ("summary, inline comments and thread replies",),
            "reporting": ("pr-<number>/<head-sha>/<review-run-id>.md", "scripts/persist_report.py"),
        }.items():
            self.assertIn(f"references/{resource}.md", skill)
            procedure = (SOURCE / f"skills/eng-pr-review/references/{resource}.md").read_text(encoding="utf-8")
            for contract in contracts:
                self.assertIn(contract, procedure)

    def test_planning_preserves_research_convergence_and_authorization(self):
        skill = (SOURCE / "skills/eng-planning/SKILL.md").read_text(encoding="utf-8")
        stages = ("Research before decomposition", "Derive the provisional approach",
                  "Validate the proposal", "Close coverage and refresh evidence",
                  "Persist and converge in place", "Stop and hand off")
        positions = [skill.index("## " + stage) for stage in stages]
        self.assertEqual(positions, sorted(positions))
        for contract in (r"user-proposed.*candidate", r"callers.*contracts/invariants.*tests",
                         r"functional-first sequencing", r"current proposal, never the history",
                         r"Planning does not authorize implementation", r"same plan"):
            self.assertRegex(skill, contract)

    def test_planning_validation_routes_by_consequence_and_separates_roles(self):
        skill = (SOURCE / "skills/eng-planning/SKILL.md").read_text(encoding="utf-8")
        gate = skill.split("## Validate the proposal\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn("references/validation.md", gate)
        for contract in (r"first draft is a hypothesis", r"Tiny.*No subagent is required",
                         r"Meaningful.*Read \[validation\]", r"Consequential design commitment",
                         r"not diff size", r"provisional approach never mentioned",
                         r"parent owns the final proposal", r"Large mechanically determined"):
            self.assertRegex(gate, contract)
        procedure = (SOURCE / "skills/eng-planning/references/validation.md").read_text(encoding="utf-8")
        for contract in (r"`explore`.*factual questions", r"fresh `general-purpose` context",
                         r"Do not send the draft plan", r"no persisted accessible draft",
                         r"Do not forward the full parent conversation", r"Only after.*result returns",
                         r"worker saw the draft.*anchored critique", r"Disclose.*missing independent",
                         r"Rubber-duck.*not an authority or sole validator", r"never model voting",
                         r"numeric confidence", r"reject.*reuse.*violates another contract",
                         r"Mutation protection", r"Draft exclusion", r"Read-only prose alone is insufficient"):
            self.assertRegex(procedure, contract)

    def test_planning_artifact_closure_and_refresh_have_runtime_owners(self):
        skill = (SOURCE / "skills/eng-planning/SKILL.md").read_text(encoding="utf-8")
        for contract in (r"session's managed plan", r"explicit repository-local plan request",
                         r"artifact-only write/transfer", r"do not write.*native session plan",
                         r"Every requested behavior.*implementation owner/path.*verification",
                         r"omitted material requirement.*blocks readiness",
                         r"unchanged HEAD or status alone", r"repeat only the validation"):
            self.assertRegex(skill, contract)
        implementation = (SOURCE / "skills/eng-implementation/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("actual active surface", implementation)
        self.assertIn("eng-planning/SKILL.md", implementation)

    def test_review_routes_history_before_analysis_and_reconciles_opinions_late(self):
        skill = (SOURCE / "skills/eng-pr-review/SKILL.md").read_text(encoding="utf-8")
        stages = ("Pin the target", "Probe review state", "Understand and map material change",
                  "Falsify candidates", "Reconcile, recommend and present")
        positions = [skill.index("## " + stage) for stage in stages]
        self.assertEqual(positions, sorted(positions))
        probe = skill.split("## Probe review state\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn("references/review-state.md", probe)
        for contract in (r"even without viewer identity", r"Other reviewers' threads alone",
                         r"neutral metadata", r"before choosing the comparison"):
            self.assertRegex(probe, contract)
        state = (SOURCE / "skills/eng-pr-review/references/review-state.md").read_text(encoding="utf-8")
        for contract in (r"First review with other reviewers", r"Re-review with a new head",
                         r"Follow-up on the same head.*Do not invent a code delta",
                         r"History unknown", r"force-push", r"local prior analysis",
                         r"never a submitted GitHub review", r"A delta alone cannot establish"):
            self.assertRegex(state, contract)
        for contract in (r"known repository-standard check", r"without recursively auditing",
                         r"Inspect the consequential execution chain", r"Do not blindly execute",
                         r"recheck PR identity and base/head"):
            self.assertRegex(skill, contract)

    def test_explicit_personal_skill_invocations_use_discoverable_names(self):
        skills = {p.parent.name for p in (SOURCE / "skills").glob("*/SKILL.md")}
        setup_doc = (SOURCE / "docs/setup.md").read_text(encoding="utf-8")
        for name in skills:
            self.assertIn("/" + name, setup_doc)
        self.assertIn("/skills info eng-planning", setup_doc)
        self.assertIn("/skills info eng-pr-review", setup_doc)
        for folder in ("docs", "writing", "tests", "skills"):
            for path in (SOURCE / folder).rglob("*.md"):
                for name in re.findall(r"(?<![\w/-])/(eng-[a-z-]+)\b", path.read_text(encoding="utf-8")):
                    if name.endswith("-"):
                        continue  # Documented namespace placeholder, not invocation.
                    self.assertIn(name, skills, str(path))

    def test_planning_architecture_and_semantic_cases_are_discoverable(self):
        for name in ("README.md", "DESIGN.md"):
            self.assertIn("](docs/planning.md)", (SOURCE / name).read_text(encoding="utf-8"))
        architecture = (SOURCE / "docs/planning.md").read_text(encoding="utf-8")
        for target in ("../skills/eng-planning/SKILL.md", "../skills/eng-planning/references/validation.md",
                       "../tests/planning-quality-cases.md", "../writing/examples/plan.md"):
            self.assertIn("](" + target + ")", architecture)
        cases = (SOURCE / "tests/planning-quality-cases.md").read_text(encoding="utf-8")
        self.assertIn("manual evaluation guidance", cases)
        # Packaging and links are mechanical; scenario outcomes require evaluation.
        self.assertNotIn("planning", " ".join(p.name for p in (SOURCE / "agents").glob("*.agent.md")))

    def test_publication_examples_cover_review_artifacts_without_internal_ids(self):
        examples = (SOURCE / "writing/examples/review.md").read_text(encoding="utf-8")
        for kind in ("APPROVE summary", "COMMENT summary", "REQUEST CHANGES summary",
                     "re-review", "existing thread"):
            self.assertIn(kind, examples)
        self.assertNotRegex(examples, r"\b(?:B|I|AC|F)\d+\b|\u2014")

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
