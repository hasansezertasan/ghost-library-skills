# Conformance report

## Scope and identity

Contract URL/path and commit or hashes; selected domains; fixture profile/identity; implementation revision; harness identity; language/runtime; relevant environment; command.

## Accounting

| Discovered | Executed | Passed | Failed | Skipped | Unsupported |
| --- | --- | --- | --- | --- | --- |

Require `discovered = passed + failed + skipped + unsupported` and `executed = passed + failed` for a completed run. Account for partial assertions separately. Runner crashes with absent results leave the run incomplete.

## Case evidence

Case ID, final status, failing stage or assertion, expected/actual values, skip/unsupported reasons, and relevant logs. Link full result artifacts for large suites.

## Harness negative controls

Injected fault, disposable path, exact command, expected diagnostic, observed case failure and nonzero exit, and confirmation the injection was removed. Reference reusable evidence only with matching harness/profile identity.

## Decision and limitations

State full conformance within the named scope, failing conformance, or incomplete verification. State untested platforms/integrations and finite-fixture limits. Fixture parsing alone is not implementation conformance.
