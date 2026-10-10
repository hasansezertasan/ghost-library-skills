"""Native adapters must retain the same skills and remain self-contained."""

import json
from pathlib import Path
import tempfile
import unittest

from tools.build_plugins import HOSTS, SKILL_PATHS, build_plugins
from tools.build_skills import ROOT, validate_links


class BuildPluginsTests(unittest.TestCase):
    def test_catalog_sources_and_plugin_resources_resolve(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "plugins"
            self.assertEqual(build_plugins(ROOT, output), dict.fromkeys(SKILL_PATHS, 7))
            for host, directory in HOSTS.items():
                plugin = output / host
                manifest = json.loads((plugin / directory / "plugin.json").read_text())
                self.assertEqual(manifest["name"], "ghost-library-skills")
                self.assertEqual(manifest["version"], "0.1.0")
                validate_links(plugin, list(plugin.rglob("*.md")))
                self.assertEqual(len(list((plugin / "skills").glob("*/SKILL.md"))), 7)
            claude = output / "claude/skills"
            for source in claude.rglob("*"):
                if source.is_file():
                    for host, path in SKILL_PATHS.items():
                        self.assertEqual(source.read_bytes(), (output / host / path / source.relative_to(claude)).read_bytes())
            for host in ("opencode", "pi"):
                validate_links(output / host, list((output / host).rglob("*.md")))
            pi = json.loads((output / "pi/package.json").read_text())
            self.assertEqual(pi["version"], "0.1.0")
            self.assertIn("pi-package", pi["keywords"])
            self.assertEqual(pi["pi"]["skills"], ["./skills"])
            self.assertEqual(pi["pi"]["extensions"], [])
            claude_catalog = json.loads((output / "claude/.claude-plugin/marketplace.json").read_text())
            codex_catalog = json.loads((output / "codex/.agents/plugins/marketplace.json").read_text())
            self.assertEqual(claude_catalog["plugins"][0]["source"], "./")
            self.assertEqual(codex_catalog["plugins"][0]["source"]["path"], "./")

    def test_nonempty_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            sentinel = output / "keep.txt"
            sentinel.write_text("consumer content")
            with self.assertRaisesRegex(ValueError, "absent or empty"):
                build_plugins(ROOT, output)
            self.assertEqual(sentinel.read_text(), "consumer content")
            self.assertEqual(list(output.iterdir()), [sentinel])

    def test_source_directory_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Use dist/"):
            build_plugins(ROOT, ROOT / "skills")


if __name__ == "__main__":
    unittest.main()
