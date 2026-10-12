# Contributing

Read [AGENTS.md](AGENTS.md) for source ownership. The [maintainer guide](docs/maintainers.md) explains how to use the ghost-library lifecycle skills; this file explains how to change and release the plugin itself.

## Development

Python tooling uses only the standard library.
Use Python 3.12 or newer,
or install the interpreter selected by `.python-version` with `uv python install`.
Packaging also requires Node and npm;
CI selects Node from `.node-version`.
The Makefile installs ai-rulez from the root npm lockfile with development dependencies and install scripts disabled.
Its pinned platform binary downloads on first invocation.

```sh
make sync
make check-all
```

With uv, use `make check-all PYTHON="uv run --no-project python"`.
`make sync` reads `.ai-rulez/` sources and regenerates root skills, host manifests,
the identity and Pi fields in `package.json`, and the tracked payload using [the ai-rulez integration](docs/ai-rulez.md).
`make check-all` reports drift without repairing packaging,
validates local resource links, runs tests, and builds all four host bundles into a temporary directory.
It may install locked development tooling into `node_modules/`;
it does not install packages into your agents or run a model.

Keep canonical edits and their generated output together. Use `make build OUTPUT=dist/my-bundle` for an inspectable bundle; choose an absent or empty destination. Consult [host support](docs/host-support.md) for native installation and model evaluation evidence before changing host integration.

## Commit and PR titles

Use `<type>(optional-scope): <description>` for PR titles, because squash-merged titles determine releases. `feat:` adds functionality, `fix:` repairs behavior, and `perf:` improves performance. `docs:`, `test:`, `chore:`, `ci:`, and `build:` alone do not normally trigger a release. Mark a breaking change with `!` or a `BREAKING CHANGE:` footer.

Before 1.0, breaking changes bump the minor version; ordinary features also bump minor, and fixes bump patch. The first release is explicitly configured as `0.1.0`. The empty release manifest means no release has been recorded yet; release-please fills it when preparing the first release PR. The initial-version setting applies only before a first release, so it need not be removed after release.

## Release flow

1. On `main`, the release workflow runs the same checks and disposable build as CI.
2. Release-please creates or updates a PR containing the version bump and changelog. Automation regenerates and validates host packaging on that PR branch, then commits generated changes. Regeneration repeats whenever release-please rewrites its branch.
3. Review the complete PR, including generated changes. Merge it only after checks pass. The next release workflow validates that exact merge commit before creating its `vX.Y.Z` tag and GitHub Release.

The artifact is the tagged repository tree. These workflows do not publish to npm or create release attachments. `package.json` remains an installable Pi package; release-please's Node strategy updates its version without requiring JavaScript runtime code or npm publication.

## Repository setup

Enable GitHub Actions and allow Actions to create pull requests in repository settings. The release job needs contents, issues, and pull-request write permissions; validation jobs need only contents read. Action revisions are pinned in the workflows. No additional credential is required for the default flow.

GitHub's built-in `GITHUB_TOKEN` does not trigger ordinary PR workflows for the release PR it creates. The release workflow validates that branch explicitly before committing packaging. To obtain a check on the final PR head, manually run the `check` workflow **on the release PR branch**, keeping its optional `ref` input empty. For example:

```sh
gh workflow run check.yml --ref release-please--branches--main
```

Use the actual branch shown on the release PR if its name differs. Running on `main` with an input ref validates the requested tree but attaches the workflow run to `main`; it is useful for investigation, not a substitute for a required PR-head check. If release branches are rewritten, rerun the check on the new head. A scoped GitHub App token can instead enable automatic PR workflows; configure one deliberately if desired, rather than assuming approval starts a suppressed workflow.

For branch protection, require `validate` from the `check` workflow and permit the release PR to be merged only with that final-head check. These settings must be configured on GitHub; adding workflow files does not change repository settings.

## Recovery

If validation of a release merge fails transiently, rerun that merge commit's failed workflow. If a queued release run was superseded, rerun the original merge's workflow. A new green push or a manual release run on a later commit does not authorize releasing the older pending merge.

If the release tree has a real defect, repair it and validate the corrected tree. Close the old pending release out of the automatic queue and prepare a replacement release PR for the corrected commit; review version/changelog changes together. Do not simply relabel the failed merge to trigger release creation. More than one merged PR labelled `autorelease: pending` blocks automated release creation until the queue is reconciled.

If tagging succeeds but GitHub Release creation fails, rerun the original release merge's workflow and inspect the existing tag/release state. Do not move an existing release tag to a different tree. Record any manual reconciliation in the release PR so the manifest, changelog, tag, and release agree.
