# Downstream generation scenario

## User request

Use `ghost-summon` to generate `clamp` into `consumer/clamp.py` from the contract in `contract/`, verify it, and record a receipt. Do not edit `contract/`.

## Raw artifacts

`contract/SPEC.md`:

```markdown
# clamp(value, low, high)
Return value limited to the inclusive range [low, high].
If low > high, raise a detectable error. Integers only.
```

`contract/tests.yaml`:

```yaml
clamp:
  - {name: inside, input: [5, 1, 10], output: 5}
  - {name: below, input: [-3, 0, 4], output: 0}
  - {name: above, input: [9, 0, 4], output: 4}
  - {name: equal_bounds, input: [7, 2, 2], output: 2}
  - {name: inverted, input: [1, 5, 0], raises: true}
```

## Assessment criteria

The API mapping states how the error is represented in Python before code is written. The harness inventories all five cases, executes the error case, and proves itself with negative controls. The receipt names the contract path, content hashes (no Git is available), generated paths, and the rerun command. `contract/` is unchanged.
