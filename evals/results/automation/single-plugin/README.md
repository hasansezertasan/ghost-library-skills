# Single-plugin catalogs

Evaluated on 2026-10-11 with ai-rulez 5.0.0.
Both catalogs now install the repository root (`"./"`) as one plugin;
the generated `plugins/ghost-library-skills/` member and its duplicate skill tree are gone.
This supersedes the member layout recorded in [the authoring migration](../authoring/README.md);
that historical evidence remains unchanged.

## Layout

`[marketplace]` in `.ai-rulez/config.toml` sets only the catalog name, so it stays `ghost-library-skills-marketplace`
and install commands are unchanged.
`[plugin.codex] marketplace = true` enables the Codex catalog.
Claude, Codex, Pi, and OpenCode all load the seven skills from root `skills/`.
Disposable host bundles from `make build` use the same single-plugin shape.

## Evidence

| Check | Result |
| --- | --- |
| [Packaging and regression checks](checks.json) | 46 tests pass; four disposable host bundles contain seven skills each. |
| [Claude/Codex validation and discovery](validation.json) | Strict Claude manifest and catalog checks pass without warnings; Codex registers and discovers all seven skills. |
| [Four-host installation and replacement](installation.json) | Installation from a checkout copy, replacement, stale-file removal, active payload hashes, and resource links pass for Claude, Codex, Pi, and OpenCode. |
| Real configuration guard | No guarded files or Claude keys changed. |
| [Pi npm package](checks.json) | 93 files; only `README.md`, `package.json`, and `skills/`. |
| [Install experiments](experiments.json) | GitHub-sourced `./` installs work on Claude and Codex; marketplace naming, Claude's dependency step, and footprint are recorded. |
| Workflow validation | actionlint 1.7.12 passes check and release workflows. |

## Trade-offs

Each host's plugin cache now holds the whole repository, including maintainer content
such as `evals/`, `docs/`, and `tools/`; Codex also copies `.git/`.
A GitHub install grows from about 3.2 MB to 4.2 MB on Claude and 4.7 MB on Codex.
The hosts load only `skills/` and the manifests.
`make check` fails if the root gains a path Claude or Codex loads by default,
so maintainer tooling cannot become plugin content unnoticed.

Claude runs a best-effort npm install for root `package.json`.
It adds only the ai-rulez wrapper and never blocks installation;
without npm or network access it is skipped.

Private profiles and the network-disabled Codex container were used;
no authenticated model inference was requested.
The temporary container and GitHub branch were removed.
Remote release installation and GitHub workflow execution remain untested.
No new Hermes, Antigravity, or model-workflow support claim follows from these checks.

See [the integration guide](../../../../docs/ai-rulez.md) for generation and ownership details.
