---
name: ghost-release
description: Prepare a ghost-library contract release by comparing behavior, assessing compatibility, reconciling documentation, and assembling migration and conformance evidence. Use for release preparation; publishing requires explicit authorization.
---

# Prepare a contract release

Read [compatibility](../../references/compatibility.md) and [contract rules](../../references/contract-rules.md). Read [harness rules](../../references/harness-contract.md) when presenting implementation conformance evidence.

## Work

1. Establish the requested release scope and base/target revisions. Read existing versioning and release conventions. Keep plugin versions, library contract versions, fixture-format versions, and source commits distinct.
2. Compare behavioral rules, API shape, accepted inputs, defaults, output/error semantics, comparison policy, dependencies, and fixture requirements. Separate documentation corrections, coverage of existing rules, newly constrained behavior, and explicit behavioral changes.
3. Recommend a version using the library's policy. Explain the impact on previously conforming implementations; a corrected fixture or narrowed ambiguity may require migration even when described as a bug fix. Do not treat prose-only diffs as proof of compatibility.
4. Reconcile version references, examples, artifact links, installation guidance, and counts. Summarize relevant verification by source revision, domain, language, environment, and harness identity. Missing evaluation limits the claims; it must not be replaced with “all languages supported.”
5. Prepare changelog and migration notes with before/after examples where behavior changes. Identify unresolved contradictions and missing evidence affecting the proposed release. Use [the release report](../../templates/reports/release.md).

## Output and completion

Deliver a reviewable release patch or report with the proposed version, behavioral diff, migration steps, evidence, and outstanding requirements. Release preparation does not grant permission to push, tag, publish, or contact others. If the user already authorized publication, follow the repository's release process within that scope.

Complete preparation when changes and compatibility claims are supported and remaining limitations are explicit. Do not describe an unverified draft as a verified release.
