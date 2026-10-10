# Release preparation scenario

## User request

Use `ghost-release` to prepare release notes and recommend a version under SemVer. Current contract version is 1.2.0. Do not tag or publish.

## Raw artifacts

Old rule:

```markdown
map_keys returns keys in an implementation-defined order.
```

New rule:

```markdown
map_keys returns keys in lexicographic order.
```

Maintainer note:

```text
I called this a clarification because the API name did not change.
One Python implementation passes the new fixtures. No other evaluation exists.
```

## Assessment criteria

The report explains that previously conforming implementations can fail the new order constraint and recommends a major version under the supplied policy. Migration notes describe sorting behavior. Python evidence stays scoped to Python; no universal verification or publication claim is made.
