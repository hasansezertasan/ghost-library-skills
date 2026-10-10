#!/usr/bin/env python3
"""Permit release creation only for the sole pending release at the checked SHA."""

import argparse
import json
from pathlib import Path
import sys


def is_release_merge(pages: list[list[dict]], sha: str) -> bool:
    pending = [
        pr for page in pages for pr in page
        if pr.get('merged_at') and pr.get('base', {}).get('ref') == 'main'
        and any(label.get('name') == 'autorelease: pending' for label in pr.get('labels', []))
    ]
    return len(pending) == 1 and pending[0].get('merge_commit_sha') == sha


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pulls', type=Path, required=True, help='gh api --paginate --slurp JSON')
    parser.add_argument('--sha', required=True)
    args = parser.parse_args()
    pages = json.loads(args.pulls.read_text(encoding='utf-8'))
    allowed = is_release_merge(pages, args.sha)
    print(f'is-release-merge={str(allowed).lower()}')
    if not allowed:
        print('Release creation skipped: no unique pending release matches the validated commit.', file=sys.stderr)


if __name__ == '__main__':
    main()
