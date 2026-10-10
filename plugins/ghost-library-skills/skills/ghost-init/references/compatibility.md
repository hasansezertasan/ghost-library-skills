# Compatibility and versioning

Follow the library's declared version policy. Assess behavior before recommending a version; a filename, prose edit, or unchanged function name does not establish compatibility.

| Change | Questions to answer |
| --- | --- |
| Documentation correction | Does it merely describe behavior already required, or remove a previously plausible interpretation? |
| Added fixture | Does it cover an existing rule, or introduce a new constraint that previously conforming code can fail? |
| Error change | Are accepted inputs, failure detection, error category, or required messages different? |
| API/default/output change | Can an existing caller or previously conforming implementation observe a difference? |
| New function/domain | Is it independent and additive, or does it change shared conventions or existing guarantees? |
| Comparison/profile change | Are formerly accepted outputs now rejected, or is the case encoding/harness incompatible? |
| Dependency/platform policy | Are consumers required to add packages or run in different environments? |

With SemVer, breaking contract changes usually warrant a major release; compatible additions a minor release; corrections preserving required behavior a patch release. Draft/pre-1.0 policies may differ. Explain the recommendation rather than enforcing SemVer on a library that uses another policy.

A bug fix can still break callers relying on old behavior. A clarification can narrow an ambiguous contract. A corrected fixture can invalidate generated implementations. Report these effects and provide input/output examples and targeted migration steps.

Keep four identities distinct: plugin/toolkit version, library contract version, fixture schema version, and source commit/content identity. A downstream receipt can record source identity, selected domain, hashes, generated paths, language mapping, and verification command/report without requiring a central package registry.

Release evidence names the evaluated contract, domains, languages, environments, harness identity, and skips/unsupported cases. Do not extrapolate a passing Python implementation to all languages or confuse fixture coverage with behavior coverage. Preparing release notes does not itself publish a release.
