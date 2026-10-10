# Initial pilot evidence

Date: 2026-10-05. Method: direct execution/review by the implementing agent, not an independent agent evaluation. Original clones were left unchanged. No downstream implementation was generated or certified.

This is the initial pilot record. The later [padlib maintenance evaluation](padlib/README.md) supplies executable conformance and negative-control evidence plus an independent native audit.

## Source identity and inventory

| Scope | Source commit | Recognized case records |
| --- | --- | --- |
| `padlib` | `4c8ae4d90de98126c63ed69ff54f6ce360b6ce3f` | 111 |
| `stdlib/numbers` | `a05efdd20f99fcc2fe51dc444d16fef8b553b08f` | 32 |
| `wheredirs` | `7c83fe3e04be50144099eba87d01c36617f404c5` | 155 |

Inputs came from temporary research clones at the commits listed above; [the initial design record](../docs/decisions/0001-initial-design.md) describes that research. YAML was parsed with PyYAML via `uv run --with pyyaml python`. Case records were counted at their declared list containers, without descending into arguments or expected arrays. `padlib` includes nested Unicode/error groups; `wheredirs` uses top-level environment/strategy groups. Named case IDs were unique within each list container. The `numbers` fixtures are unnamed and identified by group/index.

`padlib` group counts: left 26, right 13, center 16, general pad 12, zero pad 22, Unicode 11, errors 11. `wheredirs` group counts: strategy picker 13, XDG 45, Apple 26, Windows 26, single-folder 14, errors 23, consumer project cases 8.

## Audit findings and scope limits

### padlib: numerical representation needs a deliberate portability policy

[`SPEC.md`, zero_pad edge cases](https://github.com/hasansezertasan/padlib/blob/4c8ae4d90de98126c63ed69ff54f6ce360b6ce3f/SPEC.md) permits language-default numeric string conversion. That can yield different spellings for otherwise equivalent numeric inputs. This is a portability question, not proof of a violated requirement: retain the permitted variation or deliberately standardize it with compatibility notes.

`SPEC.md`'s Unicode Handling section explicitly prohibits normalization. The reviewed Unicode cases cover astral emoji but contain no decomposed combining-accent case. This is a concrete coverage gap rather than a need to change the code-point contract.

### stdlib/numbers: optional tolerances lack direct coverage

[`numbers/SPEC.md`, is_close](https://github.com/hasansezertasan/stdlib/blob/a05efdd20f99fcc2fe51dc444d16fef8b553b08f/numbers/SPEC.md) defines optional relative and absolute tolerances. All five existing `is_close` records supply only two arguments. They test defaults but leave explicit optional-argument mapping and absolute tolerance uncovered.

The shared `CONVENTIONS.md` float comparison tolerance is a harness rule; it is not the default arguments of the public `is_close` function. A runner should compare boolean expectations exactly and should not use the candidate `is_close` implementation as its own float-comparison oracle.

### wheredirs: generation authority and warning assertions

[`INSTALL.md`, quick-start prompt](https://github.com/hasansezertasan/wheredirs/blob/7c83fe3e04be50144099eba87d01c36617f404c5/INSTALL.md) combines “YAML case wins” with “stop on a real contradiction.” This needs clarification if a conflicting case appears; the pilot did not invent a conflict or rewrite precedence.

`SPEC.md`'s XDG runtime fallback guidance and the install prompt call for warning behavior. Existing fixtures assert return values/errors but do not encode an expected warning observation. The return-path cases alone cannot establish that additional observable behavior. A warning assertion needs defined capture semantics or separately recorded runner evidence.

The specified placeholder substitution and path normalization are specific to this contract. Do not generalize them to every fixture profile. `null` results and `raises` cases remain distinct, including in Go-style error-result mappings.

## Spec and fixture pilot changes

All pilot changes were made in disposable copies at:

`/var/folders/vj/26z0937x6zg3hvq02p8v6nfw0000gn/T/ghost-library-pilot-jr49a2oe`

The temporary `evidence.json` records scope and counts. The paths are session artifacts, not required repository resources.

| Source rule | Pilot case | Derivation | Result |
| --- | --- | --- | --- |
| `padlib`: code points, no normalization | `left_pad("cafe\u0301", 6)` gives `" cafe\u0301"` | Input has five code points; exactly one space is needed | Parsed added case; Unicode representation retained |
| `numbers.is_close`: explicit absolute tolerance | `(0, 0.0005, 0, 0.001)` gives true | Difference is below absolute threshold | Formula agrees with expectation |
| `numbers.is_close`: absolute-tolerance failure | `(0, 0.002, 0, 0.001)` gives false | Difference exceeds threshold | Formula agrees with expectation |
| `numbers.is_close`: explicit relative tolerance | `(1, 1.001, 0.01, 0)` gives true | Difference is below relative threshold | Formula agrees with expectation |

The `numbers` draft spec gained matching examples; its fixture count became 35. Its rule already required this behavior, so adding these examples/cases does not introduce a new behavioral requirement. The `padlib` fixture copy gained one decomposed-accent case without changing its spec. Both changes preserved the existing profile.

These checks establish fixture syntax and independent expectation reasoning, not implementation conformance. They show why the skills distinguish case counts, rule coverage, and executable harness evidence. Executable negative-control behavior remains to be evaluated with a downstream implementation/harness or the dedicated [verification scenario](scenarios/verify.md).

## Structural and packaging validation

Run the commands in the repository README to repeat resource-link validation and packaging tests. The skill-creator validator was used for all seven source skills, and their Codex display metadata was parsed and checked for required display lengths and skill-name prompts.

The packaging tests relocate each built skill independently, resolve its local references/templates, reject missing and escaping resources, preserve nonempty consumer output, and reject a source directory as a build destination. These checks cover file portability, not host discovery or native plugin installation.
