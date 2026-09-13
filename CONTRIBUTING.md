# Contributing to fix-guard

Thanks for your interest in making AI agents more honest about verification. Here's how to contribute.

## Core Principle

**Every rule must trace to a concrete, real-world failure mode.** No abstract "best practices." If you propose a new rule, you must describe the specific incident or failure class it prevents.

## What We Accept

### New rules
- Must include: the failure mode it addresses, a draft imperative rule text, and ideally a real example where an agent failed this way.
- Must pass the NFR-4 check: the total skill file must remain readable in under 5 minutes after your addition.

### Improvements to existing rules
- Rewording for clarity or stronger enforcement.
- Closing loopholes where agents can rationalize around a rule.
- Adding examples to the demo scenario.

### New agent variants
- If you use an agent that needs a specific format (Windsurf, Copilot, etc.), contribute a variant file.
- The rule content must be identical — only the wrapper format changes.

### Bug reports
- If an agent successfully ignores a rule, that's a bug. Report it with:
  - Which agent (name + version)
  - Which rule was ignored
  - What the agent said (exact transcript if possible)
  - What it should have said

## What We Don't Accept

- Rules that don't trace to a real failure mode
- Agent-specific formatting that changes rule content (not just wrapper)
- Dependencies — fix-guard must remain a zero-dependency, single-file artifact
- Telemetry or usage tracking of any kind

## How to Submit

1. Fork the repo
2. Create a branch: `git checkout -b your-change`
3. Make your changes
4. Open a PR with a clear description of the failure mode your change addresses

## Style Guide

- Rules are **direct imperatives** — "Do X" not "Consider doing X"
- Bold text marks the non-negotiable core of each rule
- Each rule has a name and a number — don't change numbering for existing rules
- Keep it scannable — a wall of text defeats the purpose

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
