# Installing ghost-library-skills on Antigravity

Per-host capabilities — what Antigravity loads and how skills are invoked — live in
[host-support.md](host-support.md). This page covers install only.

There is no `.antigravity/` directory in this repository: Antigravity installs the
plugin straight from the Git URL, so no host-specific manifest is generated for it. The
hand-authored root `plugin.json` is the install adapter; ai-rulez does not generate it.

## Install

Antigravity's plugin installer currently has no project-scope option; this installs the
plugin into Antigravity's user plugin registry, so it is available across repositories.

```sh
agy plugin install https://github.com/hasansezertasan/ghost-library-skills
```

GitHub-source installation becomes available after the manifests are committed and
published; it has not been tested against the current remote. Prefer a local checkout
on the other hosts until then.

## Update

Reinstall the plugin with the same command, then **restart**. There is no in-place
`update` verb — reinstalling is the update path.

## Invoke

Ask Antigravity to run `ghost-audit` with the target and requested outcome, for example
"run ghost-audit on /path/to/padlib without editing it". All twelve skills are
available by name. This plugin ships skills only — no slash commands, agents, or hooks
(`agy plugin validate` reports those as skipped).

## Verify

Ask for a read-only audit of a target. A finding report or a no-drift report is a
working install.
