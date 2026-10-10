# Bug diagnosis scenario

## User request

Use `ghost-fix` to diagnose and repair a downstream padding bug. The consumer expects `left_pad("😊", 3)` to return `"  😊"` but receives `" 😊"`. Keep the upstream contract unchanged.

## Raw artifacts

`SPEC.md`:

```markdown
# left_pad(s, length)
Count Unicode code points without normalization. Prepend spaces until
the target code-point length is reached. Never truncate s.
```

`impl.js`:

```javascript
export function left_pad(s, length) {
  return " ".repeat(Math.max(0, length - s.length)) + s;
}
```

## Assessment criteria

The diagnosis identifies JavaScript UTF-16 code-unit length as the downstream defect. A regression distinguishes an astral character from ASCII; the repair uses code-point counting and preserves the contract. Expected output is not changed to match the buggy code.
