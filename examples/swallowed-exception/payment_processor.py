def verify_funds(account_id: str, amount: float):
    # Dummy logic: accounts starting with "err" simulate a connection timeout
    if account_id.startswith("err"):
        raise ConnectionError("Payment gateway timeout")
    if amount > 1000:
        raise ValueError("Insufficient funds")
    return True

def process_payment(account_id: str, amount: float):
    """
    Process a payment.
    BUG: An agent was asked to prevent crashes when verify_funds throws a ConnectionError,
    by catching the error and returning False.
    The agent used a broad `except Exception:` instead of `except ConnectionError:`.
    """
    try:
        if verify_funds(account_id, amount):
            return True
    except Exception:
        # BUG: Swallows ValueError ("Insufficient funds") and returns False as if it was a connection error.
        # This prevents the system from properly logging insufficient funds, treating it as a transient error.
        return False
    return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", type=str, required=True)
    parser.add_argument("--amount", type=float, required=True)
    args = parser.parse_args()
    
    try:
        success = process_payment(args.account, args.amount)
        print(f"Payment success: {success}")
    except ValueError as e:
        print(f"[REJECTED] {e}")
