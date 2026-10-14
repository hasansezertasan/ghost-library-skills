# Installing ghost-library-skills on Codex CLI

Per-host capabilities — including how Codex discovers skills — live in
[host-support.md](host-support.md). This page covers install only.

## Install

Use the absolute path to this repository. Consumers do not need to run the Python
builder first.

```sh
codex plugin marketplace add /absolute/path/to/ghost-library-skills
codex plugin add ghost-library-skills@ghost-library-skills-marketplace
```

Then **start a fresh session**. Plugins are resolved at session start.

GitHub-source installation becomes available after the manifests and the generated
Codex package are committed and published; it has not been tested against the current
remote. Prefer a local checkout until then. See the
[OpenAI plugin build guide](https://developers.openai.com/plugins/build/plugins).

## Update

Refresh the checkout, repeat the `add` command, and start a fresh session:

```sh
codex plugin add ghost-library-skills@ghost-library-skills-marketplace
```

The tested CLI has no `plugin update`; `plugin marketplace upgrade` refreshes Git
marketplace snapshots only.

## Invoke

Select `ghost-library-skills:ghost-audit` and provide the target and requested outcome.
All twelve skills share the `ghost-library-skills:` prefix.

## Verify

Select the audit skill with a read-only request. A finding report or a no-drift report
is a working install; no response at all means the session predates the install.
