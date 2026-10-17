#!/usr/bin/env python3
"""Exercise native installation/replacement with unauthenticated private profiles."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import uuid

try:
    from .build_plugins import SKILL_PATHS, load_object
    from .build_skills import validate_links
    from .smoke_plugins import app_server
except ImportError:
    from build_plugins import SKILL_PATHS, load_object
    from build_skills import validate_links
    from smoke_plugins import app_server


def fingerprint(root: Path) -> dict:
    files = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(root.rglob('*')) if p.is_file()}
    return {"files": len(files), "sha256": hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()}


CLAUDE_VOLATILE_KEYS = ('cachedGrowthBookFeaturesAt', 'pluginUsage')


def claude_configuration_fields() -> dict:
    path = Path.home() / '.claude.json'
    config = json.loads(path.read_bytes()) if path.is_file() else {}
    return {key: hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()
            for key, value in config.items() if key not in CLAUDE_VOLATILE_KEYS}


def real_configuration() -> dict:
    user_directory = Path.home()
    paths = [user_directory / '.claude.json', user_directory / '.claude/settings.json',
             user_directory / '.claude/plugins/installed_plugins.json', user_directory / '.claude/plugins/known_marketplaces.json',
             user_directory / '.codex/config.toml', user_directory / '.pi/agent/settings.json',
             user_directory / '.config/opencode/opencode.json', user_directory / '.config/opencode/opencode.jsonc']
    fingerprints = {}
    for path in paths:
        if not path.is_file():
            fingerprints[str(path)] = None
            continue
        content = path.read_bytes()
        if path.name == '.claude.json':
            config = json.loads(content)
            for key in CLAUDE_VOLATILE_KEYS:
                config.pop(key, None)
            content = json.dumps(config, sort_keys=True).encode()
        fingerprints[str(path)] = hashlib.sha256(content).hexdigest()
    return fingerprints


def exercise(bundle: Path, archive: Path, pi_loader: Path, output: Path, repository: bool = False) -> dict:
    if output.exists():
        raise ValueError('Output directory must be absent')
    if output.resolve().is_relative_to(bundle.resolve()):
        relative = output.resolve().relative_to(bundle.resolve())
        if not relative.parts or relative.parts[0] != 'dist':
            raise ValueError('Use dist/ for evaluation output inside the source checkout')
    output.mkdir(parents=True)
    commands = []
    container = f'ghost-install-{uuid.uuid4().hex[:10]}'
    container_started = False
    before_config = real_configuration()
    before_claude_fields = claude_configuration_fields()
    current = output / 'current'
    live = output / 'live'
    ignore = shutil.ignore_patterns('.git', 'dist', 'node_modules', '__pycache__', '*.pyc')
    shutil.copytree(bundle, current, ignore=ignore)
    shutil.copytree(current, live)
    pi_path = Path('.') if repository else Path('pi')
    claude_path = Path('.') if repository else Path('claude')
    catalog = load_object(current / claude_path / '.claude-plugin/marketplace.json')['name']
    plugin_id = f'ghost-library-skills@{catalog}'
    selected_paths = dict.fromkeys(SKILL_PATHS, 'skills') if repository else SKILL_PATHS
    version = load_object(current / pi_path / 'package.json')['version']
    if version == '0.0.0':
        raise ValueError('Current bundle must differ from synthetic version 0.0.0')
    for manifest in [*live.rglob('plugin.json'), live / pi_path / 'package.json']:
        value = json.loads(manifest.read_text())
        value['version'] = '0.0.0'
        manifest.write_text(json.dumps(value))
    for path in live.rglob('marketplace.json'):
        value = load_object(path)
        for entry in value.get('plugins', []):
            if entry.get('name') == 'ghost-library-skills' and 'version' in entry:
                entry['version'] = '0.0.0'
        path.write_text(json.dumps(value))
    for skill in live.rglob('ghost-audit/SKILL.md'):
        skill.write_text(skill.read_text() + '\nInstallation test marker: OLD_RELEASE_ONLY\n')
        (skill.parent / 'old-release-only.txt').write_text('OLD_RELEASE_ONLY\n')
    workspace = output / 'workspace'
    workspace.mkdir()
    env_claude = dict(os.environ, CLAUDE_CONFIG_DIR=str(output / 'claude-profile'))
    for key in list(env_claude):
        if key.startswith(('ANTHROPIC_', 'CLAUDE_CODE_')):
            del env_claude[key]
    env_pi = dict(os.environ, PI_CODING_AGENT_DIR=str(output / 'pi-profile'), PI_OFFLINE='1', PI_TELEMETRY='0')
    env_open = dict(os.environ, OPENCODE_CONFIG_DIR=str(output / 'opencode-profile'),
                    OPENCODE_DISABLE_CLAUDE_CODE='1', OPENCODE_DISABLE_EXTERNAL_SKILLS='1',
                    OPENCODE_DISABLE_MODELS_FETCH='1', OPENCODE_DISABLE_AUTOUPDATE='1',
                    OPENCODE_DISABLE_DEFAULT_PLUGINS='1')
    for key, folder in [('XDG_CONFIG_HOME', 'config'), ('XDG_CACHE_HOME', 'cache'),
                        ('XDG_DATA_HOME', 'data'), ('XDG_STATE_HOME', 'state')]:
        env_open[key] = str(output / 'opencode-xdg' / folder)
    open_skills = output / 'opencode-profile/skills'
    if repository:
        env_open['OPENCODE_CONFIG'] = str(live / 'opencode.json')
    else:
        shutil.copytree(live / 'opencode/.opencode/skills', open_skills)
    pi_program = output / 'pi-discover.mjs'
    pi_program.write_text(
        f'import {{ DefaultResourceLoader }} from {json.dumps(pi_loader.as_uri())};\n'
        'const loader = new DefaultResourceLoader({cwd:process.cwd(),agentDir:process.env.PI_CODING_AGENT_DIR,'
        'noExtensions:true,noPromptTemplates:true,noThemes:true,noContextFiles:true});\n'
        'await loader.reload(); console.log(JSON.stringify(loader.getSkills()));\n')

    def run(command: list[str], env: dict | None = None, allow_failure: bool = False, cwd: Path | None = None) -> str:
        configuration_before = real_configuration()
        result = subprocess.run(command, cwd=cwd or workspace, env=env, capture_output=True, text=True, timeout=90)
        configuration_after = real_configuration()
        commands.append({'argv': command, 'exit_code': result.returncode, 'stderr': result.stderr[-1000:],
                         'configuration_changes': [p for p in configuration_before if configuration_before[p] != configuration_after[p]]})
        if result.returncode and not allow_failure:
            raise RuntimeError(f'{command[:3]} failed: {result.stderr[-1000:]} {result.stdout[-1000:]}')
        return result.stdout

    codex = ['docker', 'exec', container, '/evaluation/codex-aarch64-unknown-linux-musl']

    def discover(stage: str) -> dict:
        claude_output = run(['claude', '--print', '--verbose', '--output-format', 'stream-json',
                             '--no-session-persistence', '--settings', '{"disableAllHooks":true}',
                             '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}', '--no-chrome',
                             '--permission-mode', 'dontAsk', '--tools', '', '--',
                             '/ghost-library-skills:ghost-audit Audit this empty workspace.'], env_claude, True)
        events = [json.loads(line) for line in claude_output.splitlines() if line.startswith('{')]
        init = next(e for e in events if e.get('type') == 'system' and e.get('subtype') == 'init')
        if init.get('apiKeySource') != 'none' or not any(e.get('error') == 'authentication_failed' for e in events):
            raise RuntimeError('Claude startup probe must stop for missing authentication')
        plugin = next(p for p in init['plugins'] if p['name'] == 'ghost-library-skills')
        claude_names = [s for s in init['skills'] if s.startswith('ghost-library-skills:')]
        pi = json.loads(run(['node', str(pi_program)], env_pi))
        pi_skills = [s for s in pi['skills'] if s['name'].startswith('ghost-')]
        if pi['diagnostics']:
            raise RuntimeError(f'Pi skill diagnostics: {pi["diagnostics"]}')
        opencode = json.loads(run(['opencode', 'debug', 'skill', '--pure'], env_open, cwd=live if repository else workspace))
        open_skills_found = [s for s in opencode if s['name'].startswith('ghost-')]
        with app_server(workspace, ['docker', 'exec', '-i', container,
                                   '/evaluation/codex-aarch64-unknown-linux-musl', 'app-server', '--stdio']) as server:
            inventory = server.request('skills/list', {'cwds': ['/evaluation/workspace'], 'forceReload': True})
        codex_skills = [s for row in inventory['data'] for s in row['skills'] if s.get('pluginId') == plugin_id]
        names = {'claude': claude_names, 'codex': [s['name'] for s in codex_skills],
                 'pi': [s['name'] for s in pi_skills], 'opencode': [s['name'] for s in open_skills_found]}
        expected = {p.parent.name for p in (current / pi_path / 'skills').glob('*/SKILL.md')}
        for host, values in names.items():
            if len(values) != len(expected) or {v.split(':')[-1] for v in values} != expected:
                raise RuntimeError(f'{host} inventory differs: {values}')
        codex_root = str(Path(codex_skills[0]['path']).parents[2])
        exported = output / f'codex-cache-{stage}'
        run(['docker', 'cp', f'{container}:{codex_root}', str(exported)])
        roots = {'claude': Path(plugin['path']) / 'skills', 'codex': exported / 'skills',
                 'pi': Path(pi_skills[0]['baseDir']).parent, 'opencode': Path(open_skills_found[0]['location']).parent.parent}
        snapshots = {}
        for host, root in roots.items():
            validate_links(root, list(root.rglob('*.md')))
            old_marker = 'OLD_RELEASE_ONLY' in (root / 'ghost-audit/SKILL.md').read_text()
            digest = fingerprint(root)
            if stage == 'after' and digest != fingerprint(current / selected_paths[host] if repository else current / host / selected_paths[host]):
                raise RuntimeError(f'{host} active payload differs from current bundle')
            if old_marker != (stage == 'before') or (root / 'ghost-audit/old-release-only.txt').exists() != (stage == 'before'):
                raise RuntimeError(f'{host} replacement marker mismatch')
            snapshots[host] = {'skills': sorted(names[host]), 'payload': digest, 'old_marker': old_marker,
                               'resource_links_valid': True, 'active_root': str(root)}
        snapshots['claude']['version'] = plugin['version']
        snapshots['claude']['model_invocation'] = 'not_authenticated_in_private_profile'
        snapshots['codex']['version'] = Path(codex_root).name
        for host in ['claude', 'codex']:
            if snapshots[host]['version'] != ('0.0.0' if stage == 'before' else version):
                raise RuntimeError(f'{host} selected the wrong version')
        return snapshots

    try:
        with tarfile.open(archive) as packed:
            members = packed.getmembers()
            if len(members) != 1 or members[0].name != 'codex-aarch64-unknown-linux-musl' or not members[0].isfile():
                raise ValueError('Expected the official Codex Linux arm64 musl single-binary archive')
            packed.extractall(output, members=members, filter='data')
        run(['docker', 'run', '-d', '--name', container, '--network', 'none', '-v', f'{output}:/evaluation',
             'alpine:latest', 'sleep', '1800'])
        container_started = True
        container_image = run(['docker', 'inspect', container, '--format', '{{.Image}}']).strip()
        versions = {h: run([h, '--version'], env).strip()
                    for h, env in [('claude', env_claude), ('opencode', env_open), ('pi', env_pi)]}
        versions['codex'] = run([*codex, '--version']).strip()
        run(['claude', 'plugin', 'marketplace', 'add', str(live / claude_path)], env_claude)
        run(['claude', 'plugin', 'install', plugin_id, '--json'], env_claude)
        run([*codex, 'plugin', 'marketplace', 'add', '/evaluation/live' if repository else '/evaluation/live/codex'])
        run([*codex, 'plugin', 'add', plugin_id])
        run(['pi', 'install', str(live / pi_path)], env_pi)
        before = discover('before')
        shutil.rmtree(live)
        shutil.copytree(current, live)
        if not repository:
            shutil.rmtree(open_skills)
            shutil.copytree(live / 'opencode/.opencode/skills', open_skills)
        run(['claude', 'plugin', 'marketplace', 'update', catalog], env_claude)
        run(['claude', 'plugin', 'update', plugin_id], env_claude)
        run([*codex, 'plugin', 'add', plugin_id])
        run(['pi', 'update', str(live / pi_path)], env_pi)
        after = discover('after')
        after_config = real_configuration()
        after_claude_fields = claude_configuration_fields()
        unchanged = before_config == after_config
        return {'success': unchanged, 'source_kind': 'repository' if repository else 'bundle', 'versions': versions, 'before': before, 'after': after,
                'container_image': container_image,
                'codex_binary_sha256': hashlib.sha256((output / 'codex-aarch64-unknown-linux-musl').read_bytes()).hexdigest(),
                'real_configuration_unchanged': unchanged, 'model_inference_tested': False,
                'configuration_guard': {'claude_json': 'normalized JSON', 'ignored_volatile_keys': list(CLAUDE_VOLATILE_KEYS),
                                        'other_files': 'byte SHA-256'},
                'changed_configuration_paths': [p for p in before_config if before_config[p] != after_config[p]],
                'changed_claude_configuration_keys': [key for key in before_claude_fields.keys() | after_claude_fields.keys()
                                                    if before_claude_fields.get(key) != after_claude_fields.get(key)],
                'replacement_methods': {'claude': 'marketplace update; plugin update; fresh process',
                                        'codex': 'plugin add again; fresh app-server',
                                        'pi': 'local path replaced; pi update; fresh resource loader',
                                        'opencode': 'checkout replaced; root config discovery' if repository else 'skill directory replaced; fresh debug skill process'},
                'commands': commands}
    finally:
        if container_started:
            subprocess.run(['docker', 'rm', '-f', container], capture_output=True, timeout=30)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--bundle', type=Path)
    source.add_argument('--repository', type=Path, help='Test installation directly from a disposable copy of a checkout')
    parser.add_argument('--codex-linux-archive', required=True, type=Path)
    parser.add_argument('--pi-resource-loader', required=True, type=Path, help='Installed Pi dist/core/resource-loader.js')
    parser.add_argument('--output', required=True, type=Path, help='Absent directory for private profiles and evidence')
    args = parser.parse_args()
    if args.output.exists():
        parser.exit(1, 'Output directory must be absent\n')
    try:
        result = exercise((args.repository or args.bundle).resolve(), args.codex_linux_archive.resolve(), args.pi_resource_loader.resolve(), args.output.resolve(), repository=args.repository is not None)
    except (ValueError, OSError, RuntimeError, subprocess.SubprocessError, StopIteration) as error:
        result = {'success': False, 'error': str(error)}
    if args.output.is_dir():
        (args.output / 'report.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ['before', 'after', 'commands']}, indent=2))
    raise SystemExit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()
