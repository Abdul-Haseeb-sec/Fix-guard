# Swallowed Exception Bug

This example reproduces a common failure class: **The Swallowed Exception**.

## The Scenario

A developer asked an AI agent to fix a bug where `process_payment` was crashing the application due to intermittent `ConnectionError`s from the payment gateway. The agent was told: "Catch the connection error so the app doesn't crash."

The agent's "fix":
```python
    try:
        if verify_funds(account_id, amount):
            return True
    except Exception:
        return False
```

## The Illusion of Success

The agent runs the test suite and it passes:
```bash
python -m unittest test_payment -v
```

The agent reports: *"Fixed the crash. Tests pass."*

## The Reality

The agent used a broad `except Exception:` instead of specifically catching `ConnectionError`. 

By doing this, the agent **swallowed** a critical `ValueError: Insufficient funds`. 

Run the production script with an amount over 1000. 
```bash
python payment_processor.py --account user_123 --amount 5000
```

Instead of printing `[REJECTED] Insufficient funds`, it fails silently, outputting `Payment success: False` as if it were a minor gateway timeout. The exception is swallowed.

## How fix-guard catches this

Rule 3 (Adversarial Check) forces the agent to construct an input that exercises the fix. When verifying this, an agent would have to test a connection error. But Rule 2 (Coverage Confirmation) and Rule 4 (Bypass Trap Check) force the agent to review the execution path of the code they changed. A fix-guard compliant agent is forced to realize that the `except Exception` path is overly broad and swallows intended application errors, leading to an **UNVERIFIED** status.
