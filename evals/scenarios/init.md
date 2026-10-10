# Initialization scenario

## User request

Use `ghost-init` to start `cronwords`, a ghost library that describes cron expressions in English. This repository currently has a README and an existing license. I have not decided which cron dialect it should accept.

## Raw artifacts

`README.md`:

```markdown
# cronwords
A cron expression parsing to human-readable text, with no code.
```

Existing license: retain it; its text is not part of the behavior decision.

## Assessment criteria

The workflow identifies that five-field Unix cron, six-field expressions, and extension syntax can yield different valid inputs and descriptions. It asks for the material dialect decision while progressing on independent scope and layout. It does not invent broad compatibility, language implementations, a new license, or timezone scheduling behavior. Any unresolved dialect-dependent rules remain a draft.
