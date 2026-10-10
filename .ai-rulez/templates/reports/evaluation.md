# Generation evaluation

## Scope and identity

Contract source and revision, selected domains, generation prompt or instructions, and the agent/model, language, and runtime of each matrix cell. State the matrix chosen and why.

## Results

| Cell (agent × language) | Decision | Discovered | Passed | Failed | Skipped | Unsupported | Retries | Duration/cost |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Use the conformance decision from each cell's report: full within scope, failing, or incomplete. Link each report.

## Failure analysis

Group failures by cause: implementation, harness, contract ambiguity, environment, or generation process. Name the cases and rules involved. Recurring failures across independent cells are evidence about the contract, not proof of a contract defect.

## Contract feedback

Ambiguities, missing cases, or instructions that the evaluation exposed, each with a proposed next skill (`ghost-spec`, `ghost-tests`, `ghost-audit`).

## Limitations

Trial count, isolation, unavailable cells, and what the results do not support. A small matrix is not a reliability estimate.
