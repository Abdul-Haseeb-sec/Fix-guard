#!/bin/bash
set -e

# Extract the core rules from each file
# We extract from "## Rule 1" down to the end of the Verification Report Template code block (```)
extract_rules() {
  sed -n '/^## Rule 1/,/^```$/p' "$1"
}

R1=$(extract_rules "fix-guard.md")
R2=$(extract_rules "fix-guard.mdc")
R3=$(extract_rules "fix-guard-prompt.md")

FAILED=0

if [ "$R1" != "$R2" ]; then
  echo "ERROR: fix-guard.md and fix-guard.mdc are out of sync"
  diff -u <(echo "$R1") <(echo "$R2")
  FAILED=1
fi

if [ "$R1" != "$R3" ]; then
  echo "ERROR: fix-guard.md and fix-guard-prompt.md are out of sync"
  diff -u <(echo "$R1") <(echo "$R3")
  FAILED=1
fi

if [ "$FAILED" -eq 1 ]; then
  echo "Variant sync check failed. The rule bodies must be exactly identical."
  exit 1
fi

echo "SUCCESS: All three variant files are perfectly in sync."
exit 0
