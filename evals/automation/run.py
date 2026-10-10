#!/usr/bin/env python3
"""Evaluate a pinned ai-rulez executable against disposable ghost-library sources."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.build_skills import build, validate_links
from tools.smoke_plugins import app_server, claude_validation
from tools.sync_packaging import manifests


def snapshot(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}


def command(executable: Path, root: Path, *args: str) -> dict:
    result = subprocess.run([str(executable), *args], cwd=root, text=True,
                            capture_output=True, timeout=120)
    return {'arguments': list(args), 'exit_code': result.returncode,
            'stdout': result.stdout, 'stderr': result.stderr}


def prepare(output: Path, mode: str) -> tuple[Path, Path]:
    case = output / mode
    case.mkdir(parents=True)
    for name in ('references', 'templates'):
        shutil.copytree(ROOT / '.ai-rulez' / name, case / name)
    for name in ('package.json', 'opencode.json'):
        shutil.copyfile(ROOT / name, case / name)
    (case / 'README.md').write_text('# Disposable packaging prototype\n')
    source = case / ('.ai-rulez' if mode != 'content-root' else 'payload')
    shutil.copytree(ROOT / '.ai-rulez/skills', source / 'skills')
    (case / '.ai-rulez').mkdir(exist_ok=True)
    for name in ('references', 'templates'):
        shutil.copytree(ROOT / '.ai-rulez' / name, case / '.ai-rulez' / name)
    if source != case / '.ai-rulez':
        shutil.copytree(source / 'skills', case / '.ai-rulez/skills')
    package = json.loads((case / 'package.json').read_text())
    runtimes = ['claude', 'codex'] + (['opencode'] if mode == 'opencode' else [])
    # The checked npm identity is derived from TOML; use it for this raw-tool trial.
    config = '\n'.join([
        'version = "4.0"', 'name = "ghost-library-skills"', 'gitignore = false',
        '[header]', 'timestamp = false', '[plugin]',
        'name = "ghost-library-skills"', f'version = {json.dumps(package["version"])}',
        f'description = {json.dumps(package["description"])}',
        f'repository = {json.dumps(package["repository"])}',
        f'runtimes = {json.dumps(runtimes)}',
        *(['content_root = "payload"'] if mode == 'content-root' else []),
        '[plugin.author]', f'name = {json.dumps(package["author"]["name"])}',
        '[plugin.interface]', 'display_name = "Ghost Library"',
        'short_description = "Maintain behavioral contracts and portable fixtures"',
        f'long_description = {json.dumps(package["description"])}',
        f'developer_name = {json.dumps(package["author"]["name"])}',
        'category = "Development"', 'capabilities = ["Read", "Write"]',
        'default_prompt = ["Audit this ghost library."]', '',
    ])
    (case / '.ai-rulez/config.toml').write_text(config)
    return case, source


def evaluate(executable: Path, output: Path, native: bool) -> dict:
    results = {'version': command(executable, ROOT, 'version'), 'cases': {}}
    if native:
        results['host_versions'] = {name: subprocess.check_output([name, '--version'], text=True).strip()
                                    for name in ('claude', 'codex')}
    for mode in ('canonical', 'content-root', 'opencode'):
        case, source = prepare(output, mode)
        package_before = (case / 'package.json').read_bytes()
        entry = {'generate': command(executable, case, 'generate', '--plugin')}
        results['cases'][mode] = entry
        if entry['generate']['exit_code']:
            continue
        entry['verify'] = command(executable, case, 'verify', '--plugin')
        entry['package_json_preserved'] = (case / 'package.json').read_bytes() == package_before
        entry['pi_declaration_preserved'] = json.loads((case / 'package.json').read_text()).get('pi') == json.loads(package_before).get('pi')
        entry['codex_catalog_generated'] = (case / '.agents/plugins/marketplace.json').exists()
        entry['missing_skill_metadata'] = [str(p.relative_to(source)) for p in source.glob('skills/*/agents/openai.yaml')
                                           if not (case / p.relative_to(source)).exists()]
        entry['skill_metadata_preserved'] = all(
            (case / p.relative_to(source)).is_file()
            and (case / p.relative_to(source)).read_bytes() == p.read_bytes()
            for p in source.glob('skills/*/agents/openai.yaml'))
        header = re.compile(r'\n<!--\nAI-RULEZ :: GENERATED FILE.*?-->\n', re.S)
        entry['skill_frontmatter_and_body_preserved'] = all(
            header.sub('', (case / p.relative_to(source)).read_text()) == p.read_text()
            for p in source.glob('skills/*/SKILL.md'))
        try:
            validate_links(case, sorted((case / 'skills').rglob('*.md')))
            entry['root_resource_links_valid'] = True
            entry['standalone_skills_built'] = build(case, output / f'{mode}-standalone')
        except ValueError as error:
            entry['resource_error'] = str(error)
        if mode != 'canonical':
            continue
        if native:
            entry['claude_native_validation'] = claude_validation(case, repository=True)
            # Supply the catalog ai-rulez does not emit for a single-plugin repo.
            catalog = manifests(ROOT)[Path('.agents/plugins/marketplace.json')]
            catalog['plugins'][0]['source']['path'] = './'
            path = case / '.agents/plugins/marketplace.json'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(catalog, indent=2) + '\n')
            with app_server(case) as server:
                plugin = server.request('plugin/read', {'marketplacePath': str(path), 'pluginName': 'ghost-library-skills'})['plugin']
                entry['codex_registered_skills_with_custom_catalog'] = sorted(s['name'] for s in plugin['skills'])
        skill = case / 'skills/ghost-audit/SKILL.md'
        clean = skill.read_bytes()
        skill.write_bytes(clean + b'\nInjected generated-output drift.\n')
        before = snapshot(case)
        entry['changed_output_verification'] = command(executable, case, 'verify', '--plugin')
        entry['verification_did_not_repair'] = before == snapshot(case)
        skill.write_bytes(clean)
        extra = case / 'skills/ghost-audit/obsolete.txt'
        extra.write_text('unexpected generated resource\n')
        entry['extra_file_verification'] = command(executable, case, 'verify', '--plugin')
        extra.unlink()
        config = case / '.ai-rulez/config.toml'
        package = json.loads((case / 'package.json').read_text())
        previous = package['version']
        major, minor, patch = previous.split('.')
        package['version'] = f'{major}.{minor}.{int(patch) + 1}'
        config.write_text(config.read_text().replace(f'version = {json.dumps(previous)}',
                                                    f'version = {json.dumps(package["version"])}'))
        (case / 'package.json').write_text(json.dumps(package, indent=2) + '\n')
        entry['version_bump_verification'] = command(executable, case, 'verify', '--plugin')
        entry['version_bump_regeneration'] = command(executable, case, 'generate', '--plugin')
        entry['version_bump_recheck'] = command(executable, case, 'verify', '--plugin')
        entry['generated_versions_after_bump'] = {
            str(p.relative_to(case)): json.loads(p.read_text())['version']
            for p in (case / '.claude-plugin/plugin.json', case / '.codex-plugin/plugin.json')}
        shutil.rmtree(source / 'skills/ghost-init')
        entry['removed_skill_regeneration'] = command(executable, case, 'generate', '--plugin')
        entry['removed_skill_output_deleted'] = not (case / 'skills/ghost-init/SKILL.md').exists()
    canonical = results['cases']['canonical']
    results['migration_contracts'] = {
        'skill_metadata_preserved': canonical.get('skill_metadata_preserved', False),
        'codex_catalog_generated': canonical.get('codex_catalog_generated', False),
        'unexpected_files_rejected': canonical.get('extra_file_verification', {}).get('exit_code', 0) != 0,
        'removed_skill_deleted': canonical.get('removed_skill_output_deleted', False),
        'pi_manifest_preserved_with_opencode': results['cases']['opencode'].get('pi_declaration_preserved', False),
    }
    results['decision'] = ('migration-candidate' if all(results['migration_contracts'].values())
                           else 'retain-existing-generator')
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ai-rulez', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path, help='Absent directory outside this repository')
    parser.add_argument('--native', action='store_true', help='Also use installed Claude/Codex CLIs without model invocation')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() or output.is_relative_to(ROOT):
        parser.error('Output must be absent and outside the repository')
    output.mkdir(parents=True)
    results = evaluate(args.ai_rulez.resolve(), output, args.native)
    (output / 'report.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'Saved prototype evidence to {output / "report.json"}')


if __name__ == '__main__':
    main()
