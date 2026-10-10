# Roadmap

Work that is planned or open, but not yet done. The reasoning behind the original plan is in [the initial design record](decisions/0001-initial-design.md). Remove an item once it ships, and link its evidence from the relevant guide.

## Features

- **Optional `ghost.yaml` metadata.** A library could declare its domains, source version, fixture profile, dependency policy, and generation instructions. Skills must keep working without it by discovering layout and conventions first. Keep plugin version, contract version, fixture-format version, and source commit distinct.
- **MCP server.** Build it only after the deterministic tools are useful on their own. It would expose contract discovery, fixture validation, conformance execution, and report retrieval by wrapping those tools. Behavioral decisions stay in reviewable Markdown and fixture changes; no registry, daemon, or remote service.

## Evidence gaps

- **Later skills.** `ghost-summon`, `ghost-evaluate`, `ghost-extract`, `ghost-upgrade`, and `ghost-catalog` have scenarios and [native cases](../evals/native/cases.json) but no recorded model trials.
- **Host rediscovery.** [Host support](host-support.md) evidence was recorded with the original seven skills; all twelve have not been rediscovered on each host.
- **Model workflows.** Claude's authenticated workflows were quota-blocked; OpenCode and Pi model workflows are untested.
- **Fixture profiles.** Verification has covered `padlib` (function cases) and `wheredirs` (environment-driven). Callable scenarios (`stdlib/functional`), seeded invariants (`stdlib/random`), and process scenarios (`reporun`) remain unexercised.
