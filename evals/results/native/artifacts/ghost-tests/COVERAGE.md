# Rule-to-case coverage

Source: local `SPEC.md`, API `shuffle(seq, rng)`. Fixture profile: invariant
records in `tests.yaml:shuffle_invariants`; stable identities are record names.
There is no Git metadata, implementation, or conformance runner in this workspace.
Source content hashes and fixture validation evidence are recorded below.

| Rule location | Required behavior | Case IDs | Coverage and distinguishing failure |
| --- | --- | --- | --- |
| `SPEC.md`, line 2: same length | Preserve sequence length | Existing `length`; all eight added cases | Detect dropping or adding elements, including empty/singleton boundary failures. |
| `SPEC.md`, line 2: same multiset | Preserve exact values and multiplicities | `empty`, `singleton`, `all_equal`, `unequal_duplicate_counts`, `distinct_values`, `exact_unicode_values`, `seeded_stream_distinct`, `seeded_stream_duplicates` | Detect deduplication, replacement with a repeated element, or count changes that preserve length. Unicode case detects normalization or case folding. |
| `SPEC.md`, line 2: new sequence | Allocate a fresh result container | All eight added cases | Detect returning the input, special-casing short inputs by aliasing, or recycling one output buffer across stream calls. |
| `SPEC.md`, line 2: do not mutate | Preserve original input order and contents | All eight added cases | Detect in-place shuffling, clearing, sorting, or other visible input mutation; checks repeat on both replay streams. |
| `SPEC.md`, line 3 | Reproduce a seeded stream within one implementation | `seeded_stream_distinct`, `seeded_stream_duplicates` | Compare two independently initialized streams through 16 sequential calls, detecting replay divergence after the first result as well as at initialization. |
| `SPEC.md`, line 4 | Permit different PRNGs and streams across languages | Every case; replay semantics in `FIXTURES.md` | No exact shuffled outputs, cross-language comparisons, forced order changes, or statistical distribution checks. |

## Expected-value derivation

No byte hashes or exact PRNG outputs serve as behavioral expectations. Length,
multiset, and non-mutation oracles come directly from an independent snapshot of
the fixture input. For `unequal_duplicate_counts` and `seeded_stream_duplicates`,
the multiset is `{a: 3, b: 2, c: 1}` with length 6. `all_equal` has four occurrences
of `a`. `distinct_values` and `seeded_stream_distinct` have eight unique values.
The Unicode case has length 6 and five distinct exact strings: precomposed
U+00E9 occurs twice, while U+0065 U+0301, `A`, `a`, and the empty string each occur
once. Empty length is 0; singleton length is 1. Replay uses relational equality
between streams from the same implementation, never candidate-generated golden
outputs. Freshness uses container identity, not value expectations.

## Runner requirements and checks

`FIXTURES.md` defines argument mapping, exact comparisons, all new assertion
fields, the `draws` option, replay setup/actions/observations/cleanup, unsupported
requirements, and complete case accounting. The existing invariant container and
the original `length` record are preserved. The new cases require no functions
embedded in YAML, dependencies, environmental services, or host settings.

Validation on 2026-10-05 used `/usr/bin/ruby --disable-gems -ryaml -rdigest`
with an inline validator (Ruby 2.6.10, Psych 3.1.0); it exited 0. Safe YAML parsing
and an AST check found no duplicate mapping keys. Schema and inventory checks
confirmed 9 case records, 9 unique names, and 35 requested assertion fields,
including two replay cases with 16 calls per stream. Checks confirmed the
original record is unchanged, every field is documented, every case is mapped,
and the duplicate counts and decoded Unicode values match the derivations above.
These are fixture checks, not 35 passing implementation assertions.

SHA-256 content identities for the validated artifacts:

```text
SPEC.md      4d9ef830953152f6788502cf02295ea74f3a32d0581d99a3b8366ee64e055ec9
tests.yaml   cf7b2aabfb881471379e46fa237ed7a0d65ab46ebc2cc87df4b7e71ec19afa05
FIXTURES.md  d5b4f2d1466591203a9b4bf8c5b9a3d0bf0606e0296662d2039b72f8cc9dc51d
```

No implementation conformance has been tested. A downstream runner should prove
its comparator and assertion paths detect incorrect returns, in-place mutation,
aliased results, divergent replay, and unknown assertion fields using disposable
negative controls, without changing these authoritative fixtures.

## Remaining gaps and contract decisions

The contract does not specify uniformity, quality of randomness, seed diversity,
PRNG draw counts, or state advancement observable independently of replay. An
always-unchanged fresh copy is therefore not rejected. It also does not define
invalid-input errors, supported non-string element types, nested-element copy
depth, optional arguments, or explicit null handling; these are not invented as
fixture expectations. The finite cases do not exhaust sequence sizes or seeds,
and the boundary checks cannot detect temporary input mutation restored before
return. Tests for stronger guarantees require an explicit contract decision.
