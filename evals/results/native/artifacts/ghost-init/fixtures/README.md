# Draft fixture conventions

`cases.json` is UTF-8 JSON with metadata `schema_version`, `contract`, and a single
`cases` array. Count records in that array only. IDs are unique across the file.
Every record calls the proposed `describe` operation; `args` is a positional
argument list. Thus `args: []` means missing input, `args: [null]` means explicit
null, and `args: [[]]` means one array-valued input, never zero arguments.

Each case has `id`, `status`, `rule`, and `args`. Required cases have `expected`.
Pending cases have `blocked_by` and `note`, and may omit `expected` when even a
proposed outcome depends on the decision. Unknown statuses, fields, rules, or assertion kinds
must be reported as unsupported, not silently ignored. Top-level metadata is not
an assertion or a function group.

- `required`: a requirement of the independent draft slice. Compare the entire
  portable result to `expected`, with exact types, key presence, and string values.
  Object key ordering is irrelevant; extra projected result keys fail. Map native
  exceptions/results as documented in SPEC.md.
- `pending`: a candidate that cannot be executed as a normative conformance test
  until its blocking decision is resolved. When present, `expected` is a proposed outcome.
  Report these as pending, separate from unsupported or skipped required cases.
  Do not include them in a required-case pass rate or enable them through a guessed
  dialect. The five-field examples all assume minute/hour/day-of-month/month/
  day-of-week solely for review; that assumption is not a selected profile.

Execute each required case at least twice to check I4's repeatability rule. Calls
must leave the input values unchanged. Report discovered, required, pending,
executed, passed, failed, skipped, and unsupported record counts. Repetitions do
not increase record counts. A statically prevented input case must be separately
reported with its mapping/evidence, never silently counted as a runtime pass.

The initial cases distinguish missing/null/coercion/empty handling and propose
schedule tests for wildcard, fixed time, step origin, range/list wording, weekday
mapping, invalid bounds, invalid steps, extra fields, and ambiguous day semantics.
This is not full parser coverage. Once a profile is chosen, add its own boundary
and extension cases, exact descriptions for combined restrictions, and equivalent
expression cases. Parser and formatter errors must both be detectable.
