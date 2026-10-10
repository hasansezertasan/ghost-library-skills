---
name: ghost-init
description: Create a ghost library or independent domain from an idea by defining a bounded API, behavioral specification, portable fixtures, and generation instructions. Use for new contract repositories, not implementation scaffolding.
---

# Start a ghost library

Read [philosophy](../../references/philosophy.md) and [contract rules](../../references/contract-rules.md). For an existing multi-domain repo, read its conventions before choosing a layout.

## Work

1. Establish purpose, target path, consumers, and scope. Assess whether observable behavior can be specified and tested with the available resources. Discuss relevant performance, external-data freshness, support, or platform constraints; these are design decisions, not blanket reasons to reject a ghost library.
2. Define the smallest coherent public API, accepted input/output representations, exclusions, dependency policy, and required external state. Ask only about unresolved choices that materially affect the contract. Preserve a user-specified API or layout.
3. Write `SPEC.md` using local conventions or [the spec template](../../templates/spec.md). Include defaults, meaningful boundaries, errors, and permitted variation. Use [fixture profiles](../../references/fixture-profiles.md) to create initial fixtures that distinguish wrong behavior rather than merely repeat happy-path examples.
4. Add concise generation instructions: read the contract and fixture conventions, generate into the consumer-selected language/location, execute all required cases, report unsupported assertions, and retain the source revision. Use [the install template](../../templates/install.md) as a starting point. Explain the library and its exclusions in the README; for a new domain, update its parent's domain index instead.
5. Reconcile examples, fixtures, instructions, and API scope. Do not claim cross-language verification from a draft spec. Preserve an existing license; for a new repo, obtain a license choice before adding one rather than assigning it automatically.

## Output and completion

Deliver a bounded contract, initial fixtures, generation instructions, and a short account of remaining decisions. A partial design with unresolved required behavior is a draft. No implementation or host configuration is needed to complete initialization.
