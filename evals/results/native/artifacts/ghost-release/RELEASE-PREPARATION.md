# Contract release preparation

## Identity and version recommendation

**Recommend contract version 2.0.0 under SemVer**, from current version 1.2.0
([VERSION](VERSION)). Status: prepared draft for review; conformance is unverified.
The library name and source commits were not supplied. The comparison scope is
[old.md, line 1](old.md) to [new.md, line 1](new.md), for `map_keys` ordering only.
No additional release policy or conventions are present in the supplied workspace.

This change removes output orders that were explicitly permitted by 1.2.0.
A previously conforming implementation may therefore fail the new contract.
An unchanged API name does not make an observable ordering change compatible.
The maintainer's description of this as a clarification does not support a patch
or minor release. A major release is appropriate even if some implementations
already return lexicographic order.

The proposed version is the library contract version. No plugin/toolkit or
fixture-schema version change is proposed; their identities were not supplied.
`VERSION` remains 1.2.0 pending release review. Source inputs are preserved.

Source content identities (SHA-256; no commit identity available):

| Artifact | SHA-256 |
| --- | --- |
| `old.md` | `a956335000ccdda5d7b5edbbd27489700a68a86e1feba465c91351620bce23b0` |
| `new.md` | `93d868b076c7518c2bdaf6edcadf3eaace0f244922b58bb85999d43158872c94` |
| `maintainer-note.txt` | `60bd12c728abd46edc95d247f0ae856c86a5f836dc11a0f9335e62a843dd4a95` |
| `VERSION` | `1e5b51cde515396a9fa762909cf8ca6584ccc564b325d2eebeea76175fe95c4d` |

## Behavioral changes

| Surface | 1.2.0 (`old.md:1`) | Proposed 2.0.0 (`new.md:1`) | Classification and impact |
| --- | --- | --- | --- |
| `map_keys` output order | Implementation-defined | Lexicographic | Breaking: formerly permitted outputs can now be rejected. |

Illustrative example using distinct lowercase ASCII keys: for a map containing
`b` and `a`, an implementation could validly return `["b", "a"]` under 1.2.0.
The proposed contract requires `["a", "b"]`. This example illustrates the
ordering change; it is not an executed fixture or a definition of supported key
types. An implementation already returning `["a", "b"]` needs no change for this
input, but that alone does not establish conformance.

The two texts retain the same API name. They provide no other API shape,
accepted-input, default, error, mutation, dependency, or fixture-format rules to
compare. No additive feature or behavior-preserving documentation correction is
shown. The reported new fixtures are not available for inspection; fixtures
enforcing lexicographic ordering would enforce this new constraint, rather than
merely add coverage of the old ordering rule.

### Proposed release notes — 2.0.0

- **Breaking:** `map_keys` now returns keys in lexicographic order. Version 1.2.0
  permitted implementation-defined order.
- Implementations must enforce the agreed lexicographic comparison rule.
  Callers must review assumptions about iteration order, first/last keys,
  snapshots, and serialized key lists.
- Available evidence is a maintainer-reported pass of the new fixtures by one
  Python implementation. No other evaluation is reported. Cross-language
  conformance has not been established.

## Migration

1. Define the portable comparison rule before finalizing implementation changes
   or fixture expectations. Do not silently substitute a runtime's default sort.
2. Update implementations that return insertion order or another permitted 1.2.0
   order to return lexicographically ordered keys under that agreed rule.
3. Review caller behavior that depends on returned order. For the example above,
   update expected key lists from `["b", "a"]` to `["a", "b"]`. If callers need
   their prior ordering, maintain that ordering explicitly in caller-owned code.
4. Keep consumer-local ordering extensions separate from the upstream contract;
   an extension returning another order does not conform to the proposed rule.
5. Run the identified fixtures and ordering assertions for each implementation
   claimed to conform. Cover an output accepted in 1.2.0 but rejected in 2.0.0,
   plus the edge cases selected by the comparison decision. Record complete case
   accounting and harness evidence.

## Evidence

The only implementation evidence is [maintainer-note.txt, line 2](maintainer-note.txt):
one Python implementation reportedly passes the new fixtures, with no other
evaluation. This is a reported result, not an independently verified run.

| Evidence dimension | Available information / limitation |
| --- | --- |
| Contract source | Local old/new texts identified by hashes above; the reported run is not bound to either hash or a source commit. |
| Domain | This release comparison concerns `map_keys`; evaluated domain/suite scope is unspecified. |
| Language / implementation | Python; implementation identity and revision absent. |
| Runtime / environment | Python version, platform, locale, and other relevant environment details absent. |
| Fixtures / comparison profile | New fixtures mentioned but not supplied; identity, schema/profile, expected outputs, coverage, and ordering assertions cannot be inspected. |
| Harness | Identity/revision, API mapping, comparison semantics, and negative-control evidence absent. |
| Commands / reports | No execution command or run report supplied. |
| Accounting | Case counts and failed, skipped, or unsupported statuses absent; do not infer zero skips or complete assertion execution. |
| Other languages | No evaluation reported; no broader support or conformance claim is justified. |

Preparation checks: inspected all four supplied artifacts, compared the full
texts with `diff -u old.md new.md`, confirmed `VERSION` is 1.2.0, and recorded
content identities using `shasum -a 256 VERSION old.md new.md maintainer-note.txt`.
No implementation or harness is present to execute conformance checks.

Documentation reconciliation: the proposed release notes and migration guidance
consistently identify 2.0.0 as proposed and 1.2.0 as current. The example reflects
the new ordering. No installation guidance, external artifact links, existing
changelog, or fixture counts were supplied to reconcile. Before release, bind
the final contract, fixtures, version references, and applicable downstream
guidance to the reviewed target revision.

## Outstanding decisions and publication

- **Maintainer decision:** define what “lexicographic” means for supported keys:
  key types, comparison units, case sensitivity, normalization, locale behavior,
  and any tie rules that apply. Neither supplied contract defines these details.
  This draft does not choose them. Selecting a comparator may require further
  contract/fixture review and migration examples.
- Resolve the maintainer note's compatibility characterization: the supplied
  old rule explicitly permits the outputs now excluded. If this behavior change
  is retained, release it as 2.0.0 under SemVer. Keeping 1.x compatibility would
  require a different target contract, such as a separately additive operation;
  that is outside this preparation's scope.
- Obtain the fixture artifacts and a reproducible report bound to the final
  contract, implementation, runtime, and harness identities. Verify required
  ordering assertions and complete case accounting, including skips and
  unsupported cases. Additional language claims require corresponding evidence.

Release preparation is complete as a reviewable draft with explicit limitations;
it is not a verified release. Final contract review and conformance evidence
remain outstanding. No tag, commit, push, or publication was performed.
