# ai-rulez adoption evidence

This records the earlier staging-only integration.
The subsequent [authoring migration](../authoring/README.md) moves canonical sources into `.ai-rulez/`
and records checks for the new generated root skills.


Integration evaluated on 2026-10-05 with released ai-rulez `4.24.2`.
This supersedes the initial decision to retain hand-written host JSON schemas;
the [initial prototype](../README.md) remains a record of raw generator behavior.
See [the integration guide](../../../../docs/ai-rulez.md) for the actual staging and ownership boundaries.

## Decision

Adopt ai-rulez for native Claude/Codex manifests and both marketplace catalogs,
using its released marketplace/member configuration.
Retain canonical root skills, Pi metadata, OpenCode's native skill paths,
our portable resource builder, and strict checkout drift checks.
The fully owned member is generated in a fresh tree on every run,
which avoids publishing stale source deletions without changing upstream behavior.

## Evidence

| Check | Result |
| --- | --- |
| `make check-all`, Python 3.12 | 42 tests pass; all four disposable host bundles build. |
| [Native validation](validation.json) | Claude manifest/catalog validation passes; Codex registers and discovers all seven skills. |
| [Installation and replacement](installation.json) | All four hosts discover seven skills before and after replacement; versions, resource hashes, removed markers/files, and links pass. |
| Configuration guard | Final run passes with no changed guarded files or Claude keys; ignore list remains unchanged. |
| [Pi npm package inspection](pi-package.json) | 27 files: seven skills with display metadata, five shared references, six templates, README, and package metadata; no tooling/governance files. |
| [Release-please strategy](release-please.json) | First release, patch, feature, and pre-1.0 breaking changes pass; Pi fields and new development/display metadata survive. |
| Workflow syntax | actionlint `1.7.12` accepts updated check and release workflows. |

The two new integration regressions check canonical skill deletion and Codex display changes.
Existing packaging tests retain changed/missing/extra detection, symlink rejection,
source preservation, independent resource portability, and version regeneration.
Both catalogs now point to `./plugins/ghost-library`;
that directory contains both native host manifests and plain self-contained skills.
Pi and OpenCode continue using the canonical root skills and shared resources.

The [preliminary installation run](preliminary-installation.json) passed all host payload checks,
but the real-configuration guard detected changing Claude tip-history metadata.
A separate [background observation](background-observation.json), with no host commands running,
also detected Claude metadata changes.
The repeat run passed the original guard without adding ignored fields.
The preliminary data is retained rather than reclassified as a complete pass.

Native versions are Claude `2.1.289`, Codex `0.160.0`, OpenCode `1.18.34`, and Pi `1.0.1`.
Codex installation uses the same official Linux arm64 musl binary in a network-disabled container;
the report records its binary hash and container image.
Private host profiles were used, no model inference was requested,
and the temporary container was removed after evaluation.

## Maintenance comparison

The 24-line custom native JSON constructor is removed.
ai-rulez now owns the output schemas for both manifests and both catalogs.
Codex UI choices are authored under `package.json`'s `ghostLibrary.interface`,
and shared descriptions/author identity are derived rather than copied into another authored config.

The synchronizer and bundle builder grow from 235 to 277 Python lines,
an increase of 42 lines for staged configuration derivation, tool invocation, and verification.
One pinned npm development dependency and a lockfile are added;
the resource builder remains.
Adoption delegates host schema maintenance upstream,
but does not reduce total custom Python line count or eliminate the wrapper.

The raw generator's permissive extra-file handling and stale-file retention are handled locally,
while OpenCode package generation remains disabled in the Pi authoring tree.
This makes the integration compatible with existing packaging requirements without relying on unreleased ai-rulez features.

## Limits and reproduction

Use `make sync` and `make check-all` with Node/npm and Python installed.
The Makefile installs locked tooling when needed.
Repeat native validation with `tools/smoke_plugins.py --repository .`,
and repeat installation using the documented private-profile command in [host support](../../../../docs/host-support.md).

Full temporary profiles and installation data remain at `/private/var/folders/vj/26z0937x6zg3hvq02p8v6nfw0000gn/T/ghost-automation-i2lx7r0l/adoption-installation-final`.
This checkout has not been published;
GitHub workflow execution and installation from a remote release tag remain untested.
No new model-workflow, Hermes, or Antigravity support claim follows from these packaging checks.
