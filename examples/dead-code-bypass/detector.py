"""
detector.py — Minimal privilege escalation detector.

This is a simplified reproduction of the OmniLog incident:
- threshold_check() has a bug: it uses >= instead of > for boundary detection
- The CLI has an argparse default (--threshold 10) that silently bypasses
  the code path where the bug lives when using --mode=quick (default mode)

THE BUG:
  threshold_check() uses `score >= threshold` but the spec says detection
  should only trigger when `score > threshold` (strictly greater).
  This means score=5 with threshold=5 incorrectly triggers a detection.

THE TRAP:
  Even after fixing threshold_check(), the CLI's default --mode=quick
  skips threshold_check() entirely and uses a hardcoded fast path.
  So the fix is real but DEAD CODE in default usage.
"""

import argparse
import sys


def threshold_check(score: int, threshold: int = 5) -> dict:
    """
    Check if a privilege escalation score exceeds the detection threshold.

    BUG: Uses >= instead of >. Score exactly equal to threshold should NOT
    trigger detection per spec, but currently does.

    Args:
        score: The privilege escalation risk score (0-10).
        threshold: The detection threshold. Detection triggers when
                   score is STRICTLY GREATER than threshold.

    Returns:
        dict with 'detected' (bool) and 'detail' (str).
    """
    # BUG: should be `score > threshold` (strictly greater)
    # Currently: score=5, threshold=5 → detected=True (WRONG per spec)
    if score >= threshold:
        return {
            "detected": True,
            "detail": f"Privilege escalation detected: score {score} exceeds threshold {threshold}",
        }
    else:
        return {
            "detected": False,
            "detail": f"Score {score} within safe range (threshold: {threshold})",
        }


def quick_scan(score: int) -> dict:
    """
    Fast-path scan that skips threshold_check() entirely.
    Uses a hardcoded threshold of 8 — any score below 8 is always 'safe'.

    This is the DEFAULT mode, which means threshold_check() is never
    called in normal usage even though it's the function with the bug.
    """
    if score >= 8:
        return {
            "detected": True,
            "detail": f"Quick scan: score {score} is high risk",
        }
    return {
        "detected": False,
        "detail": f"Quick scan: score {score} is within acceptable range",
    }


def main():
    parser = argparse.ArgumentParser(description="Privilege escalation detector")
    parser.add_argument(
        "--score", type=int, required=True, help="Privilege escalation risk score (0-10)"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=5,
        help="Detection threshold (default: 5)",
    )
    parser.add_argument(
        "--mode",
        choices=["quick", "full"],
        default="quick",  # THE TRAP: default mode skips threshold_check()
        help="Scan mode: 'quick' (fast, hardcoded) or 'full' (uses threshold_check)",
    )

    args = parser.parse_args()

    if args.mode == "quick":
        # This path NEVER calls threshold_check() — the bug is invisible here
        result = quick_scan(args.score)
    else:
        # Only this path exercises the buggy function
        result = threshold_check(args.score, args.threshold)

    status = "!! DETECTED" if result["detected"] else "OK SAFE"
    print(f"[{status}] {result['detail']}")

    sys.exit(1 if result["detected"] else 0)


if __name__ == "__main__":
    main()
