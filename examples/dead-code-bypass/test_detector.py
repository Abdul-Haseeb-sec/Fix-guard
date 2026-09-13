"""
test_detector.py — Test suite for the privilege escalation detector.

THIS TEST SUITE DEMONSTRATES THE PROBLEM fix-guard SOLVES.

All tests pass. But NONE of them test the boundary condition where
score == threshold (the actual bug). And even if they did, they call
threshold_check() directly — they don't test the CLI's default mode,
which skips threshold_check() entirely via quick_scan().

An agent without fix-guard will run this suite, see "all pass",
and report "fixed" — even though:
  1. The boundary bug is untested
  2. The CLI default mode bypasses the fix entirely

An agent WITH fix-guard will:
  1. Notice these tests don't cover the exact changed lines (Rule 2)
  2. Construct a boundary input score=5, threshold=5 (Rule 3)
  3. Check for bypass traps and find the --mode=quick default (Rule 4)
  4. Show raw test output instead of just saying "tests pass" (Rule 5)
"""

import unittest
from detector import threshold_check, quick_scan


class TestThresholdCheck(unittest.TestCase):
    """Tests for threshold_check() — but missing the critical boundary case."""

    def test_high_score_detected(self):
        """Score well above threshold should trigger detection."""
        result = threshold_check(score=9, threshold=5)
        self.assertTrue(result["detected"])
        self.assertIn("exceeds", result["detail"])

    def test_low_score_safe(self):
        """Score well below threshold should be safe."""
        result = threshold_check(score=2, threshold=5)
        self.assertFalse(result["detected"])
        self.assertIn("within safe range", result["detail"])

    def test_zero_score(self):
        """Score of zero should always be safe."""
        result = threshold_check(score=0, threshold=5)
        self.assertFalse(result["detected"])

    def test_max_score(self):
        """Maximum score should always trigger detection."""
        result = threshold_check(score=10, threshold=5)
        self.assertTrue(result["detected"])

    def test_custom_threshold(self):
        """Custom threshold should be respected."""
        result = threshold_check(score=7, threshold=8)
        self.assertFalse(result["detected"])

    # NOTE: There is NO test for score == threshold (the boundary bug).
    # This is intentional — it demonstrates the coverage-blind pass.


class TestQuickScan(unittest.TestCase):
    """Tests for quick_scan() — the fast path that bypasses threshold_check()."""

    def test_high_risk(self):
        """Score >= 8 should be flagged in quick scan."""
        result = quick_scan(score=9)
        self.assertTrue(result["detected"])

    def test_acceptable_risk(self):
        """Score < 8 should be acceptable in quick scan."""
        result = quick_scan(score=5)
        self.assertFalse(result["detected"])

    def test_boundary_quick(self):
        """Score exactly 8 in quick scan."""
        result = quick_scan(score=8)
        self.assertTrue(result["detected"])


if __name__ == "__main__":
    unittest.main()
