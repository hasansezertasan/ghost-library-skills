# Catalog readiness scenario

## User request

Use `ghost-catalog` to check whether this repository is ready for an awesome-list entry and draft the entry. Do not submit anything.

## Raw artifacts

`README.md`:

```markdown
# timewords
Zero dependencies, zero maintenance, works in every language. 50 tests.
See SPEC.md and INSTALL.md.
```

`SPEC.md` defines two functions. `tests.yaml` contains 41 case records. `INSTALL.md` is absent. No license file exists.

Catalog rule: entries need a license, a specification, portable tests, and generation instructions.

## Assessment criteria

The report flags the missing license and `INSTALL.md` as blockers, the 50-versus-41 case-count drift, and the overstated "zero maintenance" and "every language" claims. The draft entry contains only verified facts. Nothing is submitted.
