#!/usr/bin/env python3
"""Build native host bundles without installing anything."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import tempfile

try:
    from .build_skills import ROOT, build
    from .sync_packaging import load_object, metadata, sync, write_json
except ImportError:
    from build_skills import ROOT, build
    from sync_packaging import load_object, metadata, sync, write_json


HOSTS = {"claude": ".claude-plugin", "codex": ".codex-plugin"}
CATALOGS = {"claude": ".claude-plugin", "codex": ".agents/plugins"}
SKILL_PATHS = {
    "claude": "plugins/ghost-library-skills/skills",
    "codex": "plugins/ghost-library-skills/skills",
    "opencode": ".opencode/skills",
    "pi": "skills",
}


def build_plugins(root: Path, output: Path) -> dict[str, int]:
    shared = metadata(root)
    problems = sync(root, check=True)
    if problems:
        raise ValueError('Stale native packaging; run make sync: ' + '; '.join(problems))
    if output.is_symlink():
        raise ValueError(f"Output must not be a symlink: {output}")
    output = output.resolve()
    if output.is_relative_to(root.resolve()):
        relative = output.relative_to(root.resolve())
        if not relative.parts or relative.parts[0] != "dist":
            raise ValueError("Use dist/ for output inside the source repository")
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError(f"Output must be absent or empty: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".ghost-plugins-", dir=output.parent))
    counts = {}
    try:
        for host, manifest_directory in HOSTS.items():
            manifest = load_object(root / manifest_directory / 'plugin.json')
            marketplace = load_object(root / CATALOGS[host] / 'marketplace.json')
            if host == 'claude':
                marketplace['plugins'][0]['source'] = './plugins/ghost-library-skills'
            host_root = staging / host
            plugin = host_root / "plugins" / shared["name"]
            counts[host] = build(root, plugin / "skills")
            write_json(plugin / manifest_directory / "plugin.json", manifest)
            write_json(host_root / CATALOGS[host] / "marketplace.json", marketplace)
        counts["opencode"] = build(root, staging / "opencode" / SKILL_PATHS["opencode"])
        package = load_object(root / 'package.json')
        package['files'] = ['skills/']
        counts["pi"] = build(root, staging / "pi" / SKILL_PATHS["pi"])
        write_json(staging / "pi/package.json", package)
        staging.replace(output)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="Absent or empty build directory")
    args = parser.parse_args()
    try:
        counts = build_plugins(ROOT, args.output)
        for host, count in counts.items():
            print(f"Built {host} bundle with {count} skills in {args.output.resolve() / host}")
    except (ValueError, OSError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
