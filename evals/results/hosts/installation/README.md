# Private-profile installation and replacement

On 2026-10-05, native checks passed for Claude Code 2.1.289, Codex CLI 0.160.0, OpenCode 1.18.34, and Pi 1.0.1. The [report](report.json) records the actual commands, selected versions, skill inventories, complete active payload hashes, and resource-link checks.

The test installed a synthetic old bundle carrying `OLD_RELEASE_ONLY` in `ghost-audit/SKILL.md` and an extra resource file. It then replaced the source with the current `0.1.0` bundle and used each host's update or reload mechanism. Fresh processes discovered exactly seven skills. The old marker and extra resource were absent from every active payload; every active skill file, reference, template, and display metadata file matched the current bundle. Older versioned caches may remain on disk; the check concerns the version actively selected by discovery.

| Host | Isolation | Replacement exercised |
| --- | --- | --- |
| Claude | Disposable `CLAUDE_CONFIG_DIR`; no credentials copied | Local marketplace update, plugin update, fresh startup |
| Codex | Network-disabled Alpine container; only the disposable evaluation directory mounted | Repeat local `plugin add`, fresh app-server, installed cache export |
| OpenCode | Disposable config/data/cache/state directories; external skill discovery disabled | Complete skill-directory replacement, fresh native `debug skill --pure` |
| Pi | Disposable `PI_CODING_AGENT_DIR`; offline mode; extensions disabled | Local package source replacement, `pi update`, fresh installed native resource loader |

All watched real-profile configuration hashes remained unchanged during the isolated run. The [preliminary combined run](preliminary-run.json) failed this guard while an authenticated model trial was running concurrently; it did not retain enough information to attribute that change. The isolated rerun avoided that overlap. The guard watches the configuration files enumerated in the script; it does not claim an exhaustive filesystem comparison.

## Invocation evidence and remaining limits

The [Codex audit](codex-invocation.json) completed using an exported copy of the installed `0.1.0` cache, host authentication, and process-local skill registration. Completed command receipts show that it read the packaged skill, contract rules, and fixture-profile reference. It identified the missing zero-error fixture and undefined numeric domain in the saved [specification](contract/SPEC.md) and [fixtures](contract/tests.yaml). Target files stayed unchanged. This proves invocation and resource reads for the installed payload, not authenticated inference inside the container.

The authenticated [Claude workflow retry](claude-retry.json) discovered all seven skills, then returned HTTP 429 with the weekly usage-limit message and a 1pm Istanbul reset. No model turn completed and the reported cost was zero. The disposable profile's startup check separately stopped for missing authentication. The six Claude workflow evaluations remain pending until quota is available; discovery and installation passes do not resolve that gap.

OpenCode and Pi checks exercise native discovery and resource loading without model inference. Their workflow behavior, npm/Git package upgrades, desktop hosts, and migration from existing real installations remain untested.

## Reproduce

Use [the host-support commands](../../../../docs/host-support.md#reproduce-native-checks) and `tools/smoke_installation.py`. Provide the official Codex Linux arm64 musl archive, the installed Pi resource-loader module, a built four-host bundle, and an absent output directory. The script leaves disposable profiles and evidence for inspection and removes its container. Run it separately from authenticated trials or other writers to watched configuration files.
