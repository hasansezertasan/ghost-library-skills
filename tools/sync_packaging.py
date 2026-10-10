#!/usr/bin/env python3
"""Generate portable skills and native packaging, or report drift without edits."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import tomllib

try:
    from .build_skills import ROOT, SOURCE, build
except ImportError:
    from build_skills import ROOT, SOURCE, build


MARKETPLACE = 'ghost-library-skills-marketplace'
PACKAGE = Path('plugins/ghost-library-skills')
METADATA_KEYS = ('name', 'version', 'description', 'author', 'repository', 'keywords')
PI_RESOURCES = {'skills': ['./skills'], 'extensions': [], 'prompts': [], 'themes': []}


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


def metadata(root: Path) -> dict:
    package = load_object(root / 'package.json')
    if package.get('name') != 'ghost-library-skills' or not package.get('version'):
        raise ValueError('package.json must identify ghost-library-skills and its version')
    if package.get('pi') != PI_RESOURCES:
        raise ValueError('Pi package must expose only ./skills')
    plugin = configuration(root)['plugin']
    return {key: package['version'] if key == 'version' else plugin[key]
            for key in METADATA_KEYS}


def configuration(root: Path) -> dict:
    path = root / SOURCE / 'config.toml'
    if path.is_symlink() or path.parent.is_symlink():
        raise ValueError(f'Symlinked packaging source: {path}')
    value = tomllib.loads(path.read_text(encoding='utf-8'))
    plugin = value.get('plugin', {})
    if value.get('version') != '5.0' or plugin.get('name') != 'ghost-library-skills':
        raise ValueError('Expected a V5 ghost-library-skills plugin configuration')
    if not isinstance(plugin.get('version'), str):
        raise ValueError('Expected the generated plugin version mirror in TOML')
    if plugin.get('runtimes') != ['claude', 'codex']:
        raise ValueError('Only the validated Claude/Codex plugin runtimes are enabled')
    return value


MANIFEST_PATHS = (
    Path('.claude-plugin/plugin.json'), Path('.claude-plugin/marketplace.json'),
    Path('.codex-plugin/plugin.json'), Path('.agents/plugins/marketplace.json'),
)


def manifests(root: Path) -> dict[Path, dict]:
    """Read native output; host schemas are rendered by ai-rulez."""
    return {path: load_object(root / path) for path in MANIFEST_PATHS}


def write_toml(path: Path, value: dict) -> None:
    """Serialize derived configuration tables with JSON-compatible TOML values."""
    lines = []
    def table(name: str, values: dict) -> None:
        if name:
            lines.append(f'[{name}]')
        for key, item in values.items():
            if not isinstance(item, dict):
                lines.append(f'{key} = {json.dumps(item, ensure_ascii=False)}')
        lines.append('')
        for key, item in values.items():
            if isinstance(item, dict):
                table(f'{name}.{key}' if name else key, item)
    table('', value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(lines), encoding='utf-8')


def generate(root: Path, output: Path) -> None:
    """Render native JSON in a fresh staging tree and retain our resource builder."""
    shared = metadata(root)
    package = load_object(root / 'package.json')
    installed = ROOT / 'node_modules/ai-rulez/package.json'
    if not installed.is_file():
        raise ValueError('Missing ai-rulez; run npm ci --include=dev --ignore-scripts')
    if load_object(installed)['version'] != package['devDependencies']['ai-rulez']:
        raise ValueError('Installed ai-rulez differs from package.json; run npm ci --include=dev --ignore-scripts')
    config = configuration(root)
    with tempfile.TemporaryDirectory(prefix='ghost-ai-rulez-') as temporary:
        staging = Path(temporary)
        member = staging / PACKAGE
        # Assemble authored shared resources and supply the npm version before
        # rendering the released marketplace/member format in a fresh tree.
        build(root, member / 'payload/skills')
        write_toml(staging / '.ai-rulez/config.toml', {
            'version': '5.0', 'name': MARKETPLACE, 'gitignore': False,
            'marketplace': {'name': MARKETPLACE, 'description': shared['description'],
                            'members': [str(PACKAGE)], 'owner': shared['author']},
        })
        config['plugin'].update(version=shared['version'], content_root='payload')
        write_toml(member / '.ai-rulez/config.toml', config)
        executable = ROOT / 'node_modules/.bin/ai-rulez'
        for action in ('generate', 'verify'):
            result = subprocess.run([str(executable), action, '--plugin'], cwd=staging,
                                    capture_output=True, text=True, timeout=90)
            if result.returncode:
                raise ValueError(f'ai-rulez {action} failed: {result.stderr}')
        for path in MANIFEST_PATHS:
            source = member / path if path.name == 'plugin.json' else staging / path
            destination = output / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        # Publish plain canonical content with portable resource links, rather
        # than tool provenance headers in user-facing templates and procedures.
        build(root, output / PACKAGE / 'skills')
        shutil.copytree(output / PACKAGE / 'skills', output / 'skills')
        for directory in ('.claude-plugin', '.codex-plugin'):
            destination = output / PACKAGE / directory / 'plugin.json'
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(member / directory / 'plugin.json', destination)
        # npm tooling and Pi declarations remain authored; plugin metadata is
        # derived from TOML, while the npm version remains the release authority.
        package.update(shared)
        write_json(output / 'package.json', package)
        # Keep the committed authoring config valid for native ai-rulez commands.
        # Its required plugin.version is a generated mirror, never an authority.
        source = root / SOURCE / 'config.toml'
        text = source.read_text(encoding='utf-8')
        section = re.search(r'(?ms)^\[plugin\]\n(.*?)(?=^\[|\Z)', text)
        if section is None:
            raise ValueError('Expected an explicit [plugin] table')
        body, replacements = re.subn(r'(?m)^version\s*=.*$',
                                     'version = ' + json.dumps(shared['version']), section[1])
        if replacements != 1:
            raise ValueError('Expected one plugin version mirror')
        destination = output / SOURCE / 'config.toml'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text[:section.start(1)] + body + text[section.end(1):], encoding='utf-8')


def differences(expected: Path, actual: Path) -> list[str]:
    def paths(directory: Path) -> dict[str, Path]:
        if not directory.is_dir() or directory.is_symlink():
            return {}
        return {str(p.relative_to(directory)): p for p in directory.rglob('*')}
    wanted, found = paths(expected), paths(actual)
    problems = [f'missing: {name}' for name in sorted(wanted.keys() - found.keys())]
    problems += [f'extra: {name}' for name in sorted(found.keys() - wanted.keys())]
    for name in sorted(wanted.keys() & found.keys()):
        left, right = wanted[name], found[name]
        if right.is_symlink():
            problems.append(f'symlink: {name}')
        elif left.is_dir() != right.is_dir():
            problems.append(f'type mismatch: {name}')
        elif left.is_file() and left.read_bytes() != right.read_bytes():
            problems.append(f'changed: {name}')
    return problems


def sync(root: Path, check: bool = False) -> list[str]:
    with tempfile.TemporaryDirectory(prefix='ghost-packaging-') as temporary:
        expected = Path(temporary)
        generate(root, expected)
        directory_targets = (PACKAGE, Path('skills'))
        targets = [*MANIFEST_PATHS, *directory_targets, Path('package.json'), SOURCE / 'config.toml']
        for target in targets:
            destination = root / target
            for parent in (destination, *destination.parents):
                if parent == root.parent:
                    break
                if parent.is_symlink():
                    raise ValueError(f'Symlinked generated path: {parent}')
        if check:
            problems = []
            for target in targets:
                destination = root / target
                if target in directory_targets:
                    problems.extend(f'{target}: {p}' for p in differences(expected / target, destination))
                elif not destination.is_file():
                    problems.append(f'missing: {target}')
                elif destination.read_bytes() != (expected / target).read_bytes():
                    problems.append(f'changed: {target}')
            return problems
        for target in targets:
            destination = root / target
            if target in directory_targets:
                if destination.exists():
                    if not destination.is_dir():
                        raise ValueError(f'Generated package must be a directory: {destination}')
                    shutil.rmtree(destination)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(expected / target, destination)
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                if not destination.is_file() or destination.read_bytes() != (expected / target).read_bytes():
                    shutil.copyfile(expected / target, destination)
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
