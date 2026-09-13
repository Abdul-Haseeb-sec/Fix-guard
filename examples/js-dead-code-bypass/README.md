# JavaScript Dead-Code Bypass Bug

This is a JavaScript translation of the classic dead-code bypass incident. It proves that the 8 verification rules are completely language-agnostic.

## The Bug

In `detector.js`, there is a `thresholdCheck` function that is supposed to flag scores greater than 5. Previously, it flagged scores `>= 5`, meaning a score of 5 was falsely flagged as a privilege escalation.

An agent successfully updated the logic to `> 5`. The `node:test` suite in `detector.test.js` passes.

## The Illusion

Run the tests (requires Node 20+):
```bash
node --test detector.test.js
```

All tests pass. The agent assumes the code is completely fixed and ready for production.

## The Reality

The `main()` function parses CLI arguments using `util.parseArgs`. The `--mode` argument defaults to `quick`. 

When `--mode=quick` is used, the script completely bypasses the `thresholdCheck` function and instead routes to `quickScan`, which uses a completely different threshold (8). 

Run the bug for yourself:
```bash
node detector.js --score 5
```
Output: `[OK SAFE] Quick scan safe` — it ran `quickScan`, bypassing the fix entirely!

If a user explicitly runs with `--mode=full`:
```bash
node detector.js --score 5 --mode=full
```
Output: `[OK SAFE] Score 5 within safe range` — this is what the agent *assumed* was happening by default.

## How fix-guard catches this

Rule 4 explicitly requires checking default arguments and configurations for bypass traps. A fix-guard compliant agent would spot the `default: 'quick'` configuration in the CLI parser and flag this fix as UNVERIFIED because the fixed logic isn't accessible by default.
