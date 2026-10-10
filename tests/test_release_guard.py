"""Protect against releasing an unvalidated historical merge."""

import unittest

from tools.release_guard import is_release_merge


def release(sha: str, **changes) -> dict:
    return {
        'merged_at': '2026-10-05T00:00:00Z', 'merge_commit_sha': sha,
        'base': {'ref': 'main'}, 'labels': [{'name': 'autorelease: pending'}],
        **changes,
    }


class ReleaseGuardTests(unittest.TestCase):
    def test_exact_release_merge_is_allowed(self):
        self.assertTrue(is_release_merge([[release('checked')]], 'checked'))

    def test_later_green_commit_does_not_release_failed_merge(self):
        self.assertFalse(is_release_merge([[release('failed')]], 'later-green'))

    def test_multiple_pending_merges_are_blocked_even_across_pages(self):
        self.assertFalse(is_release_merge([[release('failed')], [release('checked')]], 'checked'))

    def test_open_tagged_and_other_branch_prs_do_not_authorize_release(self):
        for changes in ({'merged_at': None}, {'labels': [{'name': 'autorelease: tagged'}]},
                        {'base': {'ref': 'maintenance'}}):
            with self.subTest(changes=changes):
                self.assertFalse(is_release_merge([[release('checked', **changes)]], 'checked'))
        self.assertFalse(is_release_merge([], 'checked'))
