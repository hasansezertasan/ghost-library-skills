#!/usr/bin/env python3
"""Validate local resource links and build self-contained Markdown skills."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(".ai-rulez")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def markdown_files(root: Path) -> list[Path]:
    files = [root / "README.md"]
    files.extend(root / name for name in ("AGENTS.md", "CONTRIBUTING.md")
                 if (root / name).exists() or (root / name).is_symlink())
    for directory in (str(SOURCE), "docs", "evals"):
        source = root / directory
        if source.exists():
            files.extend(sorted(source.rglob("*.md")))
    return files


def validate_links(root: Path, files: list[Path]) -> None:
    for file in files:
        if file.is_symlink() or not file.is_file():
            raise ValueError(f"Missing or symlinked Markdown file: {file}")
        for match in LINK.finditer(file.read_text(encoding="utf-8")):
            target = match.group(1).strip("<>")
            if target.startswith("#") or SCHEME.match(target):
                continue
            local = unquote(target.split("#", 1)[0])
            candidate = (file.parent / local).resolve()
            if not candidate.is_relative_to(root.resolve()):
                raise ValueError(f"Resource link escapes bundle: {file}: {target}")
            if not candidate.exists():
                raise ValueError(f"Missing resource link: {file}: {target}")


def validate_tree(root: Path) -> list[Path]:
    source = root / SOURCE
    if source.is_symlink():
        raise ValueError(f"Symlinked source directory: {source}")
    skills_root = source / "skills"
    if skills_root.is_symlink():
        raise ValueError(f"Symlinked source directory: {skills_root}")
    skills = sorted(skills_root.glob("*/SKILL.md"))
    if not skills:
        raise ValueError("No skills found")
    for directory in (skills_root, source / "references", source / "templates"):
        if directory.is_symlink() or not directory.is_dir():
            raise ValueError(f"Missing or symlinked source directory: {directory}")
        for path in directory.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"Symlinked source resource: {path}")
    for skill in skills:
        content = skill.read_text(encoding="utf-8")
        name = re.search(r"\A---\nname: ([a-z0-9-]+)\n", content)
        if not name or name.group(1) != skill.parent.name:
            raise ValueError(f"Skill name does not match folder: {skill}")
    validate_links(root, markdown_files(root))
    return skills


def build(root: Path, output: Path) -> int:
    skills = validate_tree(root)
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
    staging = Path(tempfile.mkdtemp(prefix=".ghost-skills-", dir=output.parent))
    try:
        for skill in skills:
            destination = staging / skill.parent.name
            shutil.copytree(skill.parent, destination)
            for shared in ("references", "templates"):
                shutil.copytree(root / SOURCE / shared, destination / shared)
            entrypoint = destination / "SKILL.md"
            content = entrypoint.read_text(encoding="utf-8")
            for shared in ("references", "templates"):
                content = content.replace(f"](../../{shared}/", f"]({shared}/")
            entrypoint.write_text(content, encoding="utf-8")
            validate_links(destination, sorted(destination.rglob("*.md")))
        staging.replace(output)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return len(skills)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Validate source resource links")
    mode.add_argument("--output", type=Path, help="Build into an absent or empty directory")
    args = parser.parse_args()
    try:
        if args.check:
            count = len(validate_tree(ROOT))
            print(f"Validated resource links for {count} skills")
        else:
            count = build(ROOT, args.output)
            print(f"Built {count} self-contained skills in {args.output.resolve()}")
    except (ValueError, OSError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
