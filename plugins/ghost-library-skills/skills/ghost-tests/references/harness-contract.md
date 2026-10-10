# Harness contract

## Identity and execution

Record the contract source URL/path and commit or content hashes, selected domain, fixture identity/profile, implementation revision, harness revision or hash, language/runtime, relevant environment, and exact commands. When Git is unavailable, use content identity and state that limitation.

Inventory required cases independently of the runner's discovered set. Unknown groups, malformed records, unsupported assertions, and absent scenarios cannot disappear from a conformance report. Fixture parsing and case counting alone do not verify code.

Count a check as executed only after its completed tool result or saved runner evidence is available. A proposed command, predicted exit code, blocked tool call, or setup failure is not execution evidence. Keep planned, attempted, blocked, and observed checks distinct; do not fill missing results from source inspection.

Keep contract fixtures unchanged while repairing an implementation. Proposed fixture corrections need their own contract diff and justified expectations. Generated code and executable harnesses belong downstream or in a disposable workspace subject to target repository policy.

## Assertion policy

Implement the declared comparison and language mapping. Exact strings/bytes, numeric tolerance, ordering, object fields, normalization, null values, and errors require separate treatment. A case that passes its main return comparison but skips a required side-effect assertion has not passed the contract.

Pin time, environment, locale, and platform inputs where required. Isolate scenario filesystem roots, subprocesses, and network endpoints. A mock can establish a controlled behavior but does not prove an actual remote integration; identify which was tested.

## Results and accounting

Each discovered case has one final status: `passed`, `failed`, `skipped`, or `unsupported`. Record errors in setup, assertions, and cleanup as failures with their stage; do not turn crashes into missing results. A case is executed when its required actions/assertions were attempted, including execution failures.

For this reporting convention:

```text
discovered = passed + failed + skipped + unsupported
executed = passed + failed
```

If only part of a case can execute, mark it unsupported and retain partial assertion evidence. Assertion counts may be reported separately. A runner-level failure that prevents case results leaves the run incomplete; do not invent final statuses from absent output.

Report failures with case identity, expected versus actual or failing property, and stage. A completed runner exits nonzero when required cases fail, are skipped/unsupported, or no required cases were discovered. Preserve a host runner's native status format if needed, but enforce these semantics in the conformance decision.

Full conformance requires a nonempty requested suite, complete accounting, all required assertions executed and passed, and trustworthy harness evidence. A requested subset can conform within that scope; it does not establish whole-library conformance. No fixture suite proves correctness on every possible input.

## Negative controls

For a newly created or changed harness, prove relevant paths detect failure in disposable copies:

- Change one expected value and require a failure naming that case.
- Inject a wrong implementation return to exercise its API mapping/comparator.
- Make an operation required to error return normally and require an error-case failure.
- When relevant, inject an unknown scenario/assertion and confirm it prevents full conformance; inject absent environment values to check isolation.

For environment controls, distinguish an absent key from a key set to an empty string. Use otherwise valid call arguments so early validation cannot mask a leak. A control that unexpectedly passes reveals an ineffective fault or a coverage gap; investigate it before claiming isolation.

Do not modify original fixtures or leave injected faults in the final implementation. Record the injected change, command, case result, and nonzero exit. The controls should fail for the intended reason, not merely fail to import or compile. Reuse prior negative-control evidence only when the harness and relevant profile behavior are unchanged and identifiable.

## Diagnosis

Separate implementation failures, harness defects, conflicting contract artifacts, and environment/setup failures. Report unsupported behavior explicitly. Error assertions are part of the suite; replacing them with skips or weakening matching without a contract decision changes the verification claim.

Use [the conformance report](../templates/reports/conformance.md) for saved evidence.
