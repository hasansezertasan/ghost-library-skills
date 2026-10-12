#!/usr/bin/env python3
"""Generate native packaging with ai-rulez, or report drift without edits."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import tomllib

try:
    from .build_skills import ROOT, SOURCE
except ImportError:
    from build_skills import ROOT, SOURCE


MARKETPLACE = 'ghost-library-skills-marketplace'
MANIFEST_PATHS = (
    Path('.claude-plugin/plugin.json'), Path('.claude-plugin/marketplace.json'),
    Path('.codex-plugin/plugin.json'), Path('.agents/plugins/marketplace.json'),
)
SIDECAR = Path('.ai-rulez-generated.json')
# ai-rulez records what it wrote but neither verify nor generate looks at files it
# did not record, so the wrapper owns this tree and rejects anything unrecorded.
OWNED_TREE = Path('skills')
# Log lines that do not describe a finding: skills/<name>/agents/ is bundled through
# content_root although the content-tree loader warns about it.
NOISE = ('Unrecognized skill subdirectory', 'pre-OKF layout', 'INFO ')
EXPECTED_PLUGIN = {
    'version_from': 'package.json',
    'runtimes': ['claude', 'codex', 'pi'],
    'content_root': '.ai-rulez',
    'shared_resources': ['references', 'templates'],
    'provenance_headers': False,
}


def load_object(path: Path) -> dict:
    if path.is_symlink():
        raise ValueError(f'Symlinked packaging source: {path}')
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError(f'Expected JSON object: {path}')
    return value


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def configuration(root: Path) -> dict:
    path = root / SOURCE / 'config.toml'
    if path.is_symlink() or path.parent.is_symlink():
        raise ValueError(f'Symlinked packaging source: {path}')
    value = tomllib.loads(path.read_text(encoding='utf-8'))
    plugin = value.get('plugin', {})
    if value.get('version') != '5.0' or plugin.get('name') != 'ghost-library-skills':
        raise ValueError('Expected a V5 ghost-library-skills plugin configuration')
    if 'version' in plugin:
        raise ValueError('package.json owns the plugin version; remove [plugin].version')
    for key, expected in EXPECTED_PLUGIN.items():
        if plugin.get(key) != expected:
            raise ValueError(f'Expected [plugin].{key} = {json.dumps(expected)}')
    if plugin.get('pi') != {'skills_dir': 'skills', 'package_json': 'merge'}:
        raise ValueError('Pi must reuse root skills/ and merge into the authored package.json')
    marketplace = value.get('marketplace', {})
    if marketplace.get('name') != MARKETPLACE or marketplace.get('members'):
        raise ValueError(f'Expected a single-plugin {MARKETPLACE} catalog')
    if plugin.get('codex', {}).get('marketplace') is not True:
        raise ValueError('Expected the single-plugin Codex catalog to be enabled')
    return value


def manifests(root: Path) -> dict[Path, dict]:
    """Read native output; host schemas are rendered by ai-rulez."""
    return {path: load_object(root / path) for path in MANIFEST_PATHS}


def ai_rulez(root: Path, *arguments: str) -> subprocess.CompletedProcess:
    package = load_object(ROOT / 'package.json')
    installed = ROOT / 'node_modules/ai-rulez/package.json'
    if not installed.is_file():
        raise ValueError('Missing ai-rulez; run npm ci --include=dev --ignore-scripts')
    if load_object(installed)['version'] != package['devDependencies']['ai-rulez']:
        raise ValueError('Installed ai-rulez differs from package.json; run npm ci --include=dev --ignore-scripts')
    return subprocess.run([str(ROOT / 'node_modules/.bin/ai-rulez'), *arguments], cwd=root,
                          capture_output=True, text=True, timeout=120)


def findings(result: subprocess.CompletedProcess) -> str:
    lines = [line.strip() for line in (result.stdout + result.stderr).splitlines()]
    return '; '.join(line for line in lines if line and not any(n in line for n in NOISE))


def unrecorded(root: Path) -> list[str]:
    """Name owned paths ai-rulez did not record, which its own checks accept."""
    tree = root / OWNED_TREE
    if tree.is_symlink():
        return [f'symlink: {OWNED_TREE}']
    if not tree.is_dir():
        return [f'missing: {OWNED_TREE}']
    sidecar = root / SIDECAR
    recorded = set(load_object(sidecar).get('outputs', {})) if sidecar.is_file() else set()
    problems = []
    for path in sorted(tree.rglob('*')):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            problems.append(f'symlink: {name}')
        elif path.is_file() and name not in recorded:
            problems.append(f'extra: {name}')
    return problems


def sync(root: Path, check: bool = False) -> list[str]:
    configuration(root)
    if check:
        problems = unrecorded(root)
        for arguments in (('verify', '--plugin'), ('validate', '--strict')):
            result = ai_rulez(root, *arguments)
            if result.returncode:
                problems.append(f'ai-rulez {" ".join(arguments)}: {findings(result)}')
        return problems
    problems = [p for p in unrecorded(root) if p.startswith('symlink:')]
    if problems:
        raise ValueError('Refusing to write through symlinks: ' + '; '.join(problems))
    result = ai_rulez(root, 'generate', '--plugin')
    if result.returncode:
        raise ValueError(f'ai-rulez generate --plugin failed: {findings(result)}')
    # Explicit synchronization replaces the owned tree, so stray files go too.
    for problem in unrecorded(root):
        (root / problem.removeprefix('extra: ')).unlink()
    for directory in sorted((root / OWNED_TREE).rglob('*'), reverse=True):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()
    return []


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Report stale manifests/payload without repairing')
    args = parser.parse_args()
    try:
        problems = sync(ROOT, args.check)
        if problems:
            parser.exit(1, '\n'.join(problems) + '\nRun make sync to regenerate packaging.\n')
        print('Native packaging is current.' if args.check else 'Generated portable skills and native packaging.')
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
