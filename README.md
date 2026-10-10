# ghost-library-skills

Portable skills for maintaining ghost libraries: specifications, language-agnostic fixtures, and instructions that let a coding agent generate an implementation downstream.

Maintain one behavioral contract, generate idiomatic implementations, and retain evidence that they conform.

## Skills

| Skill | Use it to |
| --- | --- |
| [ghost-init](skills/ghost-init/SKILL.md) | Turn an idea into a bounded library or independent domain |
| [ghost-spec](skills/ghost-spec/SKILL.md) | Define or change behavior and assess compatibility |
| [ghost-tests](skills/ghost-tests/SKILL.md) | Create portable cases, scenarios, and invariants |
| [ghost-audit](skills/ghost-audit/SKILL.md) | Review contradictions, coverage, portability, and documentation drift |
| [ghost-verify](skills/ghost-verify/SKILL.md) | Build or run a harness with complete case accounting |
| [ghost-fix](skills/ghost-fix/SKILL.md) | Diagnose downstream failures and add the right regression |
| [ghost-release](skills/ghost-release/SKILL.md) | Prepare contract versions, migration notes, and release evidence |
| [ghost-summon](skills/ghost-summon/SKILL.md) | Generate a verified implementation into a consumer project with a receipt |
| [ghost-evaluate](skills/ghost-evaluate/SKILL.md) | Measure how reliably a contract generates across agents and languages |
| [ghost-extract](skills/ghost-extract/SKILL.md) | Derive a contract from existing code with attribution and a chosen compatibility scope |
| [ghost-upgrade](skills/ghost-upgrade/SKILL.md) | Migrate a downstream implementation to a newer contract revision |
| [ghost-catalog](skills/ghost-catalog/SKILL.md) | Check listing readiness and draft a catalog entry |

These workflows preserve each library's layout and fixture conventions. They do not require a new manifest, a registry, a particular agent, or multiple agents. The toolkit can contain executable maintenance tools; generated library implementations belong in consumer projects or disposable evaluation workspaces.

## Use from this checkout

Give your agent a concrete task and the corresponding skill path:

```text
Read skills/ghost-audit/SKILL.md from this checkout.
Audit /path/to/padlib without editing it. Report located findings
and distinguish contract issues from implementation assumptions.
```

```text
Read skills/ghost-spec/SKILL.md from this checkout.
Add an explicitly defined behavior to /path/to/my-ghost-library.
Update its specification, examples, and affected fixtures together.
```

The tracked `skills/` folders are generated and self-contained;
each can be copied independently.
Authoring sources under `.ai-rulez/skills/` link to shared source resources.
To rebuild standalone folders from those sources:

```sh
python3 tools/build_skills.py --output /tmp/ghost-library-skills
```

The output directory must be absent or empty. Each built folder includes its skill, references, and templates, with local links rewritten. Configure your host to discover the built folders using its supported skill mechanism, or point the agent directly at the built `SKILL.md`. This command builds files; it does not install plugins or alter host configuration.

## Structure

- `.ai-rulez/config.toml`: authored plugin identity, runtime selection, and display options.
- `.ai-rulez/skills/`: canonical workflows and optional Codex display metadata.
- `.ai-rulez/references/`, `.ai-rulez/templates/`: shared guidance and artifact templates.
- `skills/`: generated self-contained workflows for Pi, OpenCode, and direct use.
- `package.json`: authored release version, Pi declaration, and pinned development tooling;
  plugin identity fields are generated from TOML.
- `.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/`: generated native manifests and single-plugin catalogs that install the repository root.
- `opencode.json`: generated skill discovery when running from this checkout.
- `tools/`: local packaging, resource-link validation, and native smoke checks.
- `evals/`: realistic workflow cases and pilot evidence.
- `docs/`: usage and host-support boundaries.

Read [the maintainer guide](docs/maintainers.md) for the lifecycle, [host support](docs/host-support.md) for current packaging scope, and [PROPOSAL.md](PROPOSAL.md) for the research and longer-term design.

For plugin development, CI, and release-please setup, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Install and validate

Install directly from this checkout, without a build step:

```sh
claude plugin marketplace add /absolute/path/to/ghost-library-skills
claude plugin install ghost-library-skills@ghost-library-skills-marketplace

codex plugin marketplace add /absolute/path/to/ghost-library-skills
codex plugin add ghost-library-skills@ghost-library-skills-marketplace

pi install /absolute/path/to/ghost-library-skills
```

OpenCode discovers generated skills when launched from this checkout. In another project, configure an absolute skill path. See [host support](docs/host-support.md) for invocation, update commands, and tested limits. The new repository layout has not yet been published to GitHub.

For maintainers, edit canonical files and shared metadata, regenerate, and check:

```sh
make sync
make check
```

These targets require Python, Node, and npm.
They install locked development tooling when needed.
[ai-rulez generates the native manifests and catalogs](docs/ai-rulez.md) in temporary staging trees;
our builder preserves the Pi package and self-contained skill resources.

Generated-file checks report drift without repairing it. Native metadata and discovery checks use:

```sh
python3 tools/smoke_plugins.py --repository . --report dist/repository-validation.json
```

For disposable self-contained bundles, use `make build OUTPUT=dist/plugins` with an absent or empty output directory. The standalone builder remains available.

The [padlib evaluation](evals/padlib/README.md) records an isolated maintenance cycle: 117 passing Python cases, seven detected faults, and an independent native Codex audit. Claude discovered all seven commands; its model invocation was blocked by the account's weekly usage limit.

The [six remaining workflow evaluations](evals/results/native/README.md) record five clean passes and verification with a reporting limitation. The [wheredirs evaluation](evals/wheredirs/README.md) passes 166 cases and 15 warning assertions, detects ten deliberate faults, and documents the absent-environment coverage gap those controls exposed.

The workflow evaluations in [evals/README.md](evals/README.md) check decisions that structural validation cannot prove. Fixture parsing or skill validation alone does not certify an implementation.

[Private-profile installation and replacement checks](evals/results/hosts/installation/README.md) passed for all four hosts, including complete active resource hashes. Claude’s authenticated workflow retry remains quota-blocked; OpenCode and Pi model workflows have not been evaluated.

[Repository-root installation and replacement](evals/results/hosts/repository/README.md) passed on all four hosts before ai-rulez adoption.
[The original integration evaluation](evals/results/automation/adoption/README.md) records native schema adoption.
[The authoring migration](evals/results/automation/authoring/README.md) records the committed `.ai-rulez/` sources,
renamed plugin, and generated root skills.
Root metadata and the generated Claude/Codex payload are checked with `make check`.
