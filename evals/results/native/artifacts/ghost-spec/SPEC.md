# fit(s, limit)

Status: draft pending the isolated-surrogate input policy described below.
Code-point counting and preservation without normalization are decided.

## Behavior

`s` is a string. `limit` is a nonnegative integer.

Count Unicode code points, not UTF-16 code units, bytes, grapheme clusters,
or display columns. If the code-point count exceeds `limit`, return the
prefix containing the first `limit` code points. Otherwise return `s`
unchanged. A zero limit returns the empty string.

Never normalize strings, either before counting or when returning a result.
Preserve the exact code-point sequence of the selected prefix or unchanged
input. Canonically equivalent strings can therefore have different counts
and results. Do not compose, decompose, replace, or reorder code points.

A supplementary character such as U+1F600 (😀) counts as one code point.
In a UTF-16 representation, its surrogate pair must be kept intact.
Combining marks and zero-width joiners each count separately. A returned
prefix may end within a grapheme cluster.

## Examples

In the table, `\uXXXX` denotes one code point and is explanatory notation,
not literal backslash text in the input or output.

| Input | Limit | Output | Reason |
| --- | --- | --- | --- |
| `abc` | 2 | `ab` | ASCII code points each count once. |
| `😀x` | 1 | `😀` | A supplementary character counts once. |
| `😀x` | 2 | `😀x` | The input has two code points. |
| `e\u0301x` | 1 | `e` | The combining acute accent is a separate code point. |
| `e\u0301x` | 2 | `e\u0301` | The decomposed sequence stays decomposed. |
| `\u00E9x` | 1 | `\u00E9` | The composed character stays composed. |
| `👩\u200D💻` | 2 | `👩\u200D` | The joiner counts, even within one displayed grapheme. |
| `😀` | 0 | empty string | No code points are selected. |

## Language mapping and fixtures

Use a language-native string API that iterates code points. Native string
length and slicing are suitable only if they obey these rules; UTF-16
code-unit length and slicing alone do not. Do not normalize as part of
input decoding, fitting, or output comparison.

`tests.yaml` uses the existing `fit` group with named cases, positional
`input: [s, limit]` arguments, and an exact string `output`. Double-quoted
YAML Unicode escapes encode actual code points. Compare output code-point
sequences exactly, without normalization or grapheme-based comparison.

## Compatibility

This intentionally replaces the UTF-16 code-unit counting and prefix rules.
It is a breaking contract change despite the unchanged function signature
and fixture format. For example, `fit("😀x", 2)` previously returned `"😀"`
and now returns `"😀x"`. At limit 1, the old rule selected only the leading
surrogate; the new rule returns the complete `"😀"` character.

Inputs containing only BMP scalar values have the same counting and prefix
results. The no-normalization rule makes the existing exact-prefix and
unchanged-input guarantees explicit. Composed
`"\u00E9x"` and decomposed `"e\u0301x"` at limit 1 must return
`"\u00E9"` and `"e"`, respectively.

Downstream implementations must replace code-unit counting and slicing
with code-point operations, preserve source text exactly, and rerun the
updated fixtures. Callers must express limits in code points and review
assumptions about UTF-16 output sizes. No version policy is declared here;
under SemVer this change would require a major contract release. This patch
does not assign or publish a release or change the fixture schema.

## Unresolved input policy

The previous contract did not specify whether strings containing isolated
UTF-16 surrogates are accepted. These are not Unicode scalar values, and
language runtimes differ in whether they can represent them. The rules and
fixtures above cover strings of Unicode scalar values. A maintainer decision
is still needed: reject isolated surrogates, or accept and preserve each as
one counted code point where representable, with a documented cross-language
mapping. This patch does not silently choose either behavior or introduce
an error category. Handling of other invalid input types and invalid limits
also remains outside the existing contract.
