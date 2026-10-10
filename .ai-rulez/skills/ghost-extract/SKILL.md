---
name: ghost-extract
description: Derive a ghost-library contract from an existing utility, package, or dependency by inventorying its observable behavior, choosing a compatibility scope, and preserving attribution. Use to replace or document existing code with a contract, not to design new behavior from an idea.
---

# Extract a contract from existing code

Read [philosophy](../../references/philosophy.md), [contract rules](../../references/contract-rules.md), and [fixture profiles](../../references/fixture-profiles.md).

## Work

1. Establish the source project, revision, license, the subset of the API to extract, and the target contract repository or domain. Confirm the license permits the intended reuse of documentation, examples, and test data; when it is unclear, report it and continue with behavior described in your own words. Retain required notices and attribution.
2. Inventory observable behavior from documentation, the source's tests, and the code. Where they disagree or are silent, observe actual behavior in an isolated environment with the source's own runtime, and record each observation's command and version. Do not run untrusted install scripts outside a disposable environment.
3. Choose a compatibility scope with the user: exact compatibility, compatibility for a named subset, or a cleaned-up contract that deliberately differs. Classify each behavior as required, permitted variation, or excluded. Runtime-specific quirks such as UTF-16 lengths, float formatting, or locale defaults are classified deliberately, not copied by default.
4. Write the spec and fixtures using the target's conventions or [the spec template](../../templates/spec.md), following the `ghost-spec` and `ghost-tests` workflows when available. Derive each expected value from the classified behavior; an observation of the source is evidence for a required behavior, not an oracle for excluded quirks.
5. Record the extraction with [the extraction template](../../templates/reports/extraction.md). When feasible, verify that the source itself passes the required fixtures, and report any required behavior it fails as a deliberate divergence.

## Output and completion

Deliver the contract draft, fixtures, attribution, extraction report, and open classification decisions. Keep any harness used to check the source outside the contract repository unless repository policy says otherwise.

Complete when every behavior in scope is classified, the fixtures express the required ones, and divergences from the source are explicit. A contract with unclassified behavior is a draft.
