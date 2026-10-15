# Host support

Twelve generated skills are available directly from this checkout. The host evidence below was recorded with the original seven; the five later skills (`ghost-summon`, `ghost-evaluate`, `ghost-extract`, `ghost-upgrade`, `ghost-catalog`) use the same packaging path but have not been rediscovered on each host. This file is the single capability record; the install guides cite it rather than restating it.

| Host | Evidence and limits | Install guide |
| --- | --- | --- |
| Claude Code 2.1.296 | Strict root manifest/catalog validation; private-profile root installation and version replacement; installation from a GitHub branch; seven discovered commands. Authenticated workflows remain weekly-quota blocked | [install-claude-code.md](install-claude-code.md) |
| Codex CLI 0.162.1 | Root catalog parsing/discovery; network-disabled container installation and version replacement; installation from a GitHub branch; seven discovered skills. Earlier model trials are recorded separately | [install-codex.md](install-codex.md) |
| Pi 1.0.3 | Private-profile root-package installation and local-path update; native resource loader discovers seven skills and resolves shared resources. Model workflows untested | [install-pi.md](install-pi.md) |
| OpenCode 1.18.35 | Root configuration discovers seven generated skills when run from the checkout; replacement and resource checks pass. Relative skill paths resolve from the working directory. Model workflows untested | [install-opencode.md](install-opencode.md) |
| Antigravity | Hand-authored root `plugin.json` adapter, verified against canonical metadata by `make check`. Local `agy plugin validate` discovers twelve skills, no commands/agents/hooks ([evidence](../evals/results/hosts/antigravity/README.md)). Git-URL installation and model workflows not evaluated | [install-antigravity.md](install-antigravity.md) |
| Hermes | Standalone skill folders; native integrations not implemented | — |

The root catalog installs the repository root (`./`) as the plugin; Claude and Codex load the skills from root `skills/`, the same payload Pi and OpenCode use.

The [single-plugin report](../evals/results/automation/single-plugin/README.md) records the current layout, in which both catalogs install the repository root. The earlier [repository installation report](../evals/results/hosts/repository/README.md) records the member layout. The earlier [bundle installation report](../evals/results/hosts/installation/README.md), [six-workflow assessment](../evals/results/native/README.md), and [wheredirs evaluation](../evals/wheredirs/README.md) retain their original scope. Packaging checks and completed model turns do not establish task success by themselves. Desktop applications and npm/Git package upgrades have not been evaluated.

## Install

Install and update commands live in the per-host guides linked in the table above; this file records capabilities and evidence only. Use the absolute path to this repository. Consumers do not need to run the Python builder first.

## Repository publication and previous installations

This migration is tested from a local checkout. GitHub-source installation becomes available after these manifests and the generated Codex package are committed and published; it has not been tested against the current remote repository. Claude and Codex support repository marketplace sources, while Pi supports Git packages. Keep this distinction when writing release instructions.

Earlier evaluations used `ghost-library-local` and then `ghost-library-marketplace`.
The project is now named `ghost-library-skills`, with catalog `ghost-library-skills-marketplace`. Upgrading an existing real-profile installation across that marketplace-name change has not been tested. Install one distribution at a time to avoid duplicate registrations.

## Maintain generated packaging

`.ai-rulez/config.toml` owns plugin identity, runtime selection, and Codex display options.
`package.json` owns the release version and npm tooling;
ai-rulez generates its identity fields, Pi declaration, and npm file allowlist from TOML.
`tools/sync_packaging.py` runs the pinned ai-rulez development dependency in the checkout
and rejects files under `skills/` that ai-rulez did not record.
See [the integration guide](ai-rulez.md) for ownership boundaries.
Edit `.ai-rulez/` skill sources, shared resources, and metadata, then run:

```sh
make sync
make check
```

`make check` reports stale generated files without repairing them, validates resource links, and runs unit tests. Keep generated root `skills/`, manifests, and catalogs in version control. It also fails when the root gains a path Claude or Codex would load from the installed plugin, such as `.mcp.json` or `hooks/` (ai-rulez `AR9T0`).
Author skill procedures under `.ai-rulez/skills/`, shared resources under `.ai-rulez/references/` and `.ai-rulez/templates/`,
and plugin metadata in `.ai-rulez/config.toml`.
`package.json` remains the release version authority.

## Build disposable bundles

```sh
make build OUTPUT=dist/plugins
```

The output must be absent or empty. The builder consumes root metadata/manifests and produces the existing `claude/`, `codex/`, `opencode/`, and `pi/` bundle layouts. Standalone folders remain available through `python3 tools/build_skills.py --output PATH`.

## Reproduce native checks

Validate root Claude metadata and Codex discovery without installation or inference:

```sh
python3 tools/smoke_plugins.py --repository . --report dist/repository-validation.json
```

For a built bundle, substitute `--bundle dist/plugins`. To additionally run a read-only Codex audit with existing authentication, add `--invoke-codex /absolute/path/to/disposable-workspace --target contract`. The target must be a directory within that workspace. This explicit option performs model inference.

For installation/replacement, install the four host CLIs and Docker. Provide the official Codex Linux arm64 musl archive and locate Pi's installed `dist/core/resource-loader.js`:

```sh
gh release download rust-v0.160.0 --repo openai/codex \
  --pattern codex-aarch64-unknown-linux-musl.tar.gz --dir /tmp/ghost-codex-release
python3 tools/smoke_installation.py --repository . \
  --codex-linux-archive /tmp/ghost-codex-release/codex-aarch64-unknown-linux-musl.tar.gz \
  --pi-resource-loader /absolute/path/to/pi-coding-agent/dist/core/resource-loader.js \
  --output /tmp/ghost-repository-installation-check
```

The output must be absent.
The script copies the checkout,
excludes Git/build/cache directories and `node_modules/`,
creates a marked old version, installs it in private profiles,
replaces it with the current checkout, and checks fresh discovery, active resource hashes, removed resources, and local Markdown links.
Codex runs in a network-disabled container without real profiles or credentials;
the container is removed afterward.
Profiles and evidence remain for inspection.
Claude's startup probe strips authentication variables and must stop for missing authentication;
the other host checks do not request inference.
The guard normalizes `.claude.json` and excludes the independently observed volatile `cachedGrowthBookFeaturesAt` and `pluginUsage` fields;
all other fields remain guarded.
Other watched files use byte hashes.
Run separately from processes that modify real preferences or plugin configuration.
