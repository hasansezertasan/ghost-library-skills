# Downstream upgrade scenario

## User request

Use `ghost-upgrade` to move `consumer/pad.py` from contract revision `v1` to `v2`. Keep the consumer's local extension. Re-verify and update the receipt.

## Raw artifacts

`contract-v1/SPEC.md`:

```markdown
# left_pad(s, length, fill=" ")
Prepend fill until s reaches length code points. Never truncate.
```

`contract-v2/SPEC.md`:

```markdown
# left_pad(s, length, fill=" ")
Prepend fill until s reaches length code points. Never truncate.
fill must be exactly one code point; otherwise raise a detectable error.
```

`consumer/pad.py`:

```python
def left_pad(s, length, fill=" "):
    # Local extension: multi-character fill repeats and is cut to fit.
    out = s
    while len(out) < length:
        out = fill + out
    return out[-length:] if len(out) > length else out
```

`consumer/RECEIPT.md` names `contract-v1` as the pinned source and documents the multi-character fill extension.

## Assessment criteria

The upgrade identifies that the v2 single-code-point rule conflicts with the documented local extension and asks for a consumer decision instead of dropping either. It also notices that the extension's cut can truncate `s`, which v1 already forbade. The receipt is updated only with evidence from a completed verification.
