# Release and generation automation

The current [ai-rulez authoring structure](ai-rulez.md) supersedes the source layout and metadata ownership proposed below.
Canonical skills and shared resources now live under `.ai-rulez/`;
root `skills/` is a generated, self-contained installation surface.


CI, release-please configuration, and contributor guidance are implemented locally.
The subsequent [ai-rulez integration](ai-rulez.md) adopts native JSON generation with a staged resource/verification wrapper,
superseding the initial prototype rejection.
[Integration evidence](../evals/results/automation/adoption/README.md) records the measured tradeoff and private-profile tests.
GitHub workflow execution and publication remain unexercised.
The original research below was reviewed on 2026-10-05 against `hasansezertasan/infra-copilot` at `534c0579239c676d9a921fdbc1f857caed8f0e29`,
cloned into `/private/var/folders/vj/26z0937x6zg3hvq02p8v6nfw0000gn/T/ghost-infra-research-1n1rnf94/infra-copilot`.

## Recommendation

Adopt release-please, CI, and explicit maintainer ownership rules first. Evaluate ai-rulez in a temporary prototype before replacing the current generator. Keep `package.json` as the identity/version source and preserve the native installation layout established by [the Flow packaging review](packaging-proposal.md).

| Pattern | Decision | Reason |
| --- | --- | --- |
| Conventional Commits and release PRs | Adopt | Version changes and changelog entries become reviewable together. |
| Regeneration after release version changes | Adopt | Host manifests and the tracked Codex payload must match the bumped source version. |
| Validation of the actual release commit | Adopt | A later green commit must not authorize releasing an older failing tree. |
| Source/generated ownership guidance | Adopt | Contributors need an explicit edit, regenerate, and check path. |
| Locked tooling dependencies | Adopt when adding tools | Local development and CI should resolve the same versions. |
| ai-rulez plugin generation | Prototype | It may replace host-specific generation, but must preserve our Pi package and resource packaging. |
| Hub skill with thin routers | Keep current structure | Our seven workflows currently work independently; a hub would introduce an installation dependency. |

## What infra-copilot establishes

Its canonical skills and commands live under `.ai-rulez/`. The [configuration](https://github.com/hasansezertasan/infra-copilot/blob/534c0579239c676d9a921fdbc1f857caed8f0e29/.ai-rulez/config.toml) owns plugin metadata and selects Claude and Codex generation. The private npm tooling package pins ai-rulez to `4.11.3`; it is not the plugin's version source. Generated outputs are committed and inventoried in `.ai-rulez-generated.json`, including non-Markdown files that lack generated-file headers.

The [Makefile](https://github.com/hasansezertasan/infra-copilot/blob/534c0579239c676d9a921fdbc1f857caed8f0e29/Makefile) separates normal checks, installation smoke tests, and upstream network checks. Its subset installation test verifies a router skill's dependency closure. That distinction matters here: copying a canonical `ghost-*` folder alone does not include the shared root resources. Our standalone builder already produces self-contained folders; new installer instructions must test those resources too.

## Release implementation

1. Add a PR/push validation workflow running `make check` and a disposable bundle build. Use scoped read permissions and pinned action revisions. Keep authenticated model evaluations separate from routine checks; add native installation jobs only with their required tools and isolated profiles provisioned.
2. Add manifest-based release-please configuration under `.config/`. Use the `node` strategy to update the existing Pi `package.json` and `CHANGELOG.md`, with a single root package and `vX.Y.Z` tags. A Node release strategy does not itself publish to npm. Do not copy infra-copilot's private tooling package or move our version into TOML as part of this step.
3. When release-please creates or rewrites its PR, check out that branch, run `make sync`, validate and build the regenerated tree, and commit only the generated manifest/package changes. Repeat regeneration on each PR rewrite. Maintain one authored version source rather than configuring independent updates to every generated version copy.
4. Before creating a tag and GitHub Release, validate the exact merge commit being released. Borrow the [release workflow's](https://github.com/hasansezertasan/infra-copilot/blob/534c0579239c676d9a921fdbc1f857caed8f0e29/.github/workflows/release.yml) guard against releasing an older pending PR after an unrelated green push, and document failed-run recovery.
5. Add contributor guidance for Conventional Commit PR titles, source/generated ownership, checks, and release recovery. Keep the existing maintainer guide focused on using the ghost-library lifecycle skills.

Both local tag enumeration and the remote tag listing returned no tags during this review. Treat this as first-release bootstrap: explicitly configure the intended initial release, provisionally `0.1.0`, instead of claiming an already released version in the release manifest. Recheck release history when implementing.

The [official release-please action documentation](https://github.com/googleapis/release-please-action#other-actions-on-release-please-prs) says events created using `GITHUB_TOKEN` do not automatically start other workflows. Explicit validation of the regenerated PR branch can provide evidence without an additional credential. If branch protection requires normal PR status checks, provide a documented manual workflow path or an appropriately scoped GitHub App token. A generic instruction to approve the bot PR does not guarantee that those checks exist. Repository settings and credentials are setup decisions, not changes made by this research.

## ai-rulez prototype

The [current upstream documentation](https://github.com/Goldziher/ai-rulez#generate-plugins-not-just-config) lists more plugin runtimes than infra-copilot enables and includes a Pi configuration preset elsewhere. A configuration preset does not establish compatibility with our installable Pi package. Evaluate an exact pinned version; infra-copilot's `4.11.3` is a reproducibility reference, not a claim about the latest release.

Use a temporary copy to generate two representative skills: one using shared references and one using artifact templates. Keep builtin governance content disabled unless deliberately selected. Test:

- Preservation of frontmatter, `agents/openai.yaml`, resource contents, and relative links.
- Native Claude/Codex manifests and marketplace source paths against our current installation layout.
- Preservation of `package.json`'s Pi declaration and file allowlist, plus OpenCode discovery from a consumer project.
- Self-contained standalone skill builds and removal of stale generated files.
- Read-only verification that detects drift without repairing the checkout.
- A source-version bump followed by regeneration and successful validation.

Measure which existing generator responsibilities actually disappear. Adopt ai-rulez if it reduces maintained host-specific code while retaining these contracts. If custom resource bundling, Pi packaging, and catalog generation remain necessary, keep those narrowly scoped tools and avoid introducing a second metadata authority. Hermes and Antigravity output would still need native validation before being advertised as supported.

## Implemented outcome

The checkout includes CI and release workflows, release-please configuration,
a regression-tested release guard, `make check-all`, and contributor ownership guidance in `AGENTS.md` and `CONTRIBUTING.md`.
ai-rulez is now a pinned root development dependency used by native packaging and CI;
the separate evaluation tooling remains under `evals/automation/`.
The integration preserves root Pi metadata, delegates native JSON schemas upstream,
and keeps the resource builder and strict checkout checks.
Native installation evidence validates both catalogs pointing at the shared generated member.
It does not publish a release or add model-workflow support claims.
