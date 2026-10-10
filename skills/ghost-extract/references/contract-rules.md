# Contract rules

## Authority and scope

Read the target repository's own instructions and conventions. Identify its specifications, portable fixtures, generation guidance, selected domains, and source revision. Do not assume every ghost library uses `SPEC.md` at the root or has an `INSTALL.md`.

Use explicit local precedence rules to understand existing artifacts. A genuine disagreement still needs a located finding and a deliberate resolution; precedence is not permission to silently change behavior. The user's stated behavior can resolve a decision. Otherwise, continue independent work and ask only about the conflicting behavior.

Specs and fixtures jointly describe the contract. A reference implementation or dependency can provide evidence, but its behavior does not automatically override either artifact. Distinguish a normative requirement, an example, implementation guidance, and a non-binding suggestion.

## Observable behavior

Specify the public API, input and output representations, defaults, accepted types, detectable errors, and exclusions. Make relevant edge decisions explicit:

- Missing, explicit null, empty, false, and zero are different values unless the contract equates them.
- String length can mean bytes, code units, code points, grapheme clusters, or display columns. Name the intended unit. State normalization only if it is required.
- Numeric formatting, integer range, overflow, float tolerance, and rounding can differ by runtime. State required behavior or permitted variation.
- Ordering and mutation are observable. Define both when they matter.
- Callable helpers need defined semantics, especially truthiness and equality across languages.
- Environmental inputs include clock, locale, platform, filesystem, network, and process state. Pin or inject them for tests when they influence results.
- Errors need a portable detection rule. Exact messages and types are requirements only when explicitly specified. Translate exceptions to language-native error results without losing the distinction between failure and a valid null value.

Allow idiomatic names, signatures, representations, and internal designs when a documented mapping preserves behavior. Algorithms belong in a behavioral contract when they determine byte-exact results or other required observable guarantees.

## Maintenance boundaries

The ghost library's primary deliverables are its contract and fixtures. Generated implementations normally live downstream or in disposable evaluation workspaces. Follow explicit repository policy for tooling and evaluation code; do not impose a universal prohibition on maintainer tools.

Record the dependency policy separately: standard-library-only, specified allowed dependencies, or unrestricted implementation dependencies. Shipping no implementation does not establish dependency freedom, supply-chain immunity, or freedom from maintenance.

Preserve consumer-local extensions separately from upstream behavior. Do not treat every customization as a portable contract rule. Existing licenses and attribution should remain intact; choose a new license only with a maintainer decision.

## Evidence

Use source paths and line/section/case identifiers for findings. Separate observed defects from portability questions and conjectures. Parsing fixtures validates syntax; it does not prove their expectations, coverage, runner semantics, or implementation correctness.

Read [compatibility](compatibility.md) when behavior changes and [fixture profiles](fixture-profiles.md) when adding or interpreting cases. For implementation verification, use [harness rules](harness-contract.md).
