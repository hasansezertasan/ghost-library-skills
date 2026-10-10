# Why ghost libraries

A ghost library distributes a behavioral specification and portable fixtures instead of a maintained implementation. A consumer generates or writes idiomatic code into their own project and checks it against the contract.

The maintainer owns shared behavior and verification artifacts. The consumer owns the generated code, integration, local changes, and operational maintenance. Keeping that distinction visible enables downstream failures to improve the shared contract without treating every customization as an upstream rule.

Focused deterministic utilities are a useful starting point. Stateful tools, UI behavior, external datasets, performance-sensitive code, and platform integrations need additional ways to judge behavior. Suitability depends on whether the relevant guarantees can be specified and tested with available resources, not whether the repository has fewer than an arbitrary number of functions.

Shipping no implementation does not imply no dependencies, no security concerns, no updates, or no maintenance. Define dependency policy explicitly and retain source identity so a generated implementation can be reproduced, diagnosed, and upgraded.

The approach draws on [Drew Breunig's experiment](https://www.dbreunig.com/2026/01/08/a-software-library-with-no-code.html) and [whenwords](https://github.com/dbreunig/whenwords), plus [Armin Ronacher's account of behavioral porting with shared tests](https://lucumr.pocoo.org/2026/1/14/minijinja-go-port/). Their practical lesson for these skills is to maintain clear contracts and trustworthy feedback loops while reporting the limits of the evidence.
