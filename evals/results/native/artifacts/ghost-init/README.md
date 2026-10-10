# cronwords

A ghost library for describing cron expressions in English. This repository
distributes a behavioral contract and portable fixtures; consumers generate or
write an implementation in their own language and project.

**Status: draft.** The cron dialect has not been selected. No complete parser or
description contract is ready for implementation, and no cross-language
conformance has been demonstrated.

- [SPEC.md](SPEC.md) defines the proposed API, independent input rules, and the
  decisions needed to finish the contract.
- [fixtures/cases.json](fixtures/cases.json) contains required draft input-boundary
  cases and explicitly pending schedule cases.
- [fixtures/README.md](fixtures/README.md) explains fixture status and comparisons.
- [INSTALL.md](INSTALL.md) supplies a downstream generation prompt for use once
  the dialect and remaining grammar/rendering rules are finalized.

The proposed operation is `describe(expression)`, returning an English description
or a detectable error. For illustration only, a five-field profile might describe
`* * * * *` as `Every minute.` This example is pending the dialect decision.

cronwords describes schedule rules. It does not execute jobs, calculate upcoming
runs, resolve daylight-saving transitions, read crontab files, or provide other
languages. The intended consumers are applications and command-line tools that
display schedules; they own their generated code and integration.

The existing [LICENSE](LICENSE) is retained unchanged.
