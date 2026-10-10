---
name: ghost-evaluate
description: Evaluate how reliably a ghost-library contract produces conforming implementations by generating clean implementations across a small agent and language matrix in disposable workspaces and summarizing results, retries, costs, and unsupported cases. Use to judge a contract's generation quality, not to adopt one implementation.
---

# Evaluate generation across a matrix

Read [harness rules](references/harness-contract.md), the applicable [fixture profiles](references/fixture-profiles.md), and [contract rules](references/contract-rules.md).

## Work

1. Establish the pinned contract revision, selected domains, generation instructions under test, and the question the evaluation answers. Propose a small matrix of agents/models and languages that answers it, including at least one language whose null, error, string, or numeric conventions differ from the first. Running external agents, paid models, or networked tools requires the user's authorization; report cells you cannot run instead of substituting others silently.
2. Prepare one fresh disposable workspace per cell, outside the contract repository, with an identical copy of the contract at the pinned revision. Give each generating agent only the request and contract artifacts, not expected results, prior findings, or other cells' output.
3. Generate and verify each cell independently. Use one harness design per language, prove it with negative controls once, and reuse it only while its identity is unchanged. Record retries, interventions, duration, and cost where available. A cell that needed human repair is reported as such.
4. Classify every failure as implementation, harness, contract ambiguity, environment, or generation process. Repeated failures on one rule across independent cells point to a contract question worth auditing; they do not by themselves prove a contract defect.
5. Summarize with [the evaluation template](templates/reports/evaluation.md). Turn contract feedback into concrete proposals for `ghost-spec`, `ghost-tests`, or `ghost-audit` without editing the contract during the evaluation.

## Output and completion

Deliver the matrix results, per-cell conformance reports, failure analysis, contract feedback, and limitations. Keep generated code in the disposable workspaces unless the user asks to keep it.

Complete when each planned cell has a decision (full, failing, incomplete, or not run with a reason) backed by saved evidence. Single trials of a small matrix are not reliability estimates; state the trial count and do not extrapolate to untested languages or agents.
