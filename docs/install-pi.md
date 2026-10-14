# Installing ghost-library-skills on Pi

Per-host capabilities — what Pi loads and how skills are invoked — live in
[host-support.md](host-support.md). This page covers install only.

## Install

Use the absolute path to this repository. Consumers do not need to run the Python
builder first.

```sh
pi install /absolute/path/to/ghost-library-skills
```

Local packages load from the source path without copying. The root manifest exposes
only skills; each generated skill contains its references and templates with
skill-local relative links. See
[Pi packages](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md).

## Update

Refresh the checkout, then:

```sh
pi update /absolute/path/to/ghost-library-skills
```

Then restart or reload resources.

## Invoke

```text
/skill:ghost-audit
```

Name the target and the requested outcome. All twelve skills ship through `/skill:`;
seven have been rediscovered on this host so far — the five newer skills use the same
packaging path but have not been rediscovered here. See [host-support](host-support.md).

## Verify

Invoke `/skill:ghost-audit` with a target and a read-only request. A finding report or
a no-drift report is a working install.
