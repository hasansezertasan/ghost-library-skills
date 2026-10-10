# ai-rulez authoring migration

Evaluated on 2026-10-05 with ai-rulez 4.24.2.
Canonical procedures, shared resources, templates, and plugin configuration now live under `.ai-rulez/`.
This supersedes the [staging-only integration](../adoption/README.md);
its historical evidence remains unchanged.

## Ownership and naming

Author procedures in `.ai-rulez/skills/`, shared guidance in `.ai-rulez/references/`,
and artifact templates in `.ai-rulez/templates/`.
The committed TOML owns plugin identity, runtime selection, and interface options.
`package.json` remains the sole authored release version;
the required TOML plugin version is a generated mirror.
Root `skills/` and the shared Claude/Codex member contain independently portable skill folders.

The project, npm package, and plugin are named `ghost-library-skills`.
Both catalogs are named `ghost-library-skills-marketplace`
and reference `./plugins/ghost-library-skills`.
The seven workflow names remain unchanged.
Old-to-new plugin or marketplace identity migration in an existing real profile is not tested;
the private installation check tests replacement within the new identity.

## Evidence

| Check | Result |
| --- | --- |
| [Packaging and regression checks](checks.json) | 45 tests pass; four disposable host bundles contain seven skills each. |
| Native ai-rulez configuration | Valid; resource-kind warnings for source `agents/` metadata remain, which our builder preserves. |
| [Claude/Codex validation and discovery](validation.json) | Strict Claude manifest/catalog checks pass; Codex registers and discovers all seven renamed plugin skills. |
| [Four-host installation and replacement](installation.json) | All seven skills, active resource hashes, stale-file removal, and resource links pass before/after replacement. |
| Real configuration guard | No guarded files or Claude keys changed; the existing volatile-key exclusions remain unchanged. |
| [Pi npm package](pi-package.json) | 93 files; only skills with embedded resources, README, and package metadata are included. |
| [Release-please](release-please.json) | First release, patch, feature, and pre-1.0 breaking versions pass; npm fields and lockfile updates survive. |
| Workflow validation | actionlint 1.7.12 passes check and release workflows. |
| Raw prototype reproduction | All three configurations generate and build seven portable skills from the migrated sources. |

Regressions check root-skill drift without repair, TOML metadata propagation,
version-mirror correction, source preservation, and source deletion from both output trees.
Release automation stages the root skill output and TOML mirror alongside native packaging.
Both generated trees reject missing, changed, extra, and symlinked resources.

Native host versions are recorded in the reports.
Private profiles and the network-disabled Codex container were used;
no authenticated model inference was requested.
The temporary container was removed.
Full temporary data remains at `/tmp/ghost-authoring-checks.dHlxbD0i`.
Remote release installation and GitHub workflow execution remain untested.
No new Hermes, Antigravity, or model-workflow support claim follows from these checks.

See [the integration guide](../../../../docs/ai-rulez.md) for generation and ownership details.
