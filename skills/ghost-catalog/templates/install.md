# Generate an implementation

Adapt this prompt to the library's names, conventions, and actual paths:

```text
Implement this ghost library in [LANGUAGE] at [LOCATION].

1. Read the specification, shared conventions, and portable fixtures.
2. Map the public API and error/null behavior to idiomatic target-language forms.
3. Generate a harness that understands every required fixture assertion.
4. Implement the requested API within the contract's dependency policy.
5. Run all required cases, including errors, scenarios, and invariants.
6. Report discovered/executed/passed/failed/skipped/unsupported cases and commands.
7. Prove a new harness detects deliberately wrong results in disposable copies.
8. Record the contract source revision and how to rerun verification.

Keep contract fixtures unchanged. Surface contradictions instead of changing
expected values to match the implementation. Report unsupported requirements.
```

Add library-specific setup or mappings only when needed. An implementation belongs in the consumer-selected location; do not assume it should be committed to the contract repository.
