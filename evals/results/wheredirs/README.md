# wheredirs evidence

See the [evaluation description](../../wheredirs/README.md) for the method and reproduction commands.

- `conformance.json`: independent 166-case report, including 15 warning assertions.
- `negative-controls.json`: all ten deliberate faults and affected case diagnostics.
- `initial-environment-control.json`: the initially undetected missing-environment fault, before the two absent-input cases were added.
- `native-results.json`: the generated runner's 155-case/161-assertion report.
- `native-verification.json`: generated harness negative controls and supplemental checks.
- `identity.json`: pinned source, original contract preservation, native model/runtime, and artifact identities.
- `native-invocation.json`: condensed native response and command evidence.

The initial environment control is historical diagnostic evidence; its incomplete coverage is not a passing isolation result. Saved runner hashes identify the generated code, which is retained only in the disposable workspace.
