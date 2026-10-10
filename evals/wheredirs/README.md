# wheredirs profile evaluation

Source: [wheredirs at 7c83fe3e](https://github.com/hasansezertasan/wheredirs/tree/7c83fe3e04be50144099eba87d01c36617f404c5). A native Codex `ghost-verify` invocation generated a downstream Python implementation and runner in a disposable consumer directory, using [this request](request.txt). The supplied contract files remained unchanged.

The generated runner passed all 155 original records and 161 assertions, including six required runtime-fallback warning observations. Its six negative controls passed their intended rejection checks. An independent evaluator in this repository checked the same implementation against those 155 records and [11 additional observations](observations.yaml): nine warning-presence/absence cases and two absent-environment error cases. It passed all 166 records and 15 warning assertions. Ten independent fault controls were detected.

The first environment fault unexpectedly passed: original fixtures covered empty `HOME`, but no otherwise-valid XDG call with an absent `HOME`. Two cases with empty environment maps were added for XDG and Windows to distinguish missing variables from empty ones. The fault then failed for the intended required-error reason. This evidence informed the shared [harness guidance](../../.ai-rulez/references/harness-contract.md).

## Reproduce

Clone the pinned source into an isolated workspace's `contract/` directory. Invoke `ghost-verify` with [request.txt](request.txt); generated files belong in its sibling `consumer/` directory. Do not provide assessment results or fault expectations to the generating agent. The recorded native run used existing cached Python/PyYAML directly after uv's cache write was blocked, without installing dependencies.

From this toolkit checkout, run the independent checks against that generated module:

```sh
uv run --with pyyaml python evals/wheredirs/run.py \
  --fixtures /absolute/path/to/workspace/contract/tests.yaml \
  --observations evals/wheredirs/observations.yaml \
  --implementation /absolute/path/to/workspace/consumer/wheredirs.py \
  --report /tmp/wheredirs-conformance.json

uv run --with pyyaml python evals/wheredirs/controls.py \
  --fixtures /absolute/path/to/workspace/contract/tests.yaml \
  --observations evals/wheredirs/observations.yaml \
  --implementation /absolute/path/to/workspace/consumer/wheredirs.py \
  --report /tmp/wheredirs-controls.json
```

The evaluator accepts exactly this profile: positional `which_strategy` calls, mapped directory arguments, explicit `_resolve(platform, env, function_name, args)` calls, path strings, null values, and detectable errors. It substitutes complete `$VAR` tokens once from the case's environment, retains unknown variables literally, and performs the contract's slash normalization only on paths. Strategy strings are compared exactly. It rejects unknown fields, duplicate IDs/keys, empty suites, and incomplete execution.

`warning: true` requires at least one Python `warnings` observation during that call; `false` requires none. Filters are set to `always` within each capture scope to observe repeated warnings. Message wording, warning category, and exact count are not constrained. Successful XDG runtime fallback calls also require a warning under INSTALL, even when the original record has no warning field. Absence/error observations and supplemental warning fields are local evaluation data, not an upstream schema migration.

The evaluator copies each argument/environment map and detects input or process-state mutation. It never writes the host's environment. The leakage fault uses a synthetic `/ambient-sentinel` default in a temporary implementation. Other faults cover bad expectations/returns, swallowed errors, null-as-empty, missing/spurious warnings, unknown assertions, empty suites, and duplicate YAML keys.

## Evidence and scope

Saved [results](../results/wheredirs/README.md) identify the pinned source, Python runtime, fixture/module/harness hashes, case-level observations, and negative controls. Generated implementation and runner code remain disposable consumer artifacts.

This establishes finite-fixture Python conformance across synthetic XDG, Apple, Windows, and single-folder inputs. It does not execute real Windows/Linux integrations or certify every input. The generated runner additionally exercised 30 public-wrapper calls in a child process on the native macOS host; that evidence remains distinct from the portable explicit-input profile. No release was published or plugin installed.
