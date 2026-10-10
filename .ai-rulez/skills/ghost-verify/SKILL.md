---
name: ghost-verify
description: Build or run a conformance harness for a downstream ghost-library implementation, accounting for every required case and proving the harness detects failures. Use for implementation verification rather than fixture authoring.
---

# Verify an implementation

Read [harness rules](../../references/harness-contract.md) and the applicable [fixture profiles](../../references/fixture-profiles.md).

## Work

1. Establish the pinned contract source, requested domains, downstream implementation path, language/API mapping, and execution scope. Read relevant specs, conventions, fixtures, and generation instructions. If no implementation exists, report the missing target or generate one only when that is included in the user's request.
2. Inventory case records independently of runner discovery. Identify required comparison, null/error mapping, named helpers, scenarios, environment injection, and invariant semantics. Confirm that the harness implements each assertion it claims to execute.
3. Run an existing harness, or build one in the downstream/disposable workspace when requested. Keep original contract fixtures unchanged. Isolate ambient inputs and side effects according to the profile. Record exact commands and source identity. Count execution only from completed tool results or saved runner evidence; identify blocked or planned checks separately.
4. Exercise applicable negative controls in a disposable copy: a wrong expectation, an incorrect return, and a required error that returns normally. Select controls that test different paths. A newly built or modified harness needs this proof; previously validated unchanged harness evidence can be reused when its source/profile identity still matches.
5. Produce case-level results and totals with skipped and unsupported cases visible. Diagnose failures as implementation, harness, contract, or environment problems; do not rewrite the contract to force success. Repair the implementation only if requested.

## Output and completion

Use [the conformance report](../../templates/reports/conformance.md). Include discovered and executed case counts, assertion results, unsupported fields, skip reasons, environment, commands, and negative-control evidence. Make claims only for the tested revision, domain, language, and environment.

Full conformance requires all required cases and assertions to execute and pass, with no skipped or unsupported requirements and a trustworthy harness. Report incomplete verification when execution or evidence is missing; report failing conformance when implemented assertions fail. Passing finite fixtures does not prove all possible inputs correct.
