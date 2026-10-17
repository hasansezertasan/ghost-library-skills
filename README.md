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

## Install

The quickest way is to give your agent the prompt in [docs/installation.md](docs/installation.md), which tells it to pick the best install route for itself. To install yourself, use the table below.

| Host | Install | Update | Invoke |
| --- | --- | --- | --- |
| [Claude Code](docs/install-claude-code.md) | `claude plugin marketplace add /absolute/path/to/ghost-library-skills`, then `claude plugin install ghost-library-skills@ghost-library-skills-marketplace` | `claude plugin marketplace update ghost-library-skills-marketplace`, then `claude plugin update ghost-library-skills@ghost-library-skills-marketplace`, then restart | `/ghost-library-skills:ghost-audit` |
| [Codex CLI](docs/install-codex.md) | `codex plugin marketplace add /absolute/path/to/ghost-library-skills`, then `codex plugin add ghost-library-skills@ghost-library-skills-marketplace`, then start a fresh session | Refresh the checkout, repeat the `add` command, then start a fresh session | Select `ghost-library-skills:ghost-audit` and provide a task |
| [Pi](docs/install-pi.md) | `pi install /absolute/path/to/ghost-library-skills` | `pi update /absolute/path/to/ghost-library-skills`, then restart | `/skill:ghost-audit` |
| [OpenCode](docs/install-opencode.md) | Point `skills.paths` at `/absolute/path/to/ghost-library-skills/skills`, then restart | Refresh the checkout (`git pull`), then restart | Ask OpenCode to use `ghost-audit`; skills load on demand through the native `skill` tool |
| [Antigravity](docs/install-antigravity.md) | `agy plugin install https://github.com/hasansezertasan/ghost-library-skills` | Reinstall the plugin, then restart | Ask Antigravity to run `ghost-audit` with a target |

The table is the index; each host name links to a page with that host's caveats — what "update" actually updates, whether a restart is required, how to verify the install, and why a local checkout is still the supported source. Per-host capabilities are recorded once in [host support](docs/host-support.md); the install pages cite it rather than restating it.

On all five hosts, restart the session after an install or update so changed skills are rediscovered. Earlier evaluations used `ghost-library-local` and then `ghost-library-marketplace`. The project is now named `ghost-library-skills`, with catalog `ghost-library-skills-marketplace`. Install one distribution at a time to avoid duplicate registrations.

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
- `package.json`: authored release version and pinned development tooling;
  identity, Pi, and npm `files` fields are generated from TOML.
- `.ai-rulez-generated.json`: generated record of every packaged file and its content hash.
- `.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/`: generated native manifests and single-plugin catalogs that install the repository root.
- `opencode.json`: OpenCode skill discovery when running from this checkout.
- `tools/`: local packaging, resource-link validation, and native smoke checks.
- `evals/`: realistic workflow cases and pilot evidence.
- `docs/`: usage and host-support boundaries.

Read [the maintainer guide](docs/maintainers.md) for the lifecycle, [host support](docs/host-support.md) for current packaging scope, [the roadmap](docs/roadmap.md) for planned work, and [the initial design record](docs/decisions/0001-initial-design.md) for the original research.

For plugin development, CI, and release-please setup, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Validate

For maintainers, edit canonical files and shared metadata, regenerate, and check:

```sh
npm run generate
npm run check
npm test
```

`npm ci` installs the locked development tooling; the unit tests need Python.
[ai-rulez generates the skills, native manifests, and catalogs](docs/ai-rulez.md)
in place, copying shared references and templates into every skill.

Generated-file checks report drift without repairing it. Native metadata and discovery checks use:

```sh
python3 tools/smoke_plugins.py --repository . --report dist/repository-validation.json
```

For disposable self-contained bundles, use `OUTPUT=dist/plugins npm run build` with an absent or empty output directory. The standalone builder remains available.

The [padlib evaluation](evals/padlib/README.md) records an isolated maintenance cycle: 117 passing Python cases, seven detected faults, and an independent native Codex audit. Claude discovered all seven commands; its model invocation was blocked by the account's weekly usage limit.

The [six remaining workflow evaluations](evals/results/native/README.md) record five clean passes and verification with a reporting limitation. The [wheredirs evaluation](evals/wheredirs/README.md) passes 166 cases and 15 warning assertions, detects ten deliberate faults, and documents the absent-environment coverage gap those controls exposed.

The workflow evaluations in [evals/README.md](evals/README.md) check decisions that structural validation cannot prove. Fixture parsing or skill validation alone does not certify an implementation.

[Private-profile installation and replacement checks](evals/results/hosts/installation/README.md) passed for all four hosts, including complete active resource hashes. Claude’s authenticated workflow retry remains quota-blocked; OpenCode and Pi model workflows have not been evaluated.

[Repository-root installation and replacement](evals/results/hosts/repository/README.md) passed on all four hosts before ai-rulez adoption.
[The original integration evaluation](evals/results/automation/adoption/README.md) records native schema adoption.
[The authoring migration](evals/results/automation/authoring/README.md) records the committed `.ai-rulez/` sources,
renamed plugin, and generated root skills.
Root metadata and the generated Claude/Codex payload are checked with `npm run check`.
