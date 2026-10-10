---
name: ghost-fix
description: Diagnose a downstream ghost-library failure and turn it into an implementation, harness, fixture, or specification repair with a portable regression where appropriate. Use for reported bugs, not broad audits.
---

# Repair a reported failure

Read [contract rules](references/contract-rules.md), [fixture profiles](references/fixture-profiles.md), and [compatibility](references/compatibility.md). Read [harness rules](references/harness-contract.md) if runner behavior is implicated.

## Work

1. Capture the reported input, expected and actual behavior, contract source revision (from the downstream receipt when one exists), implementation revision/language, relevant environment, and command. Minimize the reproduction while retaining the failure. Request missing evidence only when it prevents diagnosis; continue reading the contract and supplied artifacts.
2. Reproduce against the pinned contract. Identify the layer: implementation violates a clear rule; harness misreads or compares incorrectly; fixture contradicts independently justified behavior; spec is contradictory or incomplete; environment differs from required setup. Several layers may be involved. Do not classify every downstream failure as an upstream defect.
3. Add a regression before repair when executable artifacts are available. For a contract-only change, document the contradiction and expected fixture derivation instead of manufacturing a failing implementation test. Preserve required upstream behavior; add consumer-specific requirements to a clearly separated local extension.
4. Apply the authorized repair in the responsible repository. Implementation repairs belong downstream. Contract repairs update spec, fixtures, and instructions together as needed. A conflicting contract needs a deliberate behavior decision; do not choose whichever side lets the existing implementation pass.
5. Rerun the reproduction and affected checks. If the behavior is shared across languages, make the regression express the contract rather than one runtime's incidental formatting. Assess compatibility when a contract changes.

## Output and completion

Report cause, source identity, reproducer, regression, changed artifacts, and observed checks. If only upstream artifacts are available, deliver the contract regression and explicitly identify downstream verification still needed. Complete when the authorized repair resolves the reproduced issue with evidence, or clearly report the specific unresolved decision/environment dependency.
