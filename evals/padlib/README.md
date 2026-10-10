# padlib maintenance evaluation

Date: 2026-10-05. Source: [padlib at 4c8ae4d](https://github.com/hasansezertasan/padlib/tree/4c8ae4d90de98126c63ed69ff54f6ce360b6ce3f). The implementing agent followed the spec, tests, verification, and repair guidance in a disposable copy. A separate native Codex `ghost-audit` call reviewed raw contract artifacts without receiving expected findings. This is one complete maintenance cycle; the seven skills have not all been individually model-invoked.

## Results

| Check | Result |
| --- | --- |
| Untouched original suite | 111/111 pass with the repaired Python implementation |
| Expanded isolated suite | 117 discovered, 117 executed, 117 passed; zero failed, skipped, or unsupported |
| Deliberate faults | All seven rejected with exit code 1 |
| Initial generated implementation | 115/116 passed; existing boolean fixture exposed `True` versus required `true` |
| Native Codex audit | Completed, loaded packaged resources, found a missing partial center-pattern case |
| Native Claude audit | Seven commands discovered; inference blocked by weekly usage limit |

The six added cases cover decomposed input/fill strings, code-point counting without normalization, odd center padding, and independently restarted partial patterns. Five Unicode cases were derived directly from the existing no-normalization rule. The sixth case, `center_pad("ab", 6, "xyz") == "xyabxy"`, was prompted by the native audit and already appears in the source specification. The isolated spec gained matching Unicode examples; README and INSTALL counts were updated. No behavioral rule or version changed.

The first generated implementation used ordinary Python boolean conversion. The existing fixture requires lowercase `true`, so the implementation was repaired; the fixture was retained. Remaining questions about portable `false` spelling and integer coercion are in the [audit response](../results/padlib/native-audit.md). No broader coercion policy was invented during this cycle.

## Saved evidence

- [Contract patch](../results/padlib/contract.patch): reviewable changes against the pinned source.
- [Final conformance report](../results/padlib/conformance.json): every case and fixture/implementation/harness SHA-256 identities.
- [Initial failing run](../results/padlib/baseline.json): the boolean conversion defect before repair, at 116 cases.
- [Negative controls](../results/padlib/negative-controls.json): wrong expectation, wrong return, swallowed error, unknown assertion, empty suite, duplicate YAML key, and continued center pattern.
- [Source identity](../results/padlib/identity.json): pinned revision, original-suite result, and original-source hash preservation.
- [Native audit response](../results/padlib/native-audit.md) and [host invocation summary](../results/hosts/invocation.json).

The original clone remained unchanged. Generated library and fault implementations are disposable artifacts, not toolkit source. Saved hashes identify the implementation that ran; to reproduce its exact bytes, retain that disposable file. Regenerating from the contract may produce a different conforming implementation.

## Reproduce

Create an isolated clone and apply the saved patch from this checkout:

```sh
git clone https://github.com/hasansezertasan/padlib /tmp/ghost-padlib-eval
git -C /tmp/ghost-padlib-eval checkout 4c8ae4d90de98126c63ed69ff54f6ce360b6ce3f
git -C /tmp/ghost-padlib-eval apply "$(pwd)/evals/results/padlib/contract.patch"
```

Ask your agent to read `skills/ghost-verify/SKILL.md`, generate all five Python functions from that isolated SPEC and INSTALL, and save the module outside the contract directory. Substitute its path below:

```sh
uv run --with pyyaml python evals/padlib/run.py \
  --fixtures /tmp/ghost-padlib-eval/tests.yaml \
  --implementation /absolute/path/to/generated/padlib.py \
  --report /tmp/padlib-conformance.json

uv run --with pyyaml python evals/padlib/controls.py \
  --fixtures /tmp/ghost-padlib-eval/tests.yaml \
  --implementation /absolute/path/to/generated/padlib.py \
  --report /tmp/padlib-negative-controls.json
```

`run.py` implements padlib's profile, not a universal ghost-library format. It inventories declared case lists, treats nested arguments as data, compares type and output exactly, requires error cases to raise, and rejects unknown assertions and duplicate YAML keys/IDs. Empty, incomplete, unsupported, or failing suites exit nonzero. Reports identify the Python runtime and input hashes. PyYAML is the only added dependency; it is needed to run the evaluation, not to use the skills.

`controls.py` first requires a passing baseline, then corrupts fixtures or appends deliberately faulty function overrides in temporary files. It tests all seven faults against the supplied implementation and saves compact results. It is intended for this expanded padlib profile, including the partial center-pattern regression.

Native host reproduction commands are in [host support](../../docs/host-support.md). The independent audit ran against the intermediate 116-case contract; its finding led to the final 117th fixture. It correctly reported that it had not executed an implementation and could not fully parse YAML in its read-only environment.

## Scope

The result establishes finite-fixture conformance for one generated Python implementation and this patched contract. It does not establish every untested input, another language, an installed plugin upgrade, or a public release. The audit's open contract questions still require maintainer decisions. Release preparation consists of the patch, counts, compatibility assessment, and reports here; nothing was published.
