# Contributor instructions

This repository distributes skills for maintaining ghost libraries. It contains packaging and evaluation tools, not implementations of the ghost libraries themselves.

## Ownership

- Edit procedures in `.ai-rulez/skills/ghost-*/SKILL.md` and their `agents/openai.yaml` metadata.
- Edit shared guidance in `.ai-rulez/references/` and artifact templates in `.ai-rulez/templates/`.
- Edit plugin identity, runtimes, and Codex display options in `.ai-rulez/config.toml`.
  It reads the plugin version from `package.json` (`version_from`); do not add a literal `version`.
- Edit the release version and npm tooling in `package.json`.
  It is the sole plugin version source;
  ai-rulez generates its identity fields, `pi`, and `files` from TOML.
- Generate root `skills/`, `.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/marketplace.json`, and `.ai-rulez-generated.json` with `make sync`.
  Both catalogs install the repository root, so keep host-loaded paths such as `.mcp.json`, `hooks/`, `agents/`, and `commands/` out of it.
  Do not independently edit these outputs.
- Keep maintainer governance here and in contributor documentation; do not inject it into distributed skills.

## Checks

After a canonical skill, resource, or metadata change, run `make sync`, then `make check-all`. Checks must report drift without repairing the checkout. Bundle builds use disposable destinations; explicit development builds use an absent or empty destination under `dist/`.

Use the existing standard-library Python tooling and unittest conventions.
CI's Python version is in `.python-version` and its Node version is in `.node-version`;
locally, `make check-all PYTHON="uv run --no-project python"` uses the selected Python interpreter.
The Makefile installs the locked ai-rulez development dependency when needed.
ai-rulez generates and verifies the packaging in place from the committed TOML configuration;
our wrapper adds the strict check that root `skills/` holds only files ai-rulez recorded.
Read [the integration guide](docs/ai-rulez.md) before changing that boundary.

Native host tests use isolated profiles and disposable repositories. Preserve the real user's settings, authentication, and installed packages. Keep authenticated model evaluations separate from ordinary CI, and scope support claims to saved evidence in `evals/results/`.

## Releases

Use Conventional Commit PR titles. Release-please owns `CHANGELOG.md` and the release manifest. It bumps `package.json`; release automation regenerates the host payload on the release PR and validates it. Release creation requires the exact validated release merge and no older pending release. Follow [CONTRIBUTING.md](CONTRIBUTING.md) for setup and recovery.
