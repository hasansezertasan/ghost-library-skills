# Workflow evaluations

Structural checks validate skill names, frontmatter, and resource links. These evaluations exercise decisions: retaining error requirements, identifying contradictions, preserving allowed variation, and distinguishing fixture parsing from implementation conformance.

Run each scenario with the named skill and supplied artifacts in a fresh disposable workspace. For an independent agent evaluation, provide the request and raw artifacts without expected outcomes or prior findings. Delegation is optional and requires availability/authorization in the evaluating environment.

| Scenario | Skill | Evidence to assess |
| --- | --- | --- |
| [Initialization](scenarios/init.md) | `ghost-init` | Bounded scope, unresolved dialect choice, no invented compatibility |
| [Audit](scenarios/audit.md) | `ghost-audit` | Located contradiction, missed assertions, read-only behavior |
| [Specification change](scenarios/spec.md) | `ghost-spec` | Explicit code-point rule, boundary cases, compatibility assessment |
| [Invariant fixtures](scenarios/tests.md) | `ghost-tests` | Local seeded reproducibility, invariants, no invented cross-language stream |
| [Harness verification](scenarios/verify.md) | `ghost-verify` | Bad error handling detected, unsupported assertions visible, negative controls |
| [Bug diagnosis](scenarios/fix.md) | `ghost-fix` | Contract-preserving repair in the responsible layer |
| [Release preparation](scenarios/release.md) | `ghost-release` | Narrowed behavior recognized, preparation distinct from publication |

[Pilot evidence](pilot-evidence.md) records the initial direct review of three real repositories. It is not an independent agent evaluation or an implementation certification. Repeat realistic evaluations after changes that affect workflow decisions.

The subsequent [padlib maintenance evaluation](padlib/README.md) adds a generated downstream Python implementation, a profile-specific executable harness, seven negative controls, and an independent native Codex audit. Its saved results cover 117 cases in a disposable copy of a pinned source. [Host support](../docs/host-support.md) records native packaging/discovery and invocation limits.

The [native workflow suite](native/README.md) exercises the six remaining skills with isolated model trials and independent assessment: five clean passes and verification with an explicitly recorded reporting limitation. The [wheredirs evaluation](wheredirs/README.md) adds a real environment-dependent profile: 155 original cases, 11 additional observations, 15 warning assertions, and ten detected faults.

The [four-host installation suite](results/hosts/installation/README.md) checks discovery and resource replacement in private profiles. Its structural passes are separate from model invocation evidence.

The [repository packaging evaluation](results/hosts/repository/README.md) repeats installation/replacement directly from a checkout, validates root catalogs, and records OpenCode path resolution and configuration-guard scope.

The [automation evaluation](automation/README.md) tests raw ai-rulez output and simulates release-please version/changelog updates offline.
The [initial prototype decision](results/automation/README.md) is superseded by [the integration evaluation](results/automation/adoption/README.md),
which adopts native JSON generation with preserved local resource and drift checks.
