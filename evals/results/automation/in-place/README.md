# In-place generation

Evaluated on 2026-10-12 with ai-rulez 5.0.4.
`make sync` now runs `ai-rulez generate --plugin` in the checkout;
the staging tree, our resource builder, and the TOML version mirror are gone.
This supersedes the generation boundary recorded in [the single-plugin evidence](../single-plugin/README.md);
its catalog layout is unchanged.

## Configuration

| Setting | Replaces |
| --- | --- |
| `version_from = "package.json"` | The regex-maintained `[plugin].version` mirror |
| `shared_resources = ["references", "templates"]` | Copying shared resources into each skill and rewriting their links |
| `provenance_headers = false` | Discarding ai-rulez's skill tree to keep headers out of procedures and templates |
| `content_root = ".ai-rulez"` | Bundling each skill's `agents/openai.yaml` |
| `[plugin.pi] skills_dir = "skills"`, `package_json = "merge"` | Hand-maintained identity and Pi fields in `package.json` |
| `validate --strict` (`AR9T0`) | Our list of host-loaded root paths |

With these settings ai-rulez reproduced the previous `skills/` tree and all four manifests byte for byte,
apart from one source fix: `ghost-catalog`'s description contained `: ` unquoted,
which is invalid YAML and which ai-rulez rejects.

Enabling the Pi runtime renames the npm package to `@hasansezertasan/pi-ghost-library-skills`
and lists each skill directory in `pi.skills` and each file in `files`.

## Evidence

| Check | Result |
| --- | --- |
| [Packaging and regression checks](checks.json) | 45 tests pass; four disposable host bundles contain twelve skills each; strict validation has no findings. |
| [Claude/Codex validation and discovery](validation.json) | Strict Claude manifest and catalog checks pass without warnings; Codex registers and discovers all twelve skills. |
| [Four-host installation and replacement](installation.json) | Installation from a checkout copy, replacement, stale-file removal, active payload hashes, and resource links pass for Claude, Codex, Pi, and OpenCode. |
| Real configuration guard | No guarded files or Claude keys changed. |
| [Pi npm package](checks.json) | 218 entries; only `README.md`, `package.json`, and `skills/`. |
| [Drift probes](checks.json) | Each case our previous check covered is still reported; see the boundary below. |
| Workflow validation | actionlint 1.7.12 passes check and release workflows. |

## Boundary

`verify --plugin` reports changed and missing files, but says only that output is stale, without naming the file.
It accepts files it did not record and symlinks whose content matches,
so `tools/sync_packaging.py` still reports unrecorded files and symlinks under `skills/`,
and `make sync` deletes unrecorded files there.
Every run warns that the `agents` skill subdirectory will not be included, although it is.

Private profiles and the network-disabled Codex container were used;
no authenticated model inference was requested.
Remote release installation, npm publication under the new name, and GitHub workflow execution remain untested.
