import os
import json
import shutil
import unittest
from uc3m_money import AccountManager, AccountManagementException
from uc3m_money.cfg.account_management_config import TRANSACTIONS_STORE_FILE, JSON_FILES_PATH

TEMP_TRANSACTIONS_FILE = JSON_FILES_PATH + "transactions_swap.json"
DELETED_TRANSACTIONS_FILE = os.path.join(JSON_FILES_PATH, "deleted_transactions.json")


class TestDeleteTransactionsCases(unittest.TestCase):
    """Test delete_transactions with equivalence and boundary classes"""

    def setUp(self):
        """Backs up the original transactions file and creates controlled content"""
        self.valid_iban = "ES6211110783482828975098"
        self.test_data = [
            {"IBAN": self.valid_iban, "amount": "-5000"},
            {"IBAN": self.valid_iban, "amount": "1000"},
            {"IBAN": "ES0000000000000000000000", "amount": "1000"}
        ]

        if os.path.exists(TRANSACTIONS_STORE_FILE):
            shutil.copy(TRANSACTIONS_STORE_FILE, TEMP_TRANSACTIONS_FILE)

        with open(TRANSACTIONS_STORE_FILE, "w", encoding="utf-8") as file:
            json.dump(self.test_data, file, indent=2)

        if os.path.exists(DELETED_TRANSACTIONS_FILE):
            os.remove(DELETED_TRANSACTIONS_FILE)

    def tearDown(self):
        """Restores original file and cleans up"""
        if os.path.exists(TEMP_TRANSACTIONS_FILE):
            shutil.move(TEMP_TRANSACTIONS_FILE, TRANSACTIONS_STORE_FILE)
        if os.path.exists(DELETED_TRANSACTIONS_FILE):
            os.remove(DELETED_TRANSACTIONS_FILE)

    def test_TC1_valid_iban_and_transactions(self):
        """TC1: Valid IBAN and amount -5000 (boundary) with matching transaction"""
        mngr = AccountManager()
        result = mngr.delete_transactions(self.valid_iban, -5000)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)  # Should return remaining balance

    def test_TC2_invalid_iban_23_chars(self):
        """TC2: Invalid IBAN (23 digits)"""
        invalid_iban = "ES12345678901234567890123"
        mngr = AccountManager()
        with self.assertRaises(AccountManagementException) as context:
            mngr.delete_transactions(invalid_iban, -5000)
        self.assertEqual(context.exception.message, "Invalid IBAN format")

    def test_TC3_invalid_iban_21_chars(self):
        """TC3: Invalid IBAN (21 digits)"""
        invalid_iban = "ES123456789012345678901"
        mngr = AccountManager()
        with self.assertRaises(AccountManagementException) as context:
            mngr.delete_transactions(invalid_iban, -5000)
        self.assertEqual(context.exception.message, "Invalid IBAN format")

    def test_TC4_non_string_iban(self):
        """TC4: IBAN is an integer, not a string (datatype invalid)"""
        invalid_iban = 1234567890123456789012  # integer
        mngr = AccountManager()
        with self.assertRaises(AccountManagementException) as context:
            mngr.delete_transactions(invalid_iban, -5000)
        self.assertEqual(context.exception.message, "Invalid IBAN format")


if __name__ == "__main__":
    unittest.main()
