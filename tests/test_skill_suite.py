"""Cross-skill structure: every skill carries the contract revision 2 vocabulary
inline (Agent Skills references stay inside the skill root). Structural only;
says nothing about model behaviour."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted((ROOT / ".agents/skills").glob("*/SKILL.md"))
FINDING = json.loads((ROOT / "schemas/finding.schema.json").read_text(encoding="utf-8"))
DEFS = FINDING["$defs"]
SPECIALISTS = FINDING["properties"]["reviewer"]["enum"]


def text(path):
    return path.read_text(encoding="utf-8")


def shared_block(body):
    start = body.index("## Shared safety and output contract")
    return body[start:body.index("**Package status:**", start)]


class SkillSuiteTests(unittest.TestCase):
    def test_seven_skills_present(self):
        names = [p.parent.name for p in SKILLS]
        self.assertEqual(sorted(names), sorted(SPECIALISTS + ["review-coordinator"]))

    def test_shared_block_is_identical_everywhere(self):
        blocks = {p.parent.name: shared_block(text(p)) for p in SKILLS}
        reference = blocks["argument-review"]
        for name, block in blocks.items():
            with self.subTest(skill=name):
                self.assertEqual(block, reference)

    def test_shared_block_carries_schema_severity_definitions(self):
        block = shared_block(text(SKILLS[0]))
        for option in DEFS["severity"]["oneOf"]:
            with self.subTest(severity=option["const"]):
                self.assertIn(f"  - `{option['const']}`: {option['description']}\n", block)

    def test_shared_block_requires_failure_slot_and_no_change_for_abstentions(self):
        block = shared_block(text(SKILLS[0]))
        self.assertIn("**failure**", block.lower())
        self.assertIn("omitted for abstentions", block)
        self.assertIn("`embedded-instruction`", block)

    def test_specialist_categories_match_schema(self):
        for name in SPECIALISTS:
            body = text(ROOT / ".agents/skills" / name / "SKILL.md")
            with self.subTest(skill=name):
                section = re.search(r"^## Categories\n\nUse one of: (.+?)\. Any specialist", body, re.M)
                self.assertIsNotNone(section, "missing Categories section")
                listed = re.findall(r"`([a-z-]+)`", section.group(1))
                self.assertEqual(listed, DEFS["category-" + name]["enum"])

    def test_coordinator_has_no_category_list_of_its_own(self):
        body = text(ROOT / ".agents/skills/review-coordinator/SKILL.md")
        self.assertNotIn("## Categories", body)

    def test_argument_and_method_no_longer_share_a_worked_example(self):
        argument = text(ROOT / ".agents/skills/argument-review/SKILL.md")
        method = text(ROOT / ".agents/skills/method-review/SKILL.md")
        self.assertNotIn("geometric violations", argument)
        self.assertIn("Boundary with method", argument)
        self.assertIn("Boundary with argument", method)

    def test_terminology_matches_the_suite_structure(self):
        body = text(ROOT / ".agents/skills/terminology-review/SKILL.md")
        self.assertNotIn("## Before release", body)
        self.assertIn("**Package status:**", body)


if __name__ == "__main__":
    unittest.main()
