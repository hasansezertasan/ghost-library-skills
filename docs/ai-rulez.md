# ai-rulez authoring and generation

Author plugin configuration and content in the committed `.ai-rulez/` tree.
The pinned npm development dependency generates the skills, Claude/Codex manifests and both catalogs in place;
`npm run generate` runs it, and `npm run check` also verifies that the generated skill tree holds nothing it did not record.

## Sources and ownership

| Content | Authored source |
| --- | --- |
| Procedures and Codex skill display metadata | `.ai-rulez/skills/ghost-*/` |
| Shared guidance | `.ai-rulez/references/` |
| Artifact templates | `.ai-rulez/templates/` |
| Plugin identity, runtime selection, and interface | `.ai-rulez/config.toml` |
| Release version and npm tooling | `package.json` |
| Maintainer governance | `AGENTS.md`, `CONTRIBUTING.md`, and `docs/` |

`package.json` is the sole plugin version source:
`[plugin] version_from = "package.json"` reads it, so the TOML carries no version.
The TOML `version = "5.0"` is the configuration schema version, not the plugin release version.
`package.json` is authored (the template's scaffold plus this repo's version); ai-rulez does not write it.
Its identity fields, `pi.skills` (`["./skills"]`) and `devDependencies` are edited there by hand,
and the plugin identity in `.ai-rulez/config.toml` must stay consistent with them.
The npm name is `ghost-library-skills`; the repo is private and not published.

`[plugin] shared_resources` copies `.ai-rulez/references/` and `.ai-rulez/templates/` into every skill
and rewrites their `../../` links to the copies,
so each generated skill can be moved independently, including its `agents/openai.yaml` metadata.
`content_root = ".ai-rulez"` is what bundles that metadata:
each skill directory is copied whole.
ai-rulez still warns that it will not include the `agents` subdirectory; the warning is wrong for this layout.

Root `skills/`, `.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/marketplace.json`,
and `.ai-rulez-generated.json` are generated distribution surfaces.
Keep them in version control so consumers need no generator installation.
Edit their sources and regenerate instead of editing generated content directly.

## Generation and verification

```sh
npm run generate
npm run check
```

Use these npm scripts rather than running ai-rulez directly.
They run the locked development tool in the checkout:
`npm run generate` runs `generate` and `generate --plugin`, and `npm run check` runs the drift gate, `verify --plugin` and `validate --strict`.
Python tooling uses the standard library;
CI interpreter versions are selected by `.python-version` and `.node-version`.

ai-rulez generates both catalogs in single-plugin mode:
`[marketplace]` sets only the catalog name, `[plugin.codex] marketplace = true` enables the Codex catalog,
and both entries install the repository root (`"./"`).
Claude, Codex, and Pi (`pi.skills` in the authored `package.json`) load the generated skills from root `skills/`,
the same tree OpenCode discovers, so each skill is generated once.

Installing the root means each host's plugin cache also holds maintainer content
such as `evals/`, `docs/`, and `tools/`; the hosts load none of it.
They do load default component paths, so `npm run check` fails when the root gains one
(for example `.mcp.json`, `hooks/`, `agents/`, `commands/`, `bin/`, or `settings.json`).
ai-rulez reports each as `AR9T0 root-component-shipped`, but that rule is off in `.ai-rulez/config.toml`
because it also flags the Antigravity `plugin.json` adapter, so `tools/check_owned_tree.py` guards these paths instead.
Claude also runs a best-effort npm install for root `package.json`;
it adds only the ai-rulez wrapper, and installation succeeds without npm or network.
See [the single-plugin evidence](../evals/results/automation/single-plugin/README.md).

`[plugin] provenance_headers = false` keeps generated files byte-identical to their sources,
so no tool provenance header enters procedures or artifact templates.
`.ai-rulez-generated.json` records every generated file and its content hash instead.

`npm run check` compares the checkout against that record without repairing it.
`verify --plugin` reports changed and missing files and drift in the manifests and the owned `package.json` keys;
it reports that output is stale but does not name the file.
It accepts files it did not record and symlinks with recorded content,
so `tools/check_owned_tree.py` reports any unrecorded file or symlink under `skills/` as well.
Explicit synchronization regenerates the tree and deletes unrecorded files,
so deleting a canonical skill removes its generated copy.
Source files and maintainer governance stay outside this replacement boundary.

## Host and release boundaries

Pi's `package.json` points at the generated root `skills/` directory, and OpenCode's native skill path discovers the same tree.
Every root skill contains its own references and templates;
no root-level shared resource directory is needed for installation.
The package is private, so it carries no npm file allowlist.

Only the Claude and Codex plugin runtimes are generated; Pi reads `package.json` and `skills/` directly.
OpenCode JavaScript plugin generation remains outside the package tree;
new host runtimes require native validation before support is advertised.
The Antigravity root `plugin.json` is a small hand-authored adapter because ai-rulez
does not generate that install surface; Antigravity installs the repository root
straight from the Git URL and discovers the same generated `skills/` tree.

Release-please bumps `package.json` and its lockfile.
The release workflow runs synchronization and checks on the release PR,
then commits the generated output alongside that version bump.

See [the in-place generation evidence](../evals/results/automation/in-place/README.md),
[the original integration evidence](../evals/results/automation/adoption/README.md),
and [the authoring migration evidence](../evals/results/automation/authoring/README.md).
