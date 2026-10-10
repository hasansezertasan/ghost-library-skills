# Host support

Seven generated skills are available directly from this checkout. Claude and Codex have native marketplace catalogs, Pi has a root skill-package declaration, and OpenCode has a native skill-path configuration. A separate builder produces self-contained bundles for evaluation and standalone installation.

| Host | Evidence and limits |
| --- | --- |
| Claude Code 2.1.296 | Strict root manifest/catalog validation; private-profile root installation and version replacement; installation from a GitHub branch; seven discovered commands. Authenticated workflows remain weekly-quota blocked |
| Codex CLI 0.162.1 | Root catalog parsing/discovery; network-disabled container installation and version replacement; installation from a GitHub branch; seven discovered skills. Earlier model trials are recorded separately |
| OpenCode 1.18.35 | Root configuration discovers seven generated skills when run from the checkout; replacement and resource checks pass. Relative skill paths resolve from the working directory. Model workflows untested |
| Pi 1.0.3 | Private-profile root-package installation and local-path update; native resource loader discovers seven skills and resolves shared resources. Model workflows untested |
| Hermes, Antigravity | Standalone skill folders; native integrations not implemented |

The [single-plugin report](../evals/results/automation/single-plugin/README.md) records the current layout, in which both catalogs install the repository root. The earlier [repository installation report](../evals/results/hosts/repository/README.md) records the member layout. The earlier [bundle installation report](../evals/results/hosts/installation/README.md), [six-workflow assessment](../evals/results/native/README.md), and [wheredirs evaluation](../evals/wheredirs/README.md) retain their original scope. Packaging checks and completed model turns do not establish task success by themselves. Desktop applications and npm/Git package upgrades have not been evaluated.

## Install from a checkout

Use the absolute path to this repository. Consumers do not need to run the Python builder first.

### Claude Code

```sh
claude plugin marketplace add /absolute/path/to/ghost-library-skills
claude plugin install ghost-library-skills@ghost-library-skills-marketplace
```

Invoke `/ghost-library-skills:ghost-audit` with the target and requested outcome. After updating the checkout:

```sh
claude plugin marketplace update ghost-library-skills-marketplace
claude plugin update ghost-library-skills@ghost-library-skills-marketplace
```

Restart or reload plugins afterward.
The root catalog installs the repository root (`./`) as the plugin;
Claude loads the seven skills from root `skills/`, the same payload used by Codex, Pi, and OpenCode.
For a session-local trial, use `claude --plugin-dir /absolute/path/to/ghost-library-skills`.
See [Claude plugins](https://code.claude.com/docs/en/plugins).

### Codex

```sh
codex plugin marketplace add /absolute/path/to/ghost-library-skills
codex plugin add ghost-library-skills@ghost-library-skills-marketplace
```

Select `ghost-library-skills:ghost-audit` and provide a task. The root catalog installs the repository root (`./`); Codex loads the self-contained skill folders in root `skills/`. For a local version update, refresh the checkout, repeat `codex plugin add ghost-library-skills@ghost-library-skills-marketplace`, and start a fresh session. The tested CLI has no `plugin update`; `plugin marketplace upgrade` refreshes Git marketplace snapshots. See the [OpenAI plugin build guide](https://developers.openai.com/plugins/build/plugins).

### Pi

```sh
pi install /absolute/path/to/ghost-library-skills
```

Invoke `/skill:ghost-audit` with a task. After updating the checkout, run `pi update /absolute/path/to/ghost-library-skills` and restart or reload resources. Local packages load from the source path without copying. The root manifest exposes only skills; each generated skill contains its references and templates with skill-local relative links. See [Pi packages](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md).

### OpenCode

From this checkout, run `opencode`. Its root `opencode.json` declares `skills.paths: ["./skills"]`.

To discover the skills from another project, add an absolute path to that project's existing OpenCode configuration:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["/absolute/path/to/ghost-library-skills/skills"]
  }
}
```

Merge this field into existing configuration. Ask OpenCode to use `ghost-audit`; it loads the instructions through its native `skill` tool. On the tested CLI, pointing `OPENCODE_CONFIG` at our root config while running elsewhere does not resolve `./skills` relative to the config file. Use an absolute skill path for that case. See the [configuration schema](https://opencode.ai/config.json) and [Agent Skills documentation](https://opencode.ai/docs/skills/).

### Repository publication and previous installations

This migration is tested from a local checkout. GitHub-source installation becomes available after these manifests and the generated Codex package are committed and published; it has not been tested against the current remote repository. Claude and Codex support repository marketplace sources, while Pi supports Git packages. Keep this distinction when writing release instructions.

Earlier evaluations used `ghost-library-local` and then `ghost-library-marketplace`.
The project is now named `ghost-library-skills`, with catalog `ghost-library-skills-marketplace`. Upgrading an existing real-profile installation across that marketplace-name change has not been tested. Install one distribution at a time to avoid duplicate registrations.

## Maintain generated packaging

`.ai-rulez/config.toml` owns plugin identity, runtime selection, and Codex display options.
`package.json` owns the release version, npm tooling, Pi declaration, and npm file allowlist;
its plugin identity fields are generated from TOML.
`tools/sync_packaging.py` delegates native JSON rendering to the pinned ai-rulez development dependency,
then materializes the shared Claude/Codex payload with the existing resource builder.
See [the integration guide](ai-rulez.md) for ownership and staging boundaries.
Edit `.ai-rulez/` skill sources, shared resources, and metadata, then run:

```sh
make sync
make check
```

`make check` reports stale generated files without repairing them, validates resource links, and runs unit tests. Keep generated root `skills/`, manifests, and catalogs in version control. It also fails when the root gains a path Claude or Codex would load from the installed plugin, such as `.mcp.json` or `hooks/`.
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
