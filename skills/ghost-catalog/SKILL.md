---
name: ghost-catalog
description: Check a ghost library's discoverability and listing readiness: required artifacts, accurate README claims, license, metadata, and a catalog's eligibility rules, then prepare a listing entry. Use before publishing or listing a ghost library, not for behavioral review.
---

# Prepare a library for discovery

Read [contract rules](references/contract-rules.md) and [philosophy](references/philosophy.md).

## Work

1. Establish the repository, revision, and the catalogs or listings in scope, such as a topic, an awesome list, or a package index. Read each catalog's own contribution and eligibility rules; they take precedence over general guidance here.
2. Check required artifacts exist and link correctly: specification, portable fixtures, generation instructions, README, and license. Verify stated case counts by parsing fixtures with their declared profile, and check version statements and artifact links. Deep behavioral review belongs to `ghost-audit`; report suspected contract problems as a referral.
3. Review README claims against evidence. Flag claims that overstate what local generation guarantees, such as no maintenance, no dependencies, or no supply chain, and claims of language support without saved verification.
4. Check discoverability metadata: repository description, topics, and the catalog's required fields. Propose values from the repository's own facts.
5. Report with [the catalog template](templates/reports/catalog.md) and draft the listing entry. Repairs to the repository are made only when requested. Submitting a listing, opening a pull request, or changing repository settings requires separate authorization.

## Output and completion

Deliver the readiness checks, proposed corrections, and a draft listing entry.

Complete when every catalog requirement has a status with evidence and the draft entry contains only verified facts. Readiness for a catalog is not certification of the library's behavior.
