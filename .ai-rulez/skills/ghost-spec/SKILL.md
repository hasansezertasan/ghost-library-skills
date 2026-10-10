---
name: ghost-spec
description: Write or evolve a ghost library's behavioral specification, including examples, edge cases, language mappings, and compatibility impact. Use when defining or changing a contract rather than generating its implementation.
---

# Write a behavioral contract

Read [contract rules](../../references/contract-rules.md) and [compatibility](../../references/compatibility.md). Preserve the target library's conventions. For a new spec without a local format, adapt [the spec template](../../templates/spec.md).

## Work

1. Read the existing spec, relevant fixtures, conventions, installation instructions, and user-requested behavior. Establish the public API and what is outside scope. Use the user's explicit choices; do not replace them with a reference library's design.
2. Identify decisions that affect externally visible behavior: accepted representations, defaults, null/missing values, Unicode units, order, boundary rounding, detectable errors, environment inputs, dependencies, and allowed language variation. Specify only those relevant to the domain. Ask for a missing decision when different answers change required behavior; continue independent work while it is pending.
3. Write observable rules and examples. Specify an algorithm only when it determines required output or another observable guarantee. Language-specific names and error idioms may differ when the mapping preserves the contract. Make permitted variation explicit rather than leaving accidental gaps.
4. Update affected fixtures and generation guidance with the spec. Use [fixture profiles](../../references/fixture-profiles.md) when fixture meaning is involved. Derive expected values independently; if the request is fixture-heavy, follow the `ghost-tests` workflow when it is available, or perform its rule-to-case reasoning directly.
5. Review the diff as a consumer: which previously conforming inputs or implementations behave differently? Explain compatibility and whether a clarification narrows formerly allowed behavior. Do not automatically call every prose correction a patch release.

## Output and completion

Deliver a coherent spec patch with examples, affected fixture changes, compatibility impact, and unresolved decisions. Existing spec/fixture disagreements must be surfaced; do not silently choose a winner to make a patch pass. An explicit user decision can resolve them.

Complete when the requested behavior is implementable without guessing, affected examples and fixtures agree, and the compatibility assessment cites the changed rules. Mark drafts with unresolved behavior as drafts. Keep implementation code outside the contract repository unless the user specifically requests otherwise.
