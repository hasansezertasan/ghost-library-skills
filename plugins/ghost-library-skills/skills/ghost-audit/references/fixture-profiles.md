# Fixture profiles

Discover the declared schema before counting or translating cases. The profiles below describe common patterns, not a mandatory new file format. A repository may combine several profiles.

## Function cases

Common examples:

```yaml
left_pad:
  - name: basic
    input: ["x", 3]
    output: "  x"
```

```yaml
chunk:
  - {input: [[1, 2, 3], 2], expected: [[1, 2], [3]]}
chunk_errors:
  - {input: [[1], 0]}
```

`input` may be one argument, a positional list, or a keyword map. A list-valued unary argument must not accidentally be expanded into multiple arguments. Map fixture fields to signatures using the spec/conventions, including omitted optional arguments. Metadata such as `version` is not a function group.

Errors may use `raises: true`, an `error` field, or a separate error group. The declared convention determines whether the runner checks detectable failure, category, or message. Preserve it when translating language idioms.

## Structured parsing

A record may contain one input and assertions on several API calls or nested fields. For example, `ualib`'s `tests` records assert `parse` results and four classification predicates. Count one case record with multiple assertions; a case passes only when all required assertions pass. Specify missing versus null fields, sequence order, extra-field policy, and exact or tolerant comparisons.

## Environment-driven functions

Cases can name a function, arguments, platform/strategy, and an environment map. Treat undeclared environment variables according to the local convention, not the host's ambient state. Inject a pure resolver or use isolated subprocess environments; avoid shared process mutations that create parallel-test leakage.

`wheredirs` distinguishes list arguments for `which_strategy` from keyword-map arguments for directory resolvers. It substitutes only declared `$VAR` names in expected outputs, longest names first, leaves unknown placeholders literal, and normalizes separators/repeated/trailing slashes as documented. Those are `wheredirs` rules, not general string or path comparison defaults. Its public API and pinned internal resolver both need an explicit mapping.

## Named scenarios and callables

YAML cannot carry executable functions. A scenario or named helper must define concrete operations and observable outcomes. For a combinator, this can include helper definitions, application order, and underlying invocation counts. Never evaluate arbitrary fixture text as code. Implement a documented finite helper/scenario table and report unknown names as unsupported.

## Process and state scenarios

Define setup, actions, expected observations, and cleanup. Free-form setup prose can require clarification or explicit harness support. A command string alone is not an executable test if its repository, filesystem, services, or binaries do not exist.

Use disposable roots and controlled subprocess/network inputs. Assert specified exit codes, output, created artifacts, state transitions, and cleanup. Do not run fixture commands against real user repositories or install tools globally merely to interpret a scenario. If a realistic integration needs external resources beyond the user's authorized scope, report what is needed and continue isolated checks.

## Invariants and statistical checks

Specify properties such as membership, non-mutation, multiset preservation, or reproducibility. For statistical tests, define seed construction, trials, thresholds, and the intended distribution. Record the remaining probabilistic failure risk rather than tuning thresholds after seeing a failing candidate.

`stdlib/random` promises repeatable streams within one implementation, not identical streams across languages. Its cases therefore use invariants and seeded local reproducibility. Exact cross-language outputs are appropriate only when the contract fixes the algorithm and representation.

## Inventory and identity

Count records in recognized case containers, not every list recursively. Inputs, expected lists, setup steps, and action sequences are not additional cases. Reject duplicate IDs within their defined scope. Existing unnamed cases may use file/group/index identifiers; record their sensitivity to insertion/reordering rather than silently migrating a schema.

Keep unknown groups and assertion fields visible. Determine whether they are metadata or unsupported requirements before making a completeness claim. A skipped or unsupported case remains in the discovered total. New assertion semantics belong in the conventions/spec alongside the fixture.
