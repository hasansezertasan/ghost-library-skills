# 0002: Adopt the copier-skill-repo template

Status: accepted. Date: 2026-10-17.

This repo's scaffold now comes from the
[`copier-skill-repo`](https://github.com/hasansezertasan/copier-skill-repo) template (v0.3.0)
and is updated with `copier update`. The skills, `README.md` (apart from its
validate commands) and `CHANGELOG.md` were not touched. This record lists what
still differs from a plain render and why; it is not updated as the project evolves.

## Replaced by the template's version

- **Task runner.** The Makefile is gone. `npm run generate` and `npm run check`
  replace `make sync` and `make check`; `npm test` and `npm run build` replace
  `make test` and `make build`. The README, `AGENTS.md`, `CONTRIBUTING.md`,
  `docs/ai-rulez.md`, `docs/host-support.md` and `docs/install-codex.md` were
  updated to the new commands. Records under `evals/` and the two `*-proposal.md`
  documents still say `make`; they describe what was true when they were written.
- **Packaging wrapper.** `tools/sync_packaging.py` and its tests are replaced by
  `ai-rulez generate`/`verify`/`validate` behind `npm run check`. ai-rulez moved
  from 5.0.4 to the template's 5.3.0 pin, which supersedes the unmerged
  `chore/adopt-ai-rulez-5-1-0` branch.
- **Release guard.** `tools/release_guard.py` and its test are replaced by the
  template's `scripts/release-guard.mjs` and `scripts/release-merge.mjs`.
- **Release configuration.** `.config/release-please-config.json` and
  `.config/release-please-manifest.json` moved to the repo root, as the template
  places them. The manifest keeps the released `0.1.0`.
- **CI and release workflows, Renovate config, `.node-version`,
  `scripts/check-repo.mjs`.** Taken as rendered. The old `check` workflow's
  `ref` input for validating a release PR branch is gone: the template's release
  workflow regenerates the plugin output on that branch itself and hands over a patch.
- **Required check name.** The check job is now `check`, not `validate`. Branch
  protection on `main` must require `check`; that setting lives on GitHub, so
  this change does not make that edit.
- **Antigravity adapter.** The root `plugin.json` is hand-authored, as before, but
  `scripts/check-repo.mjs` now keeps it equal to the Claude manifest instead of
  `sync_packaging.py` writing it. The template's `AR9T0` opt-out for it is in
  `.ai-rulez/config.toml`.

## Differences kept on purpose

- **Python tooling.** `tools/build_skills.py`, `build_plugins.py`, `smoke_*.py`,
  `run_workflow_evals.py` and the unit tests stay. `check.yml` has extra steps for
  them after the template's `npm run check`: `build_skills.py --check`,
  `npm test` and a disposable `npm run build`. The npm scripts run Python as
  `${PYTHON:-python3}`, and CI sets `PYTHON` to `uv run --no-project python` so it
  uses the `.python-version` interpreter, not the runner's. The builders no
  longer call `sync_packaging`; staleness is `npm run check`'s job.
- **`tools/check_owned_tree.py`.** The strict check that `skills/` holds no symlink
  and no file ai-rulez did not record (ai-rulez accepts both) moved here from the
  old wrapper, with tests. It runs as the `postcheck` script, so `npm run check`
  (local, CI and the release workflow) includes it without editing the
  template-owned `check` line; `build_plugins.py` applies it too.
- **`AR9T0` is off, so the root-component guard moved.** The template turns the
  rule off because it also flags the Antigravity `plugin.json` adapter, but it
  is the rule that rejects `.mcp.json`, `hooks/` and the other host-loaded root
  paths. `tools/check_owned_tree.py` now rejects those paths itself, with a test.
- **`.ai-rulez/config.toml`.** `shared_resources = ["references", "templates"]`, the
  interface text and the default prompt stay. The `pi` runtime and `[plugin.pi]`
  (`package_json = "merge"`) stay, now as the template ships them: ai-rulez derives
  `pi.skills` (one entry per skill), the `pi-package` keyword and the `files`
  allowlist in `package.json` from the skills on disk.
- **Marketplace name.** Stays `ghost-library-skills-marketplace`, because it is part
  of the install commands in `docs/installation.md` and the host guides. The
  template would name it after the repo.
- **`docs/installation.md`.** Kept as the repo's own page, which links the per-host
  guides and uses that marketplace name. It is template-owned, so `copier update`
  will propose changes to it; resolve them by hand.
- **`CONTRIBUTING.md`.** The template's version plus a "Ghost Library Skills
  development" section, and one changed line: `AGENTS.md` is authored here, not
  generated, so it is not in the never-edit list.
- **`.gitignore`.** The template's `node_modules/` plus `dist/`, `__pycache__/`,
  `*.pyc` and `.ai-rulez/.generated-manifest.local.json`.
- **`publish_to_npm: false`.** The package is `"private": true`, as the repo never
  published to npm.
- **`.copier-answers.yml`.** `keywords` includes `pi-package`, so the generated
  manifests keep that keyword. `placeholder_skill: hello` stays but no placeholder
  skill exists here.

## Changes to review

- **Pi package name.** The merged Pi `package.json` was named
  `@hasansezertasan/pi-ghost-library-skills`; it is now `ghost-library-skills`.
  Pi installs from a path or git URL, so installs are unaffected, but the name
  differs from before.
- **`package.json` fields.** `license` is now `MIT` (the template requires one). The
  `files` allowlist stays, generated by ai-rulez. The repo had no
  `LICENSE` file, so one was added with the standard MIT text, copied from
  scoop-bucket-skills, so the declaration has terms behind it.
- **Evaluation scripts.** `evals/automation/run.py` read the manifests through
  `tools/sync_packaging`, and `release-check.cjs` read
  `.config/release-please-config.json`. Both now read the committed catalog and the
  root `release-please-config.json` (with package-level settings falling back to
  the top level), and both documented commands still run.
- **Version-bump test.** `tests/test_build_plugins.py` hard-codes version `0.1.0`
  and will need updating at the next release.
