# Maintaining a ghost library

Start with `ghost-audit` for an existing library or `ghost-init` for a new one. Read the selected skill by path or invoke its name in a host that has discovered it. Provide the target repository/domain and a concrete requested outcome.

Use `ghost-spec` for behavior decisions and `ghost-tests` for portable coverage. A behavior change usually needs both. They preserve repository conventions and identify conflicts rather than silently deciding whether prose or a fixture wins.

Use `ghost-verify` with a downstream implementation and a pinned source. The harness must account for all required cases and demonstrate that wrong behavior fails. Implementation generation can be included explicitly in the request. Results are scoped to the evaluated language, environment, domain, and revision.

For a reported bug, `ghost-fix` identifies whether the implementation, harness, fixture, spec, or environment is responsible. Keep downstream repairs in the downstream project and portable contract regressions upstream. `ghost-release` then prepares compatibility notes and release evidence.

Shared resources are loaded as needed. There is no mandatory state store, manifest, MCP server, or agent delegation. Reports can be concise responses or saved Markdown; the report templates are evidence guides, not a requirement to create files on every invocation.

These skills do not change host permissions or authorize unrelated external actions. Read-only audits remain read-only. Requests to repair artifacts authorize those repairs within the requested scope; publishing and contacting others are separate actions.
