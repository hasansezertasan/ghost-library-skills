# Installing ghost-library-skills on OpenCode

Per-host capabilities — including the fact that skills load through the native `skill`
tool rather than slash commands — live in [host-support.md](host-support.md). This page
covers install only.

OpenCode's model differs from the other three hosts: it **loads skills from a path**,
not from a plugin registry. There is nothing to register and no package cache to
refresh.

## Install

From this checkout, run `opencode`. Its root `opencode.json` declares
`skills.paths: ["./skills"]`.

To discover the skills from another project, add an absolute path to that project's
existing OpenCode configuration:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["/absolute/path/to/ghost-library-skills/skills"]
  }
}
```

Merge this field into existing configuration. Unlike the `npx skills add` copy model,
this points at the checkout, so every generated skill stays available. On the tested
CLI, pointing `OPENCODE_CONFIG` at our root config while running elsewhere does not
resolve `./skills` relative to the config file — use an absolute skill path for that
case. See the [configuration schema](https://opencode.ai/config.json) and
[Agent Skills documentation](https://opencode.ai/docs/skills/).

Each generated skill is self-contained (skill plus its references and templates), so
pointing at the whole `skills/` tree is the supported install; there is no hub router
to pair and no per-skill closure to compute.

## Update

Refresh the checkout (`git pull`), then restart the session. There is no update command
because nothing was copied.

## Invoke

Ask OpenCode to use `ghost-audit`; it loads the instructions through its native `skill`
tool.

## Verify

Ask for a read-only audit of a target. A finding report or a no-drift report is a
working install; a response that cannot find the skill means the `paths` entry did not
resolve.
