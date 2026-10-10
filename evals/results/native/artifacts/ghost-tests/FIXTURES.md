# Portable shuffle invariant fixtures

`SPEC.md` defines the behavior; `tests.yaml` contains data-driven checks of that
behavior. This document defines how a runner executes those checks. It adds no
distribution requirement or cross-language PRNG algorithm.

## Schema and comparison

`shuffle_invariants` is the case list. Each record has a unique, stable `name`,
an integer `seed`, and a `seq` list. The cases currently use only strings and
empty lists. Decode YAML strings exactly: compare Unicode code points without
normalization, case folding, locale collation, or trimming. In particular,
`"\u00e9"` and `"e\u0301"` are different element values.

Map the public `shuffle(seq, rng)` API to the implementation's idiomatic API.
Construct the implementation's RNG with `seed`; do not pass the integer as the
RNG argument unless the adapter constructs the RNG. All cases use seed 1. No
specific generator, seed-to-state mapping, or exact shuffled order is required.

The optional `draws` field is a positive integer, defaulting to 1. It counts
successive shuffle calls using one RNG instance; it is not a count of random
numbers consumed internally. Assertion fields, when present, must be boolean
`true`. An omitted assertion is not requested by that record. The original
`length` record remains a length-only check.

| Assertion | Required observation |
| --- | --- |
| `preserves_length` | Every result has the length of the original input snapshot. |
| `preserves_multiset` | Every result has exactly the same element values and occurrence counts as the original snapshot. Set equality alone is insufficient. |
| `preserves_input` | After every call, the input still equals its original snapshot element by element, in the same order. Check it again after the final call. |
| `returns_new_sequence` | Every result is a fresh sequence container: it is distinct from the supplied input and from all retained earlier result containers in that stream, including for empty and singleton inputs. Equal contents are allowed. |
| `reproduces_stream` | Two fresh RNGs constructed with the same seed in the same implementation produce equal ordered result sequences for all `draws` calls. Compare each result element by element at the corresponding call index. |

These are observable checks, not instructions to evaluate fixture text as code.
No callable helpers are used. Fresh-container identity must be checked through
the runtime's object identity or an adapter that can establish fresh allocation;
value equality cannot establish it. A runner unable to observe that requirement
must report it as unsupported rather than omit it. Input non-mutation is checked
at call boundaries; these fixtures cannot detect a temporary mutation restored
before a call returns.

## Execution and replay protocol

1. Setup: decode the case, keep an independent value snapshot of `seq`, create
   a fresh input container, and create a fresh RNG seeded with `seed`.
2. Actions: call `shuffle` exactly `draws` times with that same input container
   and RNG. Do not reseed between calls, and do not feed a shuffled result into
   the next call. Retain every returned container so identity checks cannot be
   defeated by object-ID reuse. Capture an independent ordered value snapshot
   of each result immediately after the call.
3. Observations: run every requested per-call invariant against the original
   input snapshot and check final input non-mutation when requested. Check
   result identity before copying it; a runner must not hide aliasing by copying
   the implementation's result first.
4. Replay: when `reproduces_stream` is present, create a second fresh input
   container with the original values and a second fresh RNG with the same seed.
   Repeat steps 2 and 3 for that stream. Compare the two lists of result snapshots
   in call order, with exact element order inside each result. Keep the first
   stream's RNG alive during replay; the two RNGs must be separate instances.
5. Cleanup: release retained inputs, snapshots, results, and RNGs even on failure.
   Execute cases in isolation; do not share RNGs or change host process settings.

Reproducibility is local to a fixed implementation, runtime, and RNG
configuration. The runner records those details. There are two streams of 16
calls in each replay case; this is a finite replay check, not a statistical test.
There are no distribution thresholds or probabilistic acceptance criteria.
Never require two seeds to differ, a result to differ from its input, successive
calls to differ, or an exact cross-language stream. A fresh copy returned in
unchanged order can satisfy the current specification; uniformity and a
nontrivial permutation guarantee would require a separate contract decision.

## Required handling and accounting

Only `name`, `seed`, `seq`, `draws`, and the five assertion fields above are
recognized case fields. Unknown groups or fields must be reported as unsupported
requirements (or rejected as schema errors), never silently ignored. Malformed
known fields and duplicate names are schema errors. Normal calls are required
to succeed; an implementation error is a failed case, not a valid empty result.
No portable error category or error-message contract is defined here.

Count each case record once, regardless of its draws, streams, or assertions.
A case passes only if every requested assertion executes and passes. Report
setup, call, assertion, or cleanup failures with the case name and stage. An
unsupported assertion makes the case unsupported; retain any partial evidence.
Maintain `discovered = passed + failed + skipped + unsupported` and
`executed = passed + failed`. Full conformance requires all discovered cases to
pass; failures, skips, unsupported requirements, or zero discovered cases must
prevent a successful conformance exit.
