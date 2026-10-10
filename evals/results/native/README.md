# Native workflow results

The evaluations run the [six native scenarios](../../native/README.md) with independent artifact and trajectory assessment. A completed model turn is recorded separately from task success. Per-scenario evidence includes final responses, input/output hashes, command diagnostics, and reviewer checks.

Date: 2026-10-05. The recorded runs use Codex CLI 0.160.0 and the resolved model `gpt-6.1-sol`, with existing host configuration, one fresh workspace per trial, and no plugin installation. Each scenario had one initial trial; verification had a fresh recheck after guidance changes.

| Skill | Assessment | Main observed result |
| --- | --- | --- |
| `ghost-init` | Pass | Dialect left unresolved; 11 required draft input cases and 17 pending schedule cases; license preserved |
| `ghost-spec` | Pass | All 18 exact code-point expectations independently agree; compatibility marked breaking |
| `ghost-tests` | Pass | Nine invariant cases; duplicates, non-mutation, and two local stream replay cases; semantics documented |
| `ghost-verify` | Pass with reporting limitation | Correct rejection and immutable sources; recheck provides aggregate controls, but one separately claimed command lacks an individual completed trace |
| `ghost-fix` | Pass | Three regression failures before repair; nine native tests and six independent probes pass afterward |
| `ghost-release` | Pass | Major-version recommendation, migration notes, reported-only Python evidence, and unresolved comparator policy |

[Assessment](assessment.json) separates evidence from model claims. [Independent checks](independent-checks.json) record parser, expectation, preservation, and runtime probes. Per-skill JSON files preserve responses and condensed command/file-change events; `ghost-verify-recheck.json` also retains the full aggregate control output. [Identity](identity.json) records evaluated bundle hashes and disposable trace paths. Reviewable draft contracts, fixtures, and release notes are retained under `artifacts/`.

The initial verification report listed three commands as executed without completed-command evidence in the captured trace. The recheck, after stricter guidance, executed seven child control/baseline checks in one completed aggregate command, including the actual source's error-return defect. One separately claimed standalone command still lacks its own completed trace, so it is not certified as observed. This is a reporting/evidence limitation; it is not proof that the model fabricated results, since rejected calls can be absent from completed-command telemetry.

Native traces remain in the recorded disposable session paths; saved evidence is condensed rather than a complete conversation archive. These trials establish focused workflow behavior, not a general reliability rate. Design choices correctly left unresolved in the init/spec/release trials remain maintainer decisions.
