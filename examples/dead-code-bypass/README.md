# Dead-Code Bypass Example

This example reproduces the exact bug class from the [Origin Story](../../README.md#the-origin-story) — the incident that inspired fix-guard.

## What's in here

| File | Purpose |
|------|---------|
| `detector.py` | A privilege escalation detector with **two bugs**: a boundary-condition error in `threshold_check()`, and a CLI default (`--mode=quick`) that silently bypasses `threshold_check()` entirely |
| `test_detector.py` | A test suite that **passes** — but never tests the boundary condition and never exercises the CLI's default code path |

## The setup

1. `threshold_check()` uses `>=` instead of `>` for boundary detection. A score exactly equal to the threshold incorrectly triggers a detection.
2. The CLI's `--mode` flag defaults to `quick`, which calls `quick_scan()` instead of `threshold_check()`. So even if you fix the bug in `threshold_check()`, the fix is **dead code** in default usage.

## Try it yourself (< 5 minutes)

### Step 1: Run the tests

```bash
cd examples/dead-code-bypass
python -m pytest test_detector.py -v
# or: python -m unittest test_detector -v
```

All 8 tests pass. ✅

### Step 2: Ask an agent to fix the bug

Tell your AI coding agent:

> "Fix the threshold_check() function in detector.py. The boundary condition is wrong — score equal to threshold should NOT trigger detection."

### Step 3: Observe the difference

**Without fix-guard**, the agent will likely:
1. Change `>=` to `>` in `threshold_check()` ✅ (correct fix)
2. Run the test suite → all pass ✅
3. Report: *"Fixed! All tests pass."* ❌ (false confidence)

The agent won't notice:
- No test covers `score == threshold` (the exact bug)
- The CLI default `--mode=quick` bypasses `threshold_check()` entirely
- The fix is **dead code** in production usage

**With fix-guard**, the agent will:
1. Change `>=` to `>` ✅
2. Name which test exercises the changed line → realizes **none do** (Rule 1, 2)
3. Construct boundary input `score=5, threshold=5` → show before/after (Rule 3)
4. Check for bypass traps → find `--mode=quick` default (Rule 4)
5. Show raw test output (Rule 5)
6. Report: *"Fix applied. WARNING: CLI default --mode=quick bypasses this function entirely. The fix is correct but unreachable in default usage."* ✅

### Step 4: Verify the bypass yourself

```bash
# Default mode (quick) — threshold_check() is NEVER called
python detector.py --score 5
# Output: [OK SAFE] (quick_scan hardcoded path, ignores threshold_check)

# Full mode — now threshold_check() runs
python detector.py --score 5 --mode full
# Output: [!! DETECTED] (the bug! score=5 == threshold=5 triggers detection)

# After fixing >= to >:
# python detector.py --score 5 --mode full
# Output: [OK SAFE] (correct — score=5 does not exceed threshold=5)
```

## The lesson

A green test suite is not proof that a fix works. fix-guard forces the agent to do what a careful human reviewer would do: trace the execution path, test the boundary, and check for bypass traps.
