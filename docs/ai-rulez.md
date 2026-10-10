# ai-rulez authoring and generation

Author plugin configuration and content in the committed `.ai-rulez/` tree.
The pinned npm development dependency renders Claude/Codex manifests and both catalogs;
our wrapper assembles shared resources, supplies the release version, and checks the complete output trees.

## Sources and ownership

| Content | Authored source |
| --- | --- |
| Procedures and Codex skill display metadata | `.ai-rulez/skills/ghost-*/` |
| Shared guidance | `.ai-rulez/references/` |
| Artifact templates | `.ai-rulez/templates/` |
| Plugin identity, runtime selection, and interface | `.ai-rulez/config.toml` |
| Release version, npm tooling, and Pi declarations | `package.json` |
| Maintainer governance | `AGENTS.md`, `CONTRIBUTING.md`, and `docs/` |

`package.json` is the sole authored plugin version source.
ai-rulez requires `[plugin].version` in a valid authoring configuration.
That field is a generated mirror of the npm version;
`make sync` updates it without changing other authored TOML content.
The TOML `version = "5.0"` is the configuration schema version, not the plugin release version.
Plugin identity fields in `package.json` are generated from TOML;
keep npm tooling, the Pi declaration, and the release version authored there.
Do not independently edit the TOML release-version mirror.

Shared references and templates are a local authoring convention.
ai-rulez documents supporting resources within each skill;
our builder copies the shared sources into each distributed skill and rewrites their links.
Generated skills can be moved independently, including their `agents/openai.yaml` metadata.

Root `skills/`, `.claude-plugin/`, `.codex-plugin/`, and `.agents/plugins/marketplace.json`
are generated distribution surfaces.
Keep them in version control so consumers need no generator installation.
Edit their sources and regenerate instead of editing generated content directly.

## Generation and verification

```sh
make sync
make check-all
```

Use these wrapper commands rather than running `ai-rulez generate --plugin` directly in the checkout.
They install the locked development tool when needed,
assemble resources in a fresh staging tree,
and supply the npm release version to the committed plugin configuration.
The wrapper then runs ai-rulez `generate --plugin` and `verify --plugin` in staging.
Python tooling uses the standard library;
CI interpreter versions are selected by `.python-version` and `.node-version`.

ai-rulez generates both catalogs in single-plugin mode:
`[marketplace]` sets only the catalog name, `[plugin.codex] marketplace = true` enables the Codex catalog,
and both entries install the repository root (`"./"`).
Claude and Codex load the seven skills from root `skills/`,
the same tree Pi and OpenCode discover, so each skill is generated once.

Installing the root means each host's plugin cache also holds maintainer content
such as `evals/`, `docs/`, and `tools/`; the hosts load none of it.
They do load default component paths, so `make check` fails when the root gains one
(for example `.mcp.json`, `hooks/`, `agents/`, `commands/`, `bin/`, or `settings.json`).
Claude also runs a best-effort npm install for root `package.json`;
it adds only the ai-rulez wrapper, and installation succeeds without npm or network.
See [the single-plugin evidence](../evals/results/automation/single-plugin/README.md).

Only ai-rulez native JSON output is promoted into the checkout.
Distributed skill content comes from our resource builder,
so tool provenance headers do not enter procedures or artifact templates.
ai-rulez's provenance sidecars stay with the exact staging outputs they describe;
they do not attest the independently materialized plain skill payload.

`make check-all` reconstructs expected packaging and compares it without repairing the checkout.
It detects changed, missing, extra, and symlinked files in both generated skill trees,
as well as drift in native JSON and npm identity fields.
Explicit synchronization replaces both fully owned trees,
so deleting a canonical skill removes its generated copies.
Source files and maintainer governance stay outside this replacement boundary.

## Host and release boundaries

Pi's root manifest and OpenCode's native skill path discover generated root `skills/`.
Every root skill contains its own references and templates;
no root-level shared resource directory is needed for installation.
The npm file allowlist includes only `skills/` and `README.md`;
npm also includes the package manifest.

Only Claude and Codex plugin runtimes are enabled.
OpenCode JavaScript plugin generation remains outside the Pi package tree;
new host runtimes require native validation before support is advertised.

Release-please bumps `package.json` and its lockfile.
The release workflow runs synchronization and checks on the release PR,
then commits the generated output alongside that version bump.
Synchronization updates the TOML version mirror; no manual version edit is needed there.

See [the original integration evidence](../evals/results/automation/adoption/README.md)
and [the authoring migration evidence](../evals/results/automation/authoring/README.md).
