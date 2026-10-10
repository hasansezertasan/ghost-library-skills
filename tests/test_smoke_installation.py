"""Protect consumer output and detect stale or missing packaged resources."""

from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from tools.smoke_installation import exercise, fingerprint, real_configuration


class InstallationChecksTests(unittest.TestCase):
    def test_repository_copy_cannot_recurse_into_source_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / 'consumer-output'
            with self.assertRaisesRegex(ValueError, 'Use dist/'):
                exercise(root, root / 'missing-archive', root / 'missing-loader', output, repository=True)
            self.assertFalse(output.exists())

    def test_guard_ignores_cache_timestamp_but_detects_preference_changes(self):
        with tempfile.TemporaryDirectory() as temporary, patch('tools.smoke_installation.Path.home', return_value=Path(temporary)):
            path = Path(temporary) / '.claude.json'
            path.write_text(json.dumps({'cachedGrowthBookFeaturesAt': 1, 'preferences': {'enabled': True}}))
            expected = real_configuration()
            path.write_text(json.dumps({'cachedGrowthBookFeaturesAt': 2, 'pluginUsage': {'count': 2}, 'preferences': {'enabled': True}}))
            self.assertEqual(real_configuration(), expected)
            path.write_text(json.dumps({'cachedGrowthBookFeaturesAt': 2, 'preferences': {'enabled': False}}))
            self.assertNotEqual(real_configuration(), expected)

    def test_existing_output_is_preserved_before_any_host_action(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            sentinel = output / 'report.json'
            sentinel.write_text('consumer evidence')
            with self.assertRaisesRegex(ValueError, 'must be absent'):
                exercise(output / 'missing-bundle', output / 'missing-archive', output / 'missing-loader', output)
            self.assertEqual(sentinel.read_text(), 'consumer evidence')
            self.assertEqual(list(output.iterdir()), [sentinel])

    def test_payload_check_detects_extra_missing_and_changed_resources(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / 'SKILL.md'
            skill.write_text('unchanged instructions')
            resource = root / 'rules.md'
            resource.write_text('current behavior')
            expected = fingerprint(root)
            resource.write_text('obsolete behavior')
            self.assertNotEqual(fingerprint(root), expected)
            resource.write_text('current behavior')
            self.assertEqual(fingerprint(root), expected)
            stale = root / 'old-only.txt'
            stale.write_text('removed upstream')
            self.assertNotEqual(fingerprint(root), expected)
            stale.unlink()
            resource.unlink()
            self.assertNotEqual(fingerprint(root), expected)


if __name__ == '__main__':
    unittest.main()
