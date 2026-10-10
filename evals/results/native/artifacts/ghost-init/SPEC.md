# cronwords behavioral specification

Contract identifier: `cronwords/draft-0`.

Status: **incomplete draft; dialect decision required**. The rules marked below
as independent can be reviewed now. Schedule syntax, schedule descriptions, and
validation of nonblank strings remain pending. This is not a released contract.

## Purpose and scope

Describe one cron expression in English for display in applications and tools.
This is a deterministic utility: given the same input and finalized contract,
the result must be the same across languages and environments.

The public API has one proposed operation. Parsing structures, validation helpers,
next-run calculation, job execution, crontab file parsing (including command and
environment lines), localization, time-zone resolution, and natural-language
input are outside scope. A description represents schedule rules, not a guarantee
that a calendar occurrence exists or that a scheduler will execute a job.

No network, current clock, external dataset, host locale, environment variables,
filesystem, or scheduler installation is required. English strings are part of
the contract, not obtained from the consumer's locale. Support for a particular
programming language or platform is a consumer responsibility.

Consumers may use implementation dependencies, provided they preserve the
contract and document those dependencies and their versions. A parser dependency's
defaults do not define cronwords behavior. There is no runtime dependency on this
repository. This draft makes no latency, throughput, or maximum-input-size
guarantee; input must not be silently truncated. Resource/performance guarantees
can be added with measurable requirements if a consumer needs them.

## Proposed public API

Language-neutral signature:

```text
describe(expression: string) -> success(text: string) | failure(code: string)
```

Portable fixture representation:

```json
{"ok": true, "text": "Every minute."}
```

or

```json
{"ok": false, "error": "INVALID_INPUT"}
```

Names, signatures, exceptions, and native result types may be idiomatic. A
consumer must document how they map to these two exclusive outcomes. Failure is
never a valid null description. Exact exception classes and error messages are
not prescribed. The portable result contains exactly the fields shown for its
branch; diagnostics may exist outside that projection.

There are no options in this proposed API. The initial design is for one selected
dialect with fixed English rendering. If several dialects are required, the API
must be revised to select them explicitly; never autodetect ambiguous expressions.

## Independent input rules

- **I1 — Types:** missing input, explicit null, numbers (including zero), booleans,
  arrays, and objects produce `INVALID_INPUT`. Never stringify or coerce them.
  Native static typing may prevent a call; a harness must document that mapping
  rather than pretend it executed an impossible call.
- **I2 — Empty input:** an empty string, or a string consisting solely of ASCII
  space, tab, carriage return, and line feed, produces `EMPTY_EXPRESSION`.
- **I3 — Order:** type validation precedes blank-string validation. A missing
  argument is distinct from null even though both currently have the same error.
- **I4 — Purity:** input is not mutated. Repeated calls have no observable state
  changes and return identical projected outcomes. No clock or ambient locale
  affects descriptions.
- **I5 — Other strings:** every other string proceeds to dialect-specific parsing.
  This draft deliberately does not specify its success or error. I2 does not
  authorize trimming or accepting separators within a nonblank expression.

Strings are Unicode text. No case folding, Unicode normalization, or conversion
of Unicode digits is implied. Which characters the grammar accepts (including
non-ASCII whitespace and names) must be settled with the dialect profile. There
is no string length computation in this API's observable output.

## Schedule syntax and rendering — pending

No cron dialect has been selected. Field count, field order, numeric bounds,
wildcards, lists, ranges, steps, names, aliases/macros, and special operators are
not accepted by this draft merely because a pending fixture mentions them.

Before promotion to a complete contract, name and fully specify a dialect profile:

1. Fields, order, bounds, optional seconds/year, and whitespace rules.
2. Operators and their expansion: wildcard, list, inclusive range, step origin,
   wraparound, duplicates, and ordering. Define empty lists, reversed ranges,
   zero/negative steps, overflow, and malformed-token rejection.
3. Month/weekday names and their case rules; numeric weekday mapping and whether
   alternative Sunday numbers are aliases.
4. When both day-of-month and day-of-week are constrained, define their logical
   relationship. Do not infer OR or AND from the five-field shape.
5. Supported special forms, if any: macros such as `@daily`, `?`, `L`, `W`, `#`,
   and implementation-specific extensions. Explicitly reject excluded forms.
6. Impossible calendar combinations: decide whether they are valid schedule
   rules with no occurrences or an error. Distinguish syntax from calendar
   satisfiability; no next-run API is implied.
7. Rejection of extra fields, crontab commands, time-zone prefixes, comments,
   unsupported syntax, invalid names, and out-of-range numbers.

For the finalized profile, syntactically invalid or excluded expressions will
produce `INVALID_EXPRESSION`. Do not use that category to mask a missing contract
decision during drafting.

Proposed rendering convention: one sentence, initial capital, final period,
24-hour times with two-digit hour and minute, full English weekday/month names,
and byte-exact fixture strings (no case, punctuation, or whitespace tolerance).
Examples in pending fixtures are proposals, not evidence of verified behavior.
The complete contract must supply composition rules for every accepted syntax,
including multi-field restrictions, conjunctions, list ordering, singular/plural
units, and equivalent expressions. A formatter must preserve day-combination
semantics explicitly and must not imply an execution time zone.

## Fixtures and authority

Read [fixtures/README.md](fixtures/README.md) for the schema and runner rules.
The spec and required fixtures jointly define the independent draft slice. A
disagreement requires review; neither artifact may be silently rewritten to match
an implementation. Pending fixtures define proposed review cases only.

## Completion and compatibility

There is no previous released behavior to migrate. Finalizing the dialect must
update the spec, README example, fixture applicability/expectations, and generation
instructions together. Add cases covering each accepted grammar branch and its
boundaries before claiming a complete contract. Retain IDs when their semantics
remain the same; record changed expectations when promoting this draft.

The material decision is: which exact cron dialect/profile should cronwords
accept, and should version one support one profile or multiple explicitly selected
profiles? A family name alone may need refinement where day semantics or extensions
vary. Until that decision is made, generation of a full implementation is blocked.
