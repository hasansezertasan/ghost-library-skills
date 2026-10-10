# Generate a consumer implementation

**Draft gate:** do not generate a full cronwords implementation from this revision.
First resolve the dialect decision in SPEC.md, complete its grammar and rendering
rules, and review/promote or remove every pending fixture. The repository itself
contains no implementation, and initialization requires none.

Once the contract is finalized, use this prompt in the consumer's project:

```text
Implement cronwords in [LANGUAGE] at [CONSUMER-SELECTED LOCATION].

1. Read SPEC.md, fixtures/README.md, fixtures/cases.json, and LICENSE from the
   selected contract revision. Stop and report any unresolved draft decisions.
2. Map describe, input types, missing/null behavior, success, and error categories
   to idiomatic language forms. Document the portable fixture projection.
3. Generate a harness supporting every required case and assertion. Do not
   evaluate fixture text as executable code or silently skip unsupported inputs.
4. Implement only the selected cron profile and specified English descriptions.
   Document implementation dependencies and versions. Do not inherit behavior
   from the host scheduler, locale, clock, or a dependency's default dialect.
5. Execute all required cases, including errors and repeatability/non-mutation
   checks. Report discovered/required/pending/executed/passed/failed/skipped/
   unsupported counts, commands, and any statically prevented calls.
6. In disposable copies, prove the harness rejects a wrong English string, a
   wrong error category, and a coerced non-string input. Retain the evidence.
7. Retain the contract identifier and source revision with the consumer's code:
   use its Git commit if available, otherwise a SHA-256 manifest of README.md,
   SPEC.md, INSTALL.md, LICENSE, and all fixture files. Record rerun instructions,
   API mapping, dependency versions, and any consumer-local extensions separately.

Keep the source fixtures unchanged. Report contradictions and unsupported
assertions rather than changing expected outcomes to fit the implementation.
Do not claim complete or cross-language conformance from partial execution.
```

The consumer owns generated code, integration, verification, and maintenance.
Language and destination are chosen when consuming the contract; they are not
needed to finish this repository's draft. Preserve the supplied license text.
