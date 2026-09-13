# Mocked Dependency Mask Bug

This example reproduces another very common failure class: **The Mocked Dependency Mask**.

## The Scenario

An agent is given a ticket: *"Ensure user data is encrypted at rest by setting the encryption flag."*

The agent looks at `StorageService.save_user_data()` which calls `upload_to_s3(..., use_encryption=False)`. It updates the call to pass `use_encryption=True`.

## The Illusion of Success

The agent runs the tests to verify the fix:
```bash
python -m unittest test_storage.py -v
```

The test `test_save_user_data_is_encrypted` passes! It asserts that `upload_to_s3` was called with `use_encryption=True`. The agent reports: *"Fixed. Tests pass."*

## The Reality

The test extensively mocks the `upload_to_s3` dependency using `@patch`. Because the dependency is entirely replaced with a `MagicMock`, the test is completely blind to the actual behavior of the real function.

In reality, the underlying SDK requires a KMS key ID to be configured when encryption is turned on. By just flipping the boolean flag, the agent caused a fatal crash in production.

Run the production script to see what actually happens when the mock isn't there:
```bash
python cloud_storage.py
```
Output: `[CRASH] Missing KMSKeyId for encryption configuration in real SDK`

## How fix-guard catches this

Rule 2 (Coverage Confirmation) requires the agent to confirm the test exercises the *exact lines* changed. If the target function is mocked out, the code is technically "covered", but its execution path is hijacked. 
More importantly, Rule 6 (Clean-State Re-verification) and Rule 7 (Graceful Degradation) demand manual end-to-end verification. A fix-guard compliant agent would run `python cloud_storage.py`, see the crash, and immediately flag the fix as **UNVERIFIED**.
