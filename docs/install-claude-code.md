# Installing ghost-library-skills on Claude Code

Per-host capabilities — what Claude loads and how skills are invoked — live in
[host-support.md](host-support.md). This page covers install only.

## Install

Use the absolute path to this repository. Consumers do not need to run the Python
builder first.

```sh
claude plugin marketplace add /absolute/path/to/ghost-library-skills
claude plugin install ghost-library-skills@ghost-library-skills-marketplace
```

For a session-local trial without registering the marketplace:

```sh
claude --plugin-dir /absolute/path/to/ghost-library-skills
```

GitHub-source installation becomes available after the manifests are committed and
published; it has not been tested against the current remote. Prefer a local checkout
until then. See [Claude plugins](https://code.claude.com/docs/en/plugins).

## Update

Refresh the checkout, then:

```sh
claude plugin marketplace update ghost-library-skills-marketplace
claude plugin update ghost-library-skills@ghost-library-skills-marketplace
```

Then **restart or reload plugins**. Skill descriptions are read at session start, so a
running session keeps the versions it started with.

## Invoke

```text
/ghost-library-skills:ghost-audit
```

Name the target and the requested outcome, for example "audit /path/to/padlib without
editing it". All twelve skills share the `ghost-library-skills:` prefix.

## Verify

Invoke `/ghost-library-skills:ghost-audit` with a target and a read-only request. A
finding report or a no-drift report is a working install; an unknown-command error is
not.
