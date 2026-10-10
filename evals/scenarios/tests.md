# Invariant fixture scenario

## User request

Use `ghost-tests` to add meaningful portable coverage for this contract. Preserve its invariant-based format.

## Raw artifacts

`SPEC.md`:

```markdown
# shuffle(seq, rng)
Return a new sequence with the same multiset and length. Do not mutate seq.
A fixed seed reproduces a stream within one implementation.
Different languages may use different PRNG algorithms and streams.
```

`tests.yaml`:

```yaml
shuffle_invariants:
  - name: length
    seed: 1
    seq: [a, b, c]
    preserves_length: true
```

## Assessment criteria

Fixtures cover multiset preservation including duplicates, input non-mutation, empty input, and local seeded reproducibility. New assertion/scenario semantics are documented. No hand-picked permutation becomes a universal cross-language expectation. Syntax/coverage checks are reported separately from implementation verification.
