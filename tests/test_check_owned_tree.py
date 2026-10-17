"""The generated tree must reject symlinks and files ai-rulez did not record."""

from pathlib import Path
import shutil
import tempfile
import unittest

from tools.check_owned_tree import ROOT, problems_in


class CheckOwnedTreeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for name in ('skills', '.claude-plugin', '.codex-plugin', '.agents'):
            shutil.copytree(ROOT / name, self.root / name)
        for name in ('.ai-rulez-generated.json', 'plugin.json', 'package.json'):
            shutil.copyfile(ROOT / name, self.root / name)

    def test_the_committed_tree_is_clean(self):
        self.assertEqual(problems_in(ROOT), [])
        self.assertEqual(problems_in(self.root), [])

    def test_unrecorded_file_is_reported(self):
        (self.root / 'skills/obsolete.txt').write_text('old release only')
        self.assertIn('extra: skills/obsolete.txt', problems_in(self.root))

    def test_symlinked_payload_is_reported(self):
        file = self.root / 'skills/ghost-audit/SKILL.md'
        target = self.root / 'elsewhere.md'
        shutil.copyfile(file, target)
        file.unlink()
        file.symlink_to(target)
        self.assertIn('symlink: skills/ghost-audit/SKILL.md', problems_in(self.root))

    def test_host_loaded_root_components_are_reported(self):
        (self.root / '.mcp.json').write_text('{}')
        (self.root / 'hooks').mkdir()
        problems = problems_in(self.root)
        self.assertIn('root component: .mcp.json', problems)
        self.assertIn('root component: hooks', problems)

    def test_symlinked_manifest_directory_is_reported(self):
        inside = self.root / 'elsewhere'
        shutil.move(self.root / '.claude-plugin', inside)
        (self.root / '.claude-plugin').symlink_to(inside)
        self.assertIn('symlink: .claude-plugin', problems_in(self.root))


if __name__ == '__main__':
    unittest.main()
