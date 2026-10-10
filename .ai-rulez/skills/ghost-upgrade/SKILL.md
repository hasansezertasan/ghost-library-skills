---
name: ghost-upgrade
description: Upgrade a downstream ghost-library implementation from its pinned contract revision to a newer one while preserving local extensions, then re-verify and update the receipt. Use for consumer-side migrations, not for preparing a contract release.
---

# Upgrade a downstream implementation

Read [compatibility](../../references/compatibility.md), [harness rules](../../references/harness-contract.md), and the applicable [fixture profiles](../../references/fixture-profiles.md).

## Work

1. Establish the downstream implementation, its receipt or other record of the pinned source revision, the target revision, and selected domains. If the pinned revision is unknown, reconstruct it from hashes or history where possible and report the uncertainty; do not assume the implementation matches any revision.
2. Compare the contract between the two revisions: spec rules, fixtures, conventions, comparison policy, dependency policy, and generation instructions. Use release notes as a guide, but read the actual diff. Classify each change as in or out of the selected scope and whether it affects this implementation.
3. Identify local extensions from the receipt and code. Check whether each upstream change interacts with them. An upstream rule that now conflicts with a local extension needs a consumer decision; do not silently drop either.
4. Plan a targeted migration with [the upgrade template](../../templates/reports/upgrade.md). Prefer minimal changes to the existing implementation over full regeneration unless the user asks for regeneration or the diff makes it simpler. Update the harness for new fixture fields or profiles.
5. Apply the authorized migration, then verify against the target revision with complete accounting. Re-run negative controls when the harness changed. Update the receipt with the new revision, hashes, and verification result.

## Output and completion

Deliver the migration patch, updated harness and receipt, upgrade report, and conformance report for the target revision.

Complete when the implementation conforms to the target revision within scope, local extensions are preserved or explicitly resolved, and the receipt is current. A failure that traces to the new contract is reported with evidence for `ghost-fix`; do not pin a fixture or revert upstream behavior to make the upgrade pass.
