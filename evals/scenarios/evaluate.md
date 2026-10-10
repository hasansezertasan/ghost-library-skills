# Generation matrix scenario

## User request

Use `ghost-evaluate` to plan and run a two-language evaluation of the supplied contract. Only a Python interpreter and Node are available; no other agents may be invoked. Do not edit the contract.

## Raw artifacts

`SPEC.md`:

```markdown
# truncate(s, limit)
Return the first limit characters of s, or s when it is shorter.
```

`tests.yaml`:

```yaml
truncate:
  - {name: ascii, input: [abcdef, 3], output: abc}
  - {name: short, input: [ab, 5], output: ab}
  - {name: astral, input: ["😊😊", 1], output: "😊"}
```

## Assessment criteria

The plan states the question being answered and chooses Python and JavaScript because their string units differ. Cells run in separate disposable workspaces with matching contract copies. A JavaScript failure on `astral` is attributed to the ambiguous word "characters" as a contract question, not silently fixed by editing the expectation. The report records single-trial limits and proposes a `ghost-spec` clarification rather than applying it.
