# Antigravity local plugin validation

On 2026-10-14, `agy plugin validate .` (agy 1.3.5) passed against this checkout at
`cd9c11c54da6dece7ef36b40b50ffa00052e94db`. The [report](validation.json) records the
command, the tool version, and the validator output.

The validator discovered all twelve generated skills and skipped the surfaces this
plugin does not ship — agents, commands, MCP servers, and hooks. The hand-authored
root `plugin.json` is the only Antigravity-specific file; ai-rulez generates no
Antigravity manifest, and `make check` verifies the adapter against
`.ai-rulez/config.toml`.

This establishes local discovery only. Git-URL installation (`agy plugin install`),
plugin enablement, and model workflows remain unevaluated.
