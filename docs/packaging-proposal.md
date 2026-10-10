# Packaging structure after reviewing Flow

The current [ai-rulez authoring structure](ai-rulez.md) supersedes the source layout and metadata ownership proposed below.
Canonical skills and shared resources now live under `.ai-rulez/`;
root `skills/` is a generated, self-contained installation surface.


The subsequent [ai-rulez integration](ai-rulez.md) changes native JSON generation and points both host catalogs at the self-contained `plugins/ghost-library` member.
The layout and original Flow reasoning below describe the earlier implementation.
Canonical root skills and Pi/OpenCode discovery paths are preserved.

Migration implemented locally. Native validation and installation evidence are linked in [host support](host-support.md). This document preserves the reasoning and intended boundaries. Reviewed on 2026-10-05 against `cofin/flow` at `164b07f42597aefce2dcf7268a66eaac27b19bb2`, shallow-cloned into `/private/var/folders/vj/26z0937x6zg3hvq02p8v6nfw0000gn/T/ghost-flow-research-amqbiij0/flow`.

## Migration decision

Replace the current `adapters/` source layout with native host discovery paths at the repository root. Keep the seven canonical skills and shared resources. Make the repository itself an installable distribution, while retaining standalone and disposable bundle builds for evaluation.

The previous layout worked for tested local bundles, but consumers had to run Python first. Native catalogs now live at the checkout root. Renaming `adapters/` alone would not have resolved that installation problem.

## What Flow does

- Claude's root [marketplace](https://github.com/cofin/flow/blob/164b07f42597aefce2dcf7268a66eaac27b19bb2/.claude-plugin/marketplace.json) points at `.`. Its root `.claude-plugin/plugin.json` installs the repository's canonical skills and other resources.
- Codex's root [marketplace](https://github.com/cofin/flow/blob/164b07f42597aefce2dcf7268a66eaac27b19bb2/.agents/plugins/marketplace.json) points at `./plugins/flow`. The [package synchronizer](https://github.com/cofin/flow/blob/164b07f42597aefce2dcf7268a66eaac27b19bb2/tools/sync-codex-package.py) materializes real files from canonical sources and has a non-mutating `--check` that detects missing, extra, changed, and symlinked files. The generated package is tracked in the inspected checkout.
- The [host contract](https://github.com/cofin/flow/blob/164b07f42597aefce2dcf7268a66eaac27b19bb2/contracts/flow.yaml) distinguishes host capabilities and invocation conventions. Procedures remain in canonical skills rather than being independently rewritten for every host.
- The [packaging guidance](https://github.com/cofin/flow/blob/164b07f42597aefce2dcf7268a66eaac27b19bb2/docs/multi-harness-plugin-patterns.md) favors native installation and separate checks for host contracts. Its Makefile aggregates validation and drift checks without repairing first.

One stale pre-commit comment says the Codex package is ignored and should never be staged, while `git ls-files plugins/flow` confirms it is tracked. Use the inspected manifests, generator, and tracked files as evidence for the layout.

## Implemented layout

```text
.claude-plugin/
  plugin.json                 # generated manifest
  marketplace.json            # Claude catalog; source: .
.codex-plugin/
  plugin.json                 # generated canonical Codex manifest
.agents/plugins/
  marketplace.json            # Codex catalog; source: ./plugins/ghost-library
package.json                  # identity/version and Pi skill-package declaration
skills/ghost-*/                # canonical procedures
references/                   # canonical shared resources
templates/                    # canonical artifact templates
plugins/ghost-library/        # generated, tracked Codex payload
  .codex-plugin/plugin.json
  skills/ghost-*/              # self-contained output from existing builder
tools/
  sync_packaging.py            # explicit generation and non-mutating --check
  build_skills.py              # standalone folder distribution
  build_plugins.py             # disposable multi-host evaluation bundles
  smoke_plugins.py
  smoke_installation.py
docs/
  host-support.md
evals/
tests/
Makefile                      # small sync, check, test, and build entry points
```

Use `package.json` as the shared identity/version source and expose canonical `skills/` through its explicit Pi manifest. Generate host manifests from selected shared metadata plus their required host fields. Ship `references/` and `templates/` with the root package so canonical relative links resolve. A future npm distribution should use an explicit file allowlist.

For OpenCode, retain native skill support and validate a supported configuration that points to canonical `skills/`; avoid inventing a JavaScript plugin just to distribute Markdown. The root `opencode.json` is validated by the native CLI. Relative paths resolve from its working directory; consumer projects must use an absolute skill path. Its disposable bundle can continue materializing `.opencode/skills/`. Flow's JavaScript entrypoint injects operational routing; that function is unnecessary for the current seven independent ghost workflows.

Add Antigravity or Hermes manifests only when their integration is implemented and validated. Flow does not supply evidence for our Pi package or those future hosts.

## Migration and checks

1. Establish root package metadata and generate the root Claude/Codex manifests and catalogs. Retire `adapters/` after builders consume the new sources.
2. Generate and track the Codex payload. Extend validation with a read-only drift check; rebuilding expected output in a temporary directory must not repair the checkout.
3. Retain the existing resource-link rewriting and standalone builder. Test root-package links separately from self-contained skill-folder links.
4. Update the private-profile tests to install from a copy of the repository root, rather than only `dist/` bundles. Verify initial installation, version replacement, fresh discovery, and active resource hashes again.
5. Document repository/Git-source installation as the primary Claude/Codex/Pi path after testing it. Keep build-first instructions for development and evaluation. Do not claim public installation of this migration before it is committed and available remotely.

A small host-support table is enough for now. Add a machine-readable host contract when command mappings or shared routing actually need generation. Hooks, subagents, state tracking, and mandatory routing are separate product decisions; this packaging change does not require them.
