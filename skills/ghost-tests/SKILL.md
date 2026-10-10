---
name: ghost-tests
description: Create or improve language-agnostic fixtures, scenarios, invariants, and rule-to-case coverage for a ghost library. Use when maintaining contract tests, not ordinary implementation unit tests.
---

# Write portable fixtures

Read [fixture profiles](references/fixture-profiles.md) and [contract rules](references/contract-rules.md). Read [harness rules](references/harness-contract.md) when adding a new assertion or scenario that changes runner responsibilities.

## Work

1. Read the requested spec/domain and its existing fixture conventions. Identify the actual case containers, argument encoding, expected-value fields, error semantics, comparison policy, and any named helpers. Keep this schema unless a migration is requested.
2. Map the relevant observable rules to current cases. Use [the coverage template](templates/reports/coverage.md) to record covered rules, proposed cases, and gaps. Choose cases that distinguish a plausible wrong implementation: boundaries, precedence, omitted versus explicit null, mutation, environment leakage, or ordering as applicable.
3. Derive expected results from the intended contract. Compute byte-exact hashes or conversions with an independently justified tool; record derivation where useful. Do not use the candidate implementation's output as its own oracle. If spec and fixtures disagree, report the conflict and resolve the intended behavior before changing that expectation.
4. Encode values as portable data. For callables, use named helpers with defined semantics. For stateful behavior, define setup, actions, observations, and cleanup. For nondeterminism, specify invariants, seeds, trial counts, thresholds, and the reproducibility scope. Do not substitute exact cross-language PRNG output for a contract that only promises local reproducibility.
5. Parse the changed fixture files, check unique case identifiers within their scope, and verify each assertion has defined runner semantics. Count case records rather than nested arrays. Unknown assertion fields need documented handling; they must not be silently ignored. If a runner exists and executing it is in scope, run affected cases and applicable harness checks. If it does not exist, report fixture validation and runner requirements explicitly.

## Output and completion

Deliver the fixture patch, derivation notes for computed expectations, and coverage map. Use existing case IDs or add stable names where the schema permits; otherwise identify cases by file/group/index and make the stability limitation clear.

Complete when requested rules have meaningful cases, fixture parsing succeeds, and new assertion semantics are implementable. Separate validation performed from implementation conformance. Never weaken required errors, omit unsupported cases from totals, or edit expectations merely to accommodate generated code.
