# Downstream receipt

Record this beside a generated implementation in the consumer project. It enables reproduction, diagnosis, and upgrades; it is not a registry entry.

| Field | Value |
| --- | --- |
| Contract source | URL or path |
| Source revision | Commit, tag, or content hashes when Git is unavailable |
| Domains/functions | Selected scope; note deliberate omissions |
| Spec and fixture identity | Paths and hashes |
| Target language/runtime | Name and version |
| API mapping | Location of the name, signature, null, and error mapping |
| Generated paths | Implementation and harness files |
| Local extensions | Consumer-specific behavior outside the upstream contract, or none |
| Verification command | Exact command that reruns the harness |
| Verification result | Conformance report location and decision |

Update the receipt whenever the implementation is regenerated, upgraded, or locally extended.
