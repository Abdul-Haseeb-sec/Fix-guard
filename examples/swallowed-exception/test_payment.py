import unittest
from payment_processor import process_payment

class TestPaymentProcessor(unittest.TestCase):
    def test_successful_payment(self):
        """Standard payment processes successfully"""
        self.assertTrue(process_payment("acc_123", 500))

    def test_connection_error_handled(self):
        """Connection errors are gracefully handled without crashing"""
        # The agent wrote this test to verify the fix
        self.assertFalse(process_payment("err_timeout", 500))

if __name__ == "__main__":
    unittest.main()
