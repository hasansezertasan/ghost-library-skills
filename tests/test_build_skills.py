"""Check resource portability and refusal of unsafe/incomplete packaging."""

from pathlib import Path
import tempfile
import unittest

from tools.build_skills import ROOT, build, validate_links, validate_tree


class BuildSkillsTests(unittest.TestCase):
    def test_each_built_skill_is_independently_movable(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "bundle"
            count = build(ROOT, output)
            self.assertEqual(count, 7)
            for skill in output.iterdir():
                moved = Path(temporary) / f"moved-{skill.name}"
                skill.rename(moved)
                validate_links(moved, list(moved.rglob("*.md")))
                self.assertTrue((moved / "references/contract-rules.md").is_file())
                self.assertTrue((moved / "templates/reports/conformance.md").is_file())

    def test_nonempty_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            sentinel = output / "consumer-file.txt"
            sentinel.write_text("keep", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "absent or empty"):
                build(ROOT, output)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
            self.assertEqual(list(output.iterdir()), [sentinel])

    def test_empty_output_is_supported(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "empty"
            output.mkdir()
            self.assertEqual(build(ROOT, output), 7)

    def test_source_directory_is_not_an_output(self):
        with self.assertRaisesRegex(ValueError, "Use dist/"):
            build(ROOT, ROOT / "skills")

    def test_broken_and_escaping_links_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            file = root / "SKILL.md"
            for target, message in (("missing.md", "Missing resource"), ("../escape.md", "escapes bundle")):
                with self.subTest(target=target):
                    file.write_text(f"[resource]({target})\n", encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, message):
                        validate_links(root, [file])

    def test_source_links_are_complete(self):
        self.assertEqual(len(validate_tree(ROOT)), 7)


if __name__ == "__main__":
    unittest.main()
