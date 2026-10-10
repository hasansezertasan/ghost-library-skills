# Native workflow evaluations

The scenarios in [cases.json](cases.json) exercise the workflows that had only been structurally checked: six from the initial plugin pilot and five later skills. Each receives raw artifacts and an explicit native skill input through Codex's app-server. The acceptance criteria remain outside the agent workspace, in the [scenario descriptions](../README.md).

| Skill | Capability to assess |
| --- | --- |
| `ghost-init` | Draft independent work while leaving the cron dialect unresolved; preserve the existing license |
| `ghost-spec` | Make a code-point change observable in fixtures and explain its breaking impact |
| `ghost-tests` | Preserve invariants, cover duplicates/non-mutation/replay, and document assertion semantics |
| `ghost-verify` | Reject incomplete runner evidence and distinguish a missing error assertion from a pass |
| `ghost-fix` | Reproduce the UTF-16 bug, add a regression before repair, and preserve the upstream contract |
| `ghost-release` | Recognize that constrained ordering breaks previously conforming implementations; scope evidence and prepare without publishing |
| `ghost-summon` | Map errors before generating, account for every case, and record a content-identity receipt |
| `ghost-evaluate` | Isolate cells, attribute the astral-character failure to an ambiguous contract word, and propose rather than apply a fix |
| `ghost-extract` | Classify ASCII-only and locale behavior instead of copying it, and retain attribution |
| `ghost-upgrade` | Surface the conflict between the new fill rule and the local extension, and notice the existing truncation bug |
| `ghost-catalog` | Flag the missing license and instructions, the 50-versus-41 count drift, and overstated claims without editing |

## Reproduce

With Codex installed and authenticated, run from this checkout:

```sh
python3 tools/run_workflow_evals.py --output /tmp/ghost-workflow-evaluation
```

The output path must be new and outside this repository. To select a single scenario:

```sh
python3 tools/run_workflow_evals.py --output /tmp/ghost-fix-evaluation --case ghost-fix
```

This uses the existing host configuration and model allowance. It builds fresh plugins, creates independent workspaces, sets discovery roots only in a private subprocess, and invokes one ephemeral model turn per selected scenario. The model is not overridden; the resolved model ID is recorded. The verification and catalog scenarios use a read-only sandbox; the others may edit their own disposable workspace. Requests prohibit network, MCP, subagents, host-setting changes, and publication. No expected findings are supplied.

Each result includes the final response, command/file-change events, model ID, duration, and before/after hashes. A 600-second default timeout limits each turn; `--timeout` can change it. A native `completed` status establishes only that the model turn completed. The runner does not automatically grade task semantics.

## Assessment

Review complete trajectories and resulting files against the scenario criteria. Independently parse fixture data, derive code-point prefixes, execute repair probes, compare protected-file hashes, and distinguish observed checks from generated claims. A missing decision correctly retained as a draft can satisfy an evaluation without completing that library's design.

Saved evidence and the assessment of the recorded runs are in [results](../results/native/README.md); those runs cover the original six scenarios only. These are single trials of small adversarial scenarios, not reliability estimates or a general benchmark. The larger [wheredirs evaluation](../wheredirs/README.md) exercises generation, environment injection, warnings, null/error distinctions, and complete accounting against a real repository.
