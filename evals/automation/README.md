# Automation evaluations

These optional checks exercise raw ai-rulez output and release-please's release strategy without writing to GitHub or invoking a model.
They are separate from regular packaging CI,
which now uses [the staged ai-rulez integration](../../docs/ai-rulez.md).

The private tooling package pins ai-rulez `4.24.2` and release-please `17.6.0` with an npm lockfile. The latter matches the dependency locked by the selected release-please action `v5.0.0`; it is not a claim about the latest upstream version. These evaluation dependencies do not change the root Pi package.

## Reproduce

Install only into this evaluation directory:

```sh
npm ci --prefix evals/automation --include=dev --ignore-scripts
```

The ai-rulez launcher downloads its pinned platform binary on first use. From the repository root, choose an absent output directory outside the repository:

```sh
python3 evals/automation/run.py \
  --ai-rulez evals/automation/node_modules/.bin/ai-rulez \
  --output /tmp/ghost-ai-rulez-evaluation
node evals/automation/release-check.cjs evals/automation/node_modules/release-please
```

Add `--native` to the Python command when Claude and Codex are installed. This adds native Claude validation in a temporary configuration directory and Codex manifest reading through a private app-server process; it does not install plugins or invoke a model. Codex receives a temporary, hand-authored catalog because ai-rulez does not emit one for the tested single-plugin configuration.

The ai-rulez runner tests all seven current skills, including reference and template links, with three configurations: canonical `.ai-rulez/skills`, `plugin.content_root`, and OpenCode generation. It records verification after modifying generated content, adding an unexpected file, bumping the version, and removing a source skill. Negative results are evidence for the migration decision, not a failed repository CI check.

The release check uses release-please's real parser and strategy factory with a local mock for its GitHub file reads. It verifies first-release, patch, feature, and breaking-change versions, changelog updates, and preservation of all other package fields. It creates no PR, tag, release, or npm publication.

See the [saved results and decision](../results/automation/README.md). Reproduction uses current canonical files; the saved results describe the reviewed revision, configuration, and tool versions.
