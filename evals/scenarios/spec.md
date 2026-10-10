# Specification scenario

## User request

Use `ghost-spec` to change `fit` to count Unicode code points and never normalize strings. Update examples and affected fixtures. This is an intentional change from the existing UTF-16 code-unit contract.

## Raw artifacts

`SPEC.md`:

```markdown
# fit(s, limit)
If the UTF-16 code-unit length exceeds limit, return the first limit
code units. Otherwise return s. limit is a nonnegative integer.
```

`tests.yaml`:

```yaml
fit:
  - name: ascii
    input: [abc, 2]
    output: ab
```

## Assessment criteria

The patch makes the requested representation explicit and includes non-BMP and decomposed combining-character boundaries. It explains the changed observable behavior and avoids treating grapheme count or NFC normalization as the requested rule. It does not add unrelated APIs or claim patch-level compatibility merely because the function signature is unchanged.
