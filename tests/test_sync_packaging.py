"""Generated packaging must detect drift without repairing or changing sources."""

import json
from pathlib import Path
import shutil
import tempfile
import unittest

from tools.build_skills import ROOT, validate_links
from tools.smoke_installation import fingerprint
from tools.sync_packaging import MARKETPLACE, SIDECAR, sync


def reported(errors: list[str], *needles: str) -> bool:
    return any(all(needle in error for needle in needles) for error in errors)


class SyncPackagingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for name in ('.ai-rulez',):
            shutil.copytree(ROOT / name, self.root / name)
        shutil.copyfile(ROOT / 'package.json', self.root / 'package.json')
        (self.root / 'README.md').write_text('# Test repository\n')
        self.canonical = fingerprint(self.root / '.ai-rulez')
        self.metadata = (self.root / 'package.json').read_bytes()
        sync(self.root)

    def test_generation_preserves_sources_and_installs_the_root(self):
        self.assertEqual(sync(self.root, check=True), [])
        self.assertEqual(fingerprint(self.root / '.ai-rulez'), self.canonical)
        validate_links(self.root, list((self.root / 'skills').rglob('*.md')))
        claude = json.loads((self.root / '.claude-plugin/marketplace.json').read_text())
        codex = json.loads((self.root / '.agents/plugins/marketplace.json').read_text())
        self.assertEqual((claude['name'], claude['plugins'][0]['source']), (MARKETPLACE, './'))
        self.assertEqual((codex['name'], codex['plugins'][0]['source']['path']), (MARKETPLACE, './'))
        self.assertEqual((self.root / 'package.json').read_bytes(), self.metadata)
        self.assertTrue((self.root / SIDECAR).is_file())
        self.assertFalse((self.root / 'plugins').exists())
        self.assertFalse((self.root / '.pi').exists())
        for skill in (self.root / 'skills').iterdir():
            self.assertTrue((skill / 'agents/openai.yaml').is_file())
            self.assertTrue((skill / 'references/contract-rules.md').is_file())
            self.assertNotIn('GENERATED FILE', (skill / 'SKILL.md').read_text())

    def test_host_loaded_root_paths_are_reported_without_repair(self):
        (self.root / '.mcp.json').write_text('{}')
        (self.root / 'hooks').mkdir()
        before = fingerprint(self.root)
        errors = sync(self.root, check=True)
        self.assertTrue(reported(errors, 'AR9T0', '.mcp.json'))
        self.assertTrue(reported(errors, 'AR9T0', 'hooks'))
        self.assertEqual(fingerprint(self.root), before)

    def test_drift_check_reports_changed_missing_extra_without_repair(self):
        skills = self.root / 'skills'
        (skills / 'ghost-audit/SKILL.md').write_text('stale payload')
        (skills / 'ghost-audit/references/contract-rules.md').unlink()
        (skills / 'obsolete.txt').write_text('old release only')
        before = fingerprint(self.root)
        errors = sync(self.root, check=True)
        self.assertTrue(reported(errors, 'ai-rulez verify --plugin'))
        self.assertIn('extra: skills/obsolete.txt', errors)
        self.assertEqual(fingerprint(self.root), before)
        sync(self.root)
        self.assertFalse((skills / 'obsolete.txt').exists())
        self.assertEqual(sync(self.root, check=True), [])
        self.assertEqual(fingerprint(self.root / '.ai-rulez'), self.canonical)

    def test_metadata_change_invalidates_every_manifest_and_cached_copy(self):
        path = self.root / 'package.json'
        package = json.loads(path.read_text())
        package['version'] = '0.2.0'
        path.write_text(json.dumps(package))
        before = fingerprint(self.root)
        self.assertTrue(reported(sync(self.root, check=True), 'ai-rulez verify --plugin'))
        self.assertEqual(fingerprint(self.root), before)
        sync(self.root)
        for path in self.root.rglob('plugin.json'):
            self.assertEqual(json.loads(path.read_text())['version'], '0.2.0')
        self.assertEqual(sync(self.root, check=True), [])

    def test_symlinked_payload_is_rejected_and_external_target_preserved(self):
        file = self.root / 'skills/ghost-audit/SKILL.md'
        file.unlink()
        file.symlink_to(self.root / '.ai-rulez/skills/ghost-audit/SKILL.md')
        self.assertIn('symlink: skills/ghost-audit/SKILL.md', sync(self.root, check=True))
        with self.assertRaisesRegex(ValueError, 'symlinks'):
            sync(self.root)
        self.assertTrue(file.is_symlink())
        self.assertEqual(fingerprint(self.root / '.ai-rulez'), self.canonical)

    def test_deleted_source_skill_is_removed_from_generated_payload(self):
        shutil.rmtree(self.root / '.ai-rulez/skills/ghost-init')
        before = fingerprint(self.root)
        self.assertTrue(reported(sync(self.root, check=True), 'ai-rulez verify --plugin'))
        self.assertEqual(fingerprint(self.root), before)
        sync(self.root)
        self.assertFalse((self.root / 'skills/ghost-init').exists())
        self.assertNotIn('./skills/ghost-init', json.loads((self.root / 'package.json').read_text())['pi']['skills'])
        self.assertEqual(sync(self.root, check=True), [])

    def test_interface_change_invalidates_codex_manifests(self):
        path = self.root / '.ai-rulez/config.toml'
        path.write_text(path.read_text().replace('display_name = "Ghost Library Skills"', 'display_name = "Changed display name"'))
        self.assertTrue(reported(sync(self.root, check=True), 'ai-rulez verify --plugin'))
        sync(self.root)
        manifest = json.loads((self.root / '.codex-plugin/plugin.json').read_text())
        self.assertEqual(manifest['interface']['displayName'], 'Changed display name')

    def test_toml_metadata_updates_native_and_npm_outputs(self):
        path = self.root / '.ai-rulez/config.toml'
        path.write_text(path.read_text().replace('Hasan Sezer Tasan', 'Changed author'))
        before = fingerprint(self.root)
        self.assertTrue(reported(sync(self.root, check=True), 'ai-rulez verify --plugin'))
        self.assertEqual(fingerprint(self.root), before)
        sync(self.root)
        package = json.loads((self.root / 'package.json').read_text())
        self.assertEqual(package['author']['name'], 'Changed author')
        self.assertEqual(package['version'], '0.1.0')
        self.assertIn('./skills/ghost-audit', package['pi']['skills'])
        self.assertEqual(package['devDependencies'], json.loads(self.metadata)['devDependencies'])
        manifest = json.loads((self.root / '.claude-plugin/plugin.json').read_text())
        self.assertEqual(manifest['author']['name'], 'Changed author')

    def test_literal_plugin_version_is_rejected(self):
        path = self.root / '.ai-rulez/config.toml'
        path.write_text(path.read_text().replace('[plugin]\n', '[plugin]\nversion = "9.9.9"\n'))
        with self.assertRaisesRegex(ValueError, 'package.json owns the plugin version'):
            sync(self.root, check=True)


if __name__ == '__main__':
    unittest.main()
