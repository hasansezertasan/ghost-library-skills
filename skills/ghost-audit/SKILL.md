---
name: ghost-audit
description: Audit a ghost library's specifications, portable fixtures, and generation instructions for contradictions, coverage gaps, portability issues, and documentation drift. Use for contract review, not a general source-code review.
---

# Audit a ghost library

Produce evidence a maintainer can act on without silently changing the contract. An audit is read-only unless the user also requests repairs.

Read [contract rules](references/contract-rules.md). Read [fixture profiles](references/fixture-profiles.md) for the formats actually present; consult [harness rules](references/harness-contract.md) only when runner behavior or conformance claims are in scope.

## Review

1. Establish the target path, requested domains, source revision when available, and scope. Read its own agent instructions, conventions, spec, fixtures, installation prompt, and relevant README sections. For a multi-domain repository, apply shared conventions to selected domains; do not imply every domain was reviewed.
2. Reconcile the public API, examples, errors, defaults, scope exclusions, dependency policy, version statements, artifact links, and claimed case counts. Parse fixture records using their declared profile; a recursive count of every YAML list will count argument arrays as tests.
3. Trace observable rules to cases. Distinguish an absent case, an ambiguous rule, a contradiction, and explicitly permitted variation. Check Unicode units, numeric representations, missing/null/empty values, ordering, truthiness, clock/environment inputs, and comparison policy where they affect this library.
4. Review fixture and harness meaning separately. A fixture in a prose scenario is not evidence of an executable setup. Inspect whether required errors, scenarios, invariants, and nested assertions can be executed and whether skips or unsupported assertions are exposed.
5. Report located findings with a concrete example, impact, evidence, and smallest useful next action. Label uncertain findings as questions and name what evidence would resolve them. Do not import a reference library's behavior as an unstated requirement.

## Output and completion

Use [the audit report template](templates/reports/audit.md) when a saved report is requested; a concise response with the same evidence is sufficient otherwise. Prioritize findings affecting behavior or false conformance claims. Include reviewed scope, checks performed, and limitations even when no findings remain.

The audit is complete when findings are traceable to source locations and coverage gaps are explicit. Do not certify generated code from specification review or fixture parsing. When repairs are requested, separate mechanical documentation corrections from decisions that change behavior; only the ambiguous decisions need clarification.
