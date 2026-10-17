#!/usr/bin/env python3
"""Reject symlinks and unrecorded files in the generated tree, which ai-rulez accepts.

ai-rulez records what it wrote in `.ai-rulez-generated.json`, but neither
`verify` nor `generate --check` looks at files it did not record, and it follows
symlinks inside the checkout. This repo owns `skills/`, so it checks both.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATHS = (
    Path('.claude-plugin/plugin.json'), Path('.claude-plugin/marketplace.json'),
    Path('.codex-plugin/plugin.json'), Path('.agents/plugins/marketplace.json'),
)
SIDECAR = Path('.ai-rulez-generated.json')
ANTIGRAVITY_ADAPTER = Path('plugin.json')
OWNED_TREE = Path('skills')


def symlinked(root: Path) -> list[str]:
    """Name generated targets reached through a symlink."""
    problems = set()
    for target in (*MANIFEST_PATHS, SIDECAR, ANTIGRAVITY_ADAPTER, Path('package.json'), OWNED_TREE):
        for parent in (target, *target.parents[:-1]):
            if (root / parent).is_symlink():
                problems.add(f'symlink: {parent.as_posix()}')
    return sorted(problems)


def unrecorded(root: Path) -> list[str]:
    """Name owned paths ai-rulez did not record."""
    tree = root / OWNED_TREE
    if tree.is_symlink():
        return []
    if not tree.is_dir():
        return [f'missing: {OWNED_TREE}']
    sidecar = root / SIDECAR
    recorded = set(json.loads(sidecar.read_text(encoding='utf-8')).get('outputs', {})) if sidecar.is_file() else set()
    problems = []
    for path in sorted(tree.rglob('*')):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            problems.append(f'symlink: {name}')
        elif path.is_file() and name not in recorded:
            problems.append(f'extra: {name}')
    return problems


def problems_in(root: Path) -> list[str]:
    return symlinked(root) + unrecorded(root)


if __name__ == '__main__':
    found = problems_in(ROOT)
    if found:
        sys.exit('\n'.join(found) + '\nRun npm run generate, then remove what remains by hand.')
    print('Generated tree has no symlinks or unrecorded files.')
