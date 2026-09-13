# fix-guard

**Force AI coding agents to prove fixes work — not just claim they do.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](#)
[![Works with Claude Code](https://img.shields.io/badge/Claude%20Code-supported-blue.svg)](#claude-code)
[![Works with Cursor](https://img.shields.io/badge/Cursor-supported-purple.svg)](#cursor)
[![Works with Antigravity](https://img.shields.io/badge/Antigravity-supported-orange.svg)](#antigravity)
[![Works with VS Code](https://img.shields.io/badge/VS%20Code-supported-blue.svg)](#vs-code)

A single-file behavioral skill for AI coding agents that prevents false "fixed" claims. Copy one file into your project and your agent can never again say "tests pass" without showing exactly which tests exercise the fix, checking for bypass traps, and demonstrating the fix with a concrete before/after.

**Zero dependencies. Two minutes to install. Works across agents.**

---

## The Origin Story

This project exists because of a real bug that got past an AI agent while I was vibe coding a personal project.

I had asked an AI coding agent to fix a detection threshold bug in a python script. The agent confidently reported:

> *"Fixed the threshold bug. Ran the test suite — all tests pass. Ready to go."*

In reality, the fix was **dead code**. A command-line default value (`--mode=quick`) was silently routing execution around the corrected code path. The test suite passed because it always had — the tests never actually exercised the changed lines!

The bug was only caught because I refused to trust "tests pass" and manually ran the code to test it myself. 

**This is not a one-off.** It's a known, common, and largely unaddressed failure mode across AI coding agents: agents optimize for "tests pass" as a terminal signal because that's the cheapest proxy for correctness. Most agent tooling doesn't force a distinction between *"the suite is green"* and *"the suite actually tested the change."*

fix-guard fixes that.

---

## Before & After

**Before (without fix-guard):**

> **Agent:** "Fixed the privilege_escalation threshold bug. Ran the test suite — all 73 tests pass. Ready to merge."

**After (with fix-guard):**

> **Agent:** "Change made to `threshold_check()` in detector.py. Test `test_privilege_escalation_threshold` exercises this function — confirmed via coverage that it hits the modified lines (14–19). Constructed boundary input `level=3` (previously misclassified) — fails on pre-fix code, passes on post-fix code (output attached). Checked for bypass: the CLI's `--threshold` argparse default was previously overriding this path in production use — **flagging as a risk** unless default is also updated. Re-ran full suite from a clean checkout: 73/73 pass. Status: **FIXED**, with one flagged follow-up (argparse default)."

👉 [**See a real transcript of an agent using fix-guard**](examples/dead-code-bypass/REAL_TRANSCRIPT.md)

---

## The 8 Rules

| # | Rule | What it prevents |
|---|------|-----------------|
| 1 | **Terminal Claim Gate** | Agents saying "fixed" without naming which tests cover the change |
| 2 | **Coverage Confirmation** | Green suites that never touch the changed lines |
| 3 | **Adversarial Check** | Missing boundary conditions that would catch the bug instantly |
| 4 | **Bypass Trap Check** | Default args, config values, or feature flags routing around the fix |
| 5 | **Raw Output Requirement** | Narrative summaries ("tests pass") replacing actual command output |
| 6 | **Clean-State Re-verification** | Stale local state masking bugs that appear on fresh checkouts |
| 7 | **Graceful Degradation** | Skipping verification entirely when no tests exist |
| 8 | **Escalation on Uncertainty** | Rounding uncertain results up to "fixed" instead of "unverified" |

---

## Installation

### Claude Code

Copy the skill file into your project:

```bash
mkdir -p .claude/skills
cp fix-guard.md .claude/skills/fix-guard.md
```

Or install globally (applies to all projects):

```bash
# Linux/macOS
cp fix-guard.md ~/.claude/skills/fix-guard.md

# Windows
copy fix-guard.md %USERPROFILE%\.claude\skills\fix-guard.md
```

The skill activates automatically on all files (configured via `globs: ["**/*"]` in the frontmatter).

### Cursor

Copy the rules file into your project:

```bash
mkdir -p .cursor/rules
cp fix-guard.mdc .cursor/rules/fix-guard.mdc
```

The rule is set to `alwaysApply: true`, so it activates globally — no path scoping needed.

### Antigravity

Copy the skill file into your project's `.agents` folder (or globally in your home directory) and name it `SKILL.md`:

```bash
mkdir -p .agents/skills/fix-guard
cp fix-guard.md .agents/skills/fix-guard/SKILL.md
```

Antigravity will automatically discover it on your next session.

### VS Code (GitHub Copilot)

VS Code Copilot supports workspace-level instructions. You can append the prompt file to your `.github/copilot-instructions.md`:

```bash
mkdir -p .github
cat fix-guard-prompt.md >> .github/copilot-instructions.md
```

### Other Agents (Manual Prompting)

For agents without native persistent skill loading, paste the contents of `fix-guard-prompt.md` at the start of your fix/verification session.

```bash
# Copy the prompt to your clipboard, then paste it into the agent
cat fix-guard-prompt.md | clip     # Windows
cat fix-guard-prompt.md | pbcopy   # macOS
cat fix-guard-prompt.md | xclip    # Linux
```

---

## Try the Example

A minimal demo reproducing the exact OmniLog bug class is included. Takes under 5 minutes:

```bash
cd examples/dead-code-bypass
python -m unittest test_detector -v   # All 8 tests pass — but the bug is still there
```

See [`examples/dead-code-bypass/README.md`](examples/dead-code-bypass/README.md) for the full walkthrough.

---

## How It Works

fix-guard is **not a testing tool**. It doesn't generate tests, run mutation analysis, or instrument coverage. It's a set of 8 imperative rules loaded into your agent's context that change the agent's behavior at the moment it's about to claim "fixed."

The rules work because they target the exact decision point where agents fail: the transition from "I changed some code" to "I'm telling the human it's done." fix-guard inserts a mandatory checklist at that transition that the agent cannot skip.

Each rule is:
- **A direct imperative** — not vague guidance an agent could rationalize around
- **Tied to a concrete failure mode** — every rule traces back to a real incident
- **Self-contained** — no external dependencies, APIs, or infrastructure

---

## FAQ

**Q: Does this actually change agent behavior, or is it just another prompt?**
Every rule is an imperative statement, not a suggestion. Empirically, agents follow well-structured imperative instructions loaded persistently into context. The key difference from ad-hoc prompting is persistence: the rules apply to *every* fix in *every* session, not just when you remember to ask.

**Q: What if my project has no tests?**
Rule 7 (Graceful Degradation) explicitly covers this: the agent follows a manual verification checklist instead of skipping verification.

**Q: Does this slow down my agent?**
Yes, slightly — the agent does more work before claiming "done." That's the point. A 30-second delay is cheaper than deploying dead code.

**Q: Can I use this with [specific agent]?**
If your agent can load a persistent text file into context (or you can paste one), fix-guard works. The included variants natively support Claude Code, Cursor, Antigravity, and VS Code (GitHub Copilot), plus fallback instructions for any other agent.

**Q: Does this guarantee my fixes are correct?**
No. fix-guard forces *honest reporting* of verification state. It makes it much harder for an agent to claim "fixed" on unverified code, but it cannot guarantee the absence of all bugs. Rule 8 exists specifically for this: when in doubt, the agent reports UNVERIFIED.

---

## Project Structure

```
fix-guard/
├── fix-guard.md              # Claude Code skill file
├── fix-guard.mdc             # Cursor rules file
├── fix-guard-prompt.md       # Antigravity / generic prompt block
├── README.md                 # This file
├── LICENSE                   # MIT
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md            # How to contribute
├── examples/
│   └── dead-code-bypass/     # Reproduces the OmniLog bug class
│       ├── detector.py       # Buggy privilege escalation detector
│       ├── test_detector.py  # Green-but-coverage-blind test suite
│       └── README.md         # 5-minute walkthrough
└── .github/
    └── ISSUE_TEMPLATE/
        ├── bug_report.md
        └── feature_request.md
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. The key principle: every rule in the skill file must trace to a concrete, real-world failure mode. No abstract "best practices."

---

## License

[MIT](LICENSE) — Abdul Haseeb, 2026.

---

## Topics

`ai-agents` · `claude-code` · `cursor` · `verification` · `testing` · `developer-tools` · `code-quality` · `ai-safety`
