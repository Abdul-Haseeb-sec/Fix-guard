# Evidence Base

This document tracks the verification of `fix-guard` rules against concrete bug classes and real-world incidents.

## Synthesized Examples (Verified)

These examples are constructed to isolate and reproduce common failure classes where an AI agent can merge a bug with a green test suite.

| Example Directory | Bug Class | Language | Status |
|-------------------|-----------|----------|--------|
| `examples/dead-code-bypass/` | Argparse default bypass | Python | **VERIFIED** |
| `examples/js-dead-code-bypass/` | CLI default bypass | JavaScript | **VERIFIED** |
| `examples/swallowed-exception/` | Overly broad exception handling | Python | **VERIFIED** |
| `examples/mocked-dependency-mask/` | Mock completely masks production crash | Python | **VERIFIED** |

## Real-World Open Source Incidents (Pending)

To definitively prove `fix-guard`'s efficacy in the wild, this section tracks historical open-source PRs or issues where a fix was merged with a green test suite that was plausibly blind to the actual change. 

| Repository | Issue/PR | Bug Class | Status |
|------------|----------|-----------|--------|
| TBD | TBD | Real-world coverage-blind pass or mocked dependency mask | **UNVERIFIED** |

> **Note on UNVERIFIED status:** Finding a perfect-fit, organically occurring open source incident that cleanly demonstrates this specific failure mode requires significant historical digging. Rather than fabricating a fake PR or forcing a poor fit to claim "fixed", we are adhering to Rule 8 (Escalation on Uncertainty) by explicitly marking this as **UNVERIFIED**. This serves as a call-to-action for community contribution.
