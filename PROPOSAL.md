# Ghost library plugin proposal

Research snapshot: 2026-10-05. This document preserves the original design research. The seven core skills and the five later additions are implemented; the later [packaging migration](docs/packaging-proposal.md) replaces the original `adapters/` layout.

## Recommendation

Build a portable toolkit for authoring, auditing, and evolving behavioral contracts. Make downstream generation and verification first-class workflows, because that is how a maintainer learns whether the contract works.

The central promise should be: **maintain one behavioral contract, generate idiomatic implementations, and retain evidence that they conform.**

The plugin itself may contain code for validation, packaging, and test orchestration. The ghost libraries it maintains continue to ship specifications and fixtures as their primary deliverables. Generated implementations live downstream or in disposable evaluation directories.

## What I inspected

The [GitHub topic](https://github.com/topics/ghost-library) and repository search returned six repositories, all under `hasansezertasan`. I shallow-cloned all six, plus the awesome list and `dbreunig/whenwords`, into:

`/var/folders/vj/26z0937x6zg3hvq02p8v6nfw0000gn/T/ghost-library-research-9wgtu5nh`

The temporary `inventory.json` records each source URL, local path, and exact commit. I inspected repository layouts, READMEs, specifications, installation instructions, fixtures, and authoring conventions. I parsed all 20 `tests.yaml` files successfully with Ruby's YAML parser. Counts below count case records, not individual assertions. I did not generate or certify downstream implementations.

| Project | Snapshot | Approach | Lesson for the plugin |
| --- | --- | --- | --- |
| [padlib](https://github.com/hasansezertasan/padlib) | `4c8ae4d`; 111 cases | Five compact string utilities; code-point length, pattern truncation, explicit errors | Best first pilot for authoring and conformance |
| [wheredirs](https://github.com/hasansezertasan/wheredirs) | `7c83fe3`; 155 cases | Four platform strategies; pinned environment inputs; detailed runner and null/error contracts | Strong model for environment isolation, bounded APIs, and explicit platform policy |
| [ualib](https://github.com/hasansezertasan/ualib) | `5c8999c`; 100 cases | Structured parsing plus four predicates; shared classification invariants; permits existing parser dependencies | Dependency policy and detection-data freshness must be explicit |
| [reporun](https://github.com/hasansezertasan/reporun) | `67826fe`; 37 scenarios | Build/runtime phases, subprocesses, filesystem assertions, networking, exit codes | Needs scenario setup and observable side-effect assertions |
| [stdlib](https://github.com/hasansezertasan/stdlib) | `a05efdd`; 381 cases across 15 domains | Independent domain contracts, common conventions, named callables/scenarios, random invariants | Support selective domain loading and several kinds of conformance |
| [cronwords](https://github.com/hasansezertasan/cronwords) | `be07a7e`; no fixtures | README and license only | Support taking a concept through scope decisions to its first contract |
| [whenwords](https://github.com/dbreunig/whenwords) | `1472e9d`; 123 cases | Small timestamp utilities; boundary rules, portable fixtures, generation prompt | The minimal spec/fixtures/prompt pattern remains a good default |

Your [awesome list](https://github.com/hasansezertasan/awesome-ghost-libraries) at `95864c3` declares ten projects in `projects.yaml`, including four outside the topic inventory. Those four were outside this cloning scope. Its generated README currently displays zero projects despite the populated source list; the cause needs a separate generator investigation.

## Philosophy and implications

[Drew Breunig's article](https://www.dbreunig.com/2026/01/08/a-software-library-with-no-code.html) establishes the small-library experiment and discusses its limits: performance, testing, support, frequent updates, and community. This suggests evaluating suitability before turning a dependency into a ghost library.

[Armin Ronacher's porting account](https://lucumr.pocoo.org/2026/1/14/minijinja-go-port/) shows shared snapshots enabling idiomatic implementation changes. It also describes an agent abandoning negative tests and needing correction. This suggests making error-case execution and skip accounting part of conformance evidence.

For [Theo's video](https://www.youtube.com/watch?v=u9P3CKwtRnM), I use the premise supplied in your request: locally maintained utilities can replace some third-party dependencies. The primary video could not be retrieved here, so I make no transcript-specific claims.

My synthesis: a ghost library distributes reusable behavior and a way to judge implementations. Local code ownership moves maintenance responsibilities; it does not eliminate them. Contracts, fixtures, and generation instructions still need versioning and bug fixes. `ualib` demonstrates that “ships no implementation” and “generates without dependencies” are separate choices.

## Concrete maintenance problems found

- **Documentation drift:** `whenwords/INSTALL.md` says 125 cases, while its current fixture file contains 123. It also lists `VERIFY.md`, which is absent from the clone.
- **Internal contradictions:** `reporun/SPEC.md`'s architecture diagram describes embedded URL and configuration, while its detailed build rules require embedding only the URL. Its mandatory `uv run` guidance also conflicts with an entrypoint example already prefixed by `uv run`.
- **Authority ambiguity:** `wheredirs/INSTALL.md` says YAML wins on graded cases but also says to stop on a real contradiction. A maintenance workflow should surface disagreements and obtain a contract decision rather than silently rewriting either artifact.
- **Portability decisions:** `padlib` specifies code-point lengths precisely, but some numeric string conversion follows language defaults. `stdlib` uses named truthiness helpers and language-specific RNGs. These are places to document permitted variation or tighten behavior deliberately.
- **Harness variation:** fixtures use `output`, `expected`, nested structured results, `raises`, separate error groups, named scenarios, invariants, and command expectations. A reader that only recognizes one schema could report a misleading success.
- **Claim quality:** README assertions such as no maintenance burden or no supply chain overstate what local generation guarantees. Audit generated dependency policy and distinguish fixture conformance from production assurance.

These are observed examples for designing skills, not a complete defect audit.

## Proposed skills

Use `ghost-` prefixes for portable names; adapters may expose commands such as `/ghost audit`.

| Skill | Trigger and work | Reviewable output |
| --- | --- | --- |
| `ghost-init` | Create a ghost library or independent domain; assess scope, external state, dependency policy, and testability | Small API, explicit exclusions, draft spec/fixtures/install prompt |
| `ghost-spec` | Add or change behavior; define types, defaults, boundaries, errors, Unicode, ordering, and allowed variation | Contract patch, examples, compatibility assessment |
| `ghost-tests` | Add portable coverage; map rules to cases, compute exact fixtures, define scenarios or invariants | Fixture patch and rule-to-case coverage map |
| `ghost-audit` | Review an existing library without changing its meaning | Located findings with evidence, missing cases, contradictions, documentation drift |
| `ghost-verify` | Verify a downstream implementation or build its harness | Accounted case results, harness self-checks, failures, source revision and commands |
| `ghost-fix` | Receive a downstream bug | Minimal reproducer; classification as implementation, harness, fixture, spec, or environment defect; portable regression and appropriate patch |
| `ghost-release` | Prepare a contract release | Behavioral diff, version recommendation, changelog, migration notes, supporting evidence |

Start with these seven. Keep spec review and fixture review as separate passes with distinct evidence, even when one agent performs both.

Later additions, now implemented as skills:

- `ghost-summon`: generate into a consumer-selected location with an explicit language/API mapping and invoke verification. Records a downstream receipt.
- `ghost-evaluate`: generate clean implementations across a small agent/language matrix and summarize results, costs, retries, and unsupported cases.
- `ghost-extract`: derive a contract from an existing utility or dependency, preserving attribution and explicitly choosing compatibility scope.
- `ghost-upgrade`: compare a pinned upstream revision with downstream code and local extensions; propose a targeted migration.
- `ghost-catalog`: check discoverability, metadata, required artifacts, and awesome-list eligibility.

## Repository structure

Keep one canonical skill source and thin host adapters. This is a logical layout; host-specific manifest formats and installation paths must be checked against each host's current documentation during implementation.

```text
README.md
PROPOSAL.md
skills/
  ghost-init/SKILL.md
  ghost-spec/SKILL.md
  ghost-tests/SKILL.md
  ghost-audit/SKILL.md
  ghost-verify/SKILL.md
  ghost-fix/SKILL.md
  ghost-release/SKILL.md
references/
  philosophy.md
  contract-rules.md
  fixture-profiles.md
  harness-contract.md
  compatibility.md
  recipes/
    summon.md
    evaluate.md
templates/
  single-library/           # SPEC.md, tests.yaml, INSTALL.md, README.md
  multi-domain/             # CONVENTIONS.md, domain SPEC.md and fixtures
  scenario-library/        # setup/actions/observations and isolation rules
  reports/                 # audit, conformance, release
schemas/                   # versioned metadata/report schemas, when needed
adapters/
  claude/
  codex/
  opencode/
  pi/
  hermes/
  antigravity/
tools/                     # deterministic checks and adapter packaging
evals/                     # plugin workflow fixtures and failure injections
docs/
  getting-started.md
  maintainers.md
  consumers.md
  host-support.md
```

Each skill should define its trigger, required inputs, concise procedure, output, and completion criteria. Load shared references only when relevant. Keep domain-specific knowledge in the target library instead of copying it into the plugin.

Do not require a new manifest to operate on existing repositories. Discover their layout and conventions first. Optional future `ghost.yaml` metadata could identify domains, source version, fixture profile, dependency policy, and installation instructions. Keep plugin version, contract version, fixture-format version, and source commit distinct.

For downstream provenance, optionally record a receipt with source URL/commit, domain, spec and fixture hashes, target language, generated paths, verification command, and report location. This enables bug reproduction and upgrades without turning implementations into centrally maintained packages.

Host adapters handle registration, command aliases, installation, and tool access. They should not contain independent copies of the maintenance procedure. A host with only Markdown skills should still support the core workflows. Publish a tested capability table rather than promising identical plugin features everywhere.

## Conformance design

Support explicit fixture profiles: function cases, structured parsing, environment-driven functions, scenarios, and invariants. Normalize their *reports* first; avoid rewriting existing fixture files to one format merely for convenience.

A harness must report discovered, executed, passed, failed, skipped, and unsupported cases with stable identifiers. Zero discovered cases, unsupported assertions, or unexecuted required cases prevent a full-conformance claim. A development skip list is visible and temporary. A release claiming complete conformance has no required cases skipped or unsupported.

Prove the harness can fail: change an expected value in a disposable fixture copy, inject a wrong return value, and exercise an error case that incorrectly returns normally. Keep upstream fixtures unchanged during implementation verification. Any proposed fixture correction belongs in a separate contract change with independently justified expected behavior.

Comparison policy is part of the contract: exact bytes, ordered sequences, unordered collections, numeric tolerances, null values, error categories, and normalization each require explicit treatment. Preserve `wheredirs`' declared path normalization without applying it to unrelated profiles. For scenarios, use disposable filesystem roots and controlled process/network inputs. For statistical invariants, record seeds, trials, thresholds, and the permitted reproducibility scope.

`ghost-fix` should reproduce a failure against the pinned source, identify its layer, then create the regression before the repair. Cross-language contracts should reproduce the intended behavior rather than encode an accidental quirk from one implementation.

## Commands, subagents, and MCP

Commands are entry points to the same skills. Optional reviewer roles could be contract reviewer, fixture reviewer, and conformance investigator; they need distinct questions and evidence, not separate authorities. No workflow should require multi-agent execution.

Defer MCP until deterministic tools are useful on their own. A later server could expose contract discovery, fixture validation, conformance execution, and report retrieval. It should wrap those tools; behavioral decisions remain reviewable Markdown and fixture changes. Avoid building a registry, daemon, or remote service to deliver the first useful skill.

## Suggested rollout

1. Establish shared rules and implement `ghost-audit`, `ghost-spec`, and `ghost-tests`. Use `padlib`, one ordinary `stdlib` domain, and `wheredirs` as pilots.
2. Add `ghost-init` and `ghost-verify`; use `cronwords` for creation, choosing cron dialect, timezone scope, and phrasing policy before writing fixtures. Exercise a downstream generation in Python and a language with different null/error conventions.
3. Add `ghost-fix` and `ghost-release`. Check that injected implementation bugs, broken runners, and contradictory contracts produce different diagnoses.
4. Extend verification to `stdlib/functional`, `stdlib/random`, and `reporun`. Start controlled agent/language evaluations in temporary or downstream workspaces.
5. Package and smoke-test host adapters, then consider dedicated consumer, extraction, upgrade, catalog, and MCP features.

Success for the first release: a maintainer can audit an existing contract, make a justified behavioral change with portable regression coverage, and verify a freshly generated downstream implementation with a harness that demonstrably detects failure.
