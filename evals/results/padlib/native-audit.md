# Native Codex audit response

This response audited the intermediate 116-case copy. Source locations refer to that disposable copy; Markdown links were rendered as inline code here. Its proposed center-pattern regression was subsequently added, bringing the final copy to 117 cases.

Reviewed `./contract` using `ghost-library:ghost-audit` and its packaged contract rules, fixture profiles, and harness rules. No files changed.

- **Ambiguous length validation:** `SPEC.md:267` permits an interpretation accepting values convertible to integers, while `tests.yaml:632` requires `5.5` to fail. Define whether conversion is allowed, including numeric strings, integral floats, booleans, and null; add distinguishing cases. Otherwise implementations can disagree on accepted inputs.

- **Boolean conversion is underspecified:** `SPEC.md:276` requires non-string inputs to be converted to strings, but `tests.yaml:142` specifically requires lowercase `"true"`. Python’s ordinary conversion produces `"True"`. Specify portable boolean spelling and add a `false` case so generation follows the fixture consistently.

- **Coverage gap for center-pattern truncation:** `SPEC.md:129` requires each side to restart its fill pattern independently. The center fixtures at `tests.yaml:277` use whole-pattern lengths, so they cannot distinguish restarting from continuing the pattern. Add the existing specification example `center_pad("ab", 6, "xyz") → "xyabxy"` as a fixture.

- **Verification claim lacks local evidence:** `README.md:27` says “Verified with Python,” but the supplied directory contains no implementation, runner, runtime identity, or result accounting. This remains an unverified claim in this audit. Link evidence demonstrating execution of nested Unicode groups and required error assertions.

- **Dependency claims exceed the stated policy:** `README.md:33` promises “No supply chain,” “No dependency conflicts,” and “No breaking changes,” while `INSTALL.md:10` leaves implementation dependencies unrestricted. State the dependency policy and qualify those guarantees.

**Checks and limits:** The record inventory matches all documented counts: **116 cases**, including 16 Unicode and 11 error cases. Decomposed-accent examples consistently follow code-point counting without normalization; specification and fixture versions both read `0.1.0`.

Reviewed the specification, fixtures, README, and generation instructions. No local agent instructions or Flow state directory were present; no Git revision was available. Full YAML parsing could not be completed because PyYAML was unavailable; counts came from named-record inventory. No implementation or conformance runner was executed, and external links were not checked.
