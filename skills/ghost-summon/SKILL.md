---
name: ghost-summon
description: Generate a ghost-library implementation into a consumer project with an explicit language and API mapping, verify it against the pinned contract, and record a provenance receipt. Use when a consumer adopts a ghost library, not when changing the contract.
---

# Generate an implementation downstream

Read [contract rules](references/contract-rules.md), [harness rules](references/harness-contract.md), and the applicable [fixture profiles](references/fixture-profiles.md). Follow the library's own generation instructions when it has them; they take precedence over this procedure where they are more specific.

## Work

1. Establish the contract source and pin its revision, the selected domains or functions, the consumer project, target language/runtime, and output location. Read the consumer's conventions, existing code at that location, and dependency rules. Do not write into the contract repository unless the user explicitly asks.
2. Write the API mapping before generating code: idiomatic names and signatures, argument and option encoding, null versus missing, error representation, and any permitted variation chosen. Check the mapping against the contract's dependency policy and the consumer's. A mapping that cannot express a required behavior is a blocker to report, not a reason to drop the behavior.
3. Generate the implementation and a harness that inventories every selected fixture case. Keep contract fixtures unchanged. Reuse an existing consumer test runner when it can enforce the harness rules; do not install tools globally.
4. Verify by following the `ghost-verify` workflow when it is available, or its harness rules directly: run all selected cases, account for skipped and unsupported ones, and exercise negative controls for the newly built harness. Repair implementation failures downstream. A failure that traces to the contract is reported with evidence and left for `ghost-fix` or a maintainer decision.
5. Record a receipt with [the receipt template](templates/reports/receipt.md) in the consumer-selected location. Keep consumer-specific behavior as a named local extension, separate from upstream rules.

## Output and completion

Deliver the generated implementation, harness, API mapping, receipt, and a conformance report using [the conformance template](templates/reports/conformance.md). Report the decision for the selected scope only.

Complete when the selected cases pass with complete accounting and a proven harness, or when the remaining failures, unsupported assertions, and contract questions are explicit. A generated implementation without verification evidence is a draft, not an adoption.
