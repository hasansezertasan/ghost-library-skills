# Installation

Your agent is the interface. Install the skills once, then ask your agent to
maintain a ghost library; you do not run the individual skills yourself.

Copy this prompt into your coding agent:

```text
Install the ghost-library-skills skills: pick the best installation method for
you from https://github.com/hasansezertasan/ghost-library-skills/blob/main/docs/installation.md

Then use its ghost-audit skill to audit my ghost library at the path I give you,
without editing it. Ask me for the path and anything else you need, and ask
before you change files outside that library.
```

The prompt points at this page, not at a command, so the routes below can change
without the prompt changing.

## Then use it

Each request below starts a skill. Say what you want in your own words.

| Ask your agent to | Skill |
| --- | --- |
| Turn an idea into a bounded library or domain | `ghost-init` |
| Define or change behavior and assess compatibility | `ghost-spec` |
| Create portable cases, scenarios and invariants | `ghost-tests` |
| Review contradictions, coverage and documentation drift | `ghost-audit` |
| Build or run a harness with complete case accounting | `ghost-verify` |
| Diagnose a downstream failure and add the right regression | `ghost-fix` |
| Prepare contract versions, migration notes and release evidence | `ghost-release` |
| Generate a verified implementation into a consumer project | `ghost-summon` |
| Measure how reliably a contract generates | `ghost-evaluate` |
| Derive a contract from existing code | `ghost-extract` |
| Migrate an implementation to a newer contract revision | `ghost-upgrade` |
| Check listing readiness and draft a catalog entry | `ghost-catalog` |

## Keep it current

Ask your agent to update the ghost-library-skills skills. It runs the update
command for the route it installed with (see the table below), confirms the
result and tells you to start a new session.

## For agents reading this page

You were pointed here to install the skills. Do this:

1. Pick the route in the table below that you can run yourself, matching your
   own host. Each route links to a guide with that host's caveats; read it
   before you run anything.
2. Every route except Antigravity installs from a local checkout. Clone this
   repository (`https://github.com/hasansezertasan/ghost-library-skills`) to a
   stable path first and use its absolute path. Do not use a temporary
   directory for a route that keeps pointing at the checkout.
3. If a route needs a slash command or an interactive step you cannot run, give
   the user the exact command and ask them to run it. Do not guess at another
   command.
4. Confirm the install with the host guide's Verify step.
5. Installs usually load in a new session, not in the conversation that
   installed them. If the skills are not available to you now, read
   `skills/ghost-audit/SKILL.md` from the clone and follow it, and tell the user
   to start a new session so the installed skills load next time.
6. If a route fails, fall back to reading `skills/<name>/SKILL.md` from the
   clone. Do not report the install as done until you have confirmed the skills
   or read a `SKILL.md`.
7. Install one distribution at a time; a second registration of the same
   plugin under an older name duplicates the skills.
8. Then continue with what the user asked. Do not install other agent skills or
   switch to a different route unless this one fails.

### Routes

| Host | Install | Update | Guide |
| --- | --- | --- | --- |
| Claude Code | `claude plugin marketplace add /absolute/path/to/ghost-library-skills`, then `claude plugin install ghost-library-skills@ghost-library-skills-marketplace` | refresh the checkout, `claude plugin marketplace update ghost-library-skills-marketplace`, then `claude plugin update ghost-library-skills@ghost-library-skills-marketplace`; restart | [install-claude-code.md](install-claude-code.md) |
| Codex CLI | `codex plugin marketplace add /absolute/path/to/ghost-library-skills`, then `codex plugin add ghost-library-skills@ghost-library-skills-marketplace`; start a fresh session | refresh the checkout, repeat `codex plugin add`; start a fresh session | [install-codex.md](install-codex.md) |
| Pi | `pi install /absolute/path/to/ghost-library-skills` | refresh the checkout, `pi update /absolute/path/to/ghost-library-skills`; restart | [install-pi.md](install-pi.md) |
| OpenCode | add `/absolute/path/to/ghost-library-skills/skills` to `skills.paths` in the OpenCode config; restart | `git pull` in the checkout; restart | [install-opencode.md](install-opencode.md) |
| Antigravity | `agy plugin install https://github.com/hasansezertasan/ghost-library-skills` | reinstall; restart | [install-antigravity.md](install-antigravity.md) |
| Manual | clone this repository and read `skills/<name>/SKILL.md`, or copy `skills/*` into your agent's skills directory | `git pull` in the clone, then copy again if you copied | |

Confirm every route the same way: ask for a read-only `ghost-audit` of a target.
A finding report or a no-drift report is a working install.

None of these routes is verified end to end. [Host support](host-support.md)
records the evidence per host, including which are only validated locally.
Treat them as unverified packaging guidance, and tell the user which route you
used, whether you confirmed the skills afterwards, and whether a new session is
needed.
