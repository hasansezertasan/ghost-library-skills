# Repository packaging evaluation

On 2026-10-05, installation and version replacement directly from a disposable copy of the repository passed for Claude Code 2.1.289, Codex CLI 0.160.0, Pi 1.0.1, and OpenCode 1.18.34. No distribution build was required before installation. The [installation report](installation.json) records actual commands, selected versions, native inventories, active payload hashes, and shared-resource hashes.

The synthetic old distribution was version `0.0.0`, with a marker in `ghost-audit/SKILL.md` and an old-only resource. The source checkout was then replaced with the current `0.1.0` distribution. Fresh processes selected seven skills on every host; both old markers disappeared. Claude and Codex explicitly selected the new version. Native-selected skill files matched their respective current layouts, and all local skill/resource links resolved.

Claude and Pi use canonical root skills with shared `references/` and `templates/`. OpenCode uses those canonical skills through the root `opencode.json`. Codex installs the generated self-contained payload under `plugins/ghost-library/`; its link rewrites and bundled resources are checked separately. These layouts share canonical instructions but need not have byte-identical Markdown paths.

## Native metadata and OpenCode path behavior

[Root metadata validation](validation.json) passed both Claude strict checks without warnings; Codex parsed the root catalog and registered/discovered seven namespaced skills.

The [OpenCode path checks](opencode-paths.json) exercise three cases in private configuration/data/cache/state directories:

- `./skills` with the checkout as working directory: seven skills discovered.
- The same config selected through `OPENCODE_CONFIG` from a consumer directory: zero ghost skills discovered.
- An absolute skill path in the consumer config: seven skills discovered.

This establishes a working-directory dependency for relative paths on the tested version. Consumer instructions use absolute paths accordingly.

## Configuration guard

The final run preserved all watched configuration values and plugin registries. Claude's `.claude.json` is compared as normalized JSON excluding `cachedGrowthBookFeaturesAt` and `pluginUsage`; other watched files use byte SHA-256. The exclusions are a cache timestamp and usage telemetry that changed during a separate idle observation with no test commands running. All other keys remain guarded; a unit test verifies that preference changes are detected.

The [guard diagnosis](guard-diagnosis.json) records the preliminary raw-hash failure and the independent observation. Per-command change records and the final guard policy are explicit in the installation report. This is a scoped configuration check, not an exhaustive filesystem comparison. Claude manifest validation also now uses a disposable profile.

## Scope and reproduction

Claude uses `CLAUDE_CONFIG_DIR`; Pi uses `PI_CODING_AGENT_DIR` with extensions disabled. Codex runs without network in an Alpine container with only the evaluation directory mounted. The container is removed after the test. Real configuration and credentials are never mounted into it. Claude's startup probe strips authentication variables and requires missing-authentication failure; the other checks do not request model inference.

Use the [host-support reproduction commands](../../../../docs/host-support.md#reproduce-native-checks). Both smoke tools accept `--repository PATH` and retain `--bundle PATH` for the earlier disposable bundle layout.

These results cover local checkout installation, synthetic local version replacement, native discovery, and resource loading. The migrated layout is not yet published to GitHub. Remote Git-source installation, npm/Git upgrades, marketplace-name migration from an existing real installation, desktop applications, and OpenCode/Pi model workflows remain untested. Claude's authenticated workflow suite remains quota-blocked as recorded in the [earlier retry](../installation/claude-retry.json).
