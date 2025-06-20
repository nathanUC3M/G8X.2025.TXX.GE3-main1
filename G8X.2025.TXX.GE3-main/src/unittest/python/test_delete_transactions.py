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
        self.assertEqual(result, 1000.0)

        # Check that the deleted transactions file was created and has the right content
        self.assertTrue(os.path.exists(DELETED_TRANSACTIONS_FILE))
        with open(DELETED_TRANSACTIONS_FILE, "r", encoding="utf-8") as file:
            deleted_data = json.load(file)
        self.assertEqual(len(deleted_data), 1)
        self.assertEqual(deleted_data[0]["amount"], "-5000")

        # Check that the original transactions file is updated
        with open(TRANSACTIONS_STORE_FILE, "r", encoding="utf-8") as file:
            remaining_data = json.load(file)
        self.assertEqual(len(remaining_data), 2) # a transaction for another iban is there
        remaining_ibans = {tx["IBAN"] for tx in remaining_data}
        self.assertIn(self.valid_iban, remaining_ibans)

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

    def test_TC5_invalid_country_code(self):
        """TC5: IBAN with invalid country code (GE)"""
        invalid_iban = "GE12345678901234567890123"
        mngr = AccountManager()
        with self.assertRaises(AccountManagementException) as context:
            mngr.delete_transactions(invalid_iban[:24], -5000)
        self.assertEqual(context.exception.message, "Invalid IBAN format")

    def test_TC6_all_D_characters(self):
        """TC6: IBAN with all D characters, fails digit parsing"""
        invalid_iban = "ESDDDDDDDDDDDDDDDDDDDDDD"
        mngr = AccountManager()
        with self.assertRaises(AccountManagementException) as context:
            mngr.delete_transactions(invalid_iban, -5000)
        self.assertEqual(context.exception.message, "Invalid IBAN format")

    def test_TC7_invalid_control_digits(self):
        """TC7: IBAN with valid format but invalid control digits"""
        # Correct length and ES prefix but fails modulo 97 check
        invalid_iban = "ES0059005439021242088295"
        mngr = AccountManager()
        with self.assertRaises(AccountManagementException) as context:
            mngr.delete_transactions(invalid_iban, -5000)
        self.assertEqual(context.exception.message, "Invalid IBAN control digit")

    def test_TC8_valid_but_no_matching_transactions(self):
        """TC8: Valid IBAN with no matching transactions in file"""
        mngr = AccountManager()
        unused_iban = "ES9820385778983000760236"  # 22 digits, valid format
        with self.assertRaises(AccountManagementException) as context:
            mngr.delete_transactions(unused_iban, -5000)
        self.assertEqual(context.exception.message, "No transactions for the given IBAN")

    def test_TC9_amount_out_of_bounds(self):
        """TC9: Valid IBAN with valid transactions, but amount = -5001 (out of range)"""
        mngr = AccountManager()
        with self.assertRaises(AccountManagementException) as context:
            mngr.delete_transactions(self.valid_iban, -5001)
        self.assertEqual(context.exception.message, "Invalid amount value")

    def test_TC10_amount_as_string(self):
        """TC10: Amount is a string instead of integer, should raise datatype exception"""
        mngr = AccountManager()
        amount_as_string = "-5000"  # incorrect type

        with self.assertRaises(AccountManagementException) as context:
            mngr.delete_transactions(self.valid_iban, amount_as_string)

        self.assertEqual(context.exception.message, "Invalid amount value")

    def test_TC11_positive_amount(self):
        """TC11: Valid IBAN and positive amount with matching transaction"""
        mngr = AccountManager()
        result = mngr.delete_transactions(self.valid_iban, 1000)
        self.assertEqual(result, -5000.0)

        # Check that the deleted transactions file was created and has the right content
        self.assertTrue(os.path.exists(DELETED_TRANSACTIONS_FILE))
        with open(DELETED_TRANSACTIONS_FILE, "r", encoding="utf-8") as file:
            deleted_data = json.load(file)
        self.assertEqual(len(deleted_data), 1)
        self.assertEqual(deleted_data[0]["amount"], "1000")

    def test_TC12_no_transactions_match_criteria(self):
        """TC12: Valid IBAN, but no transactions match the deletion criteria"""
        mngr = AccountManager()
        with self.assertRaises(AccountManagementException) as context:
            mngr.delete_transactions(self.valid_iban, 2000)
        self.assertEqual(context.exception.message, "No transactions match the deletion criteria")

        # Make sure no deleted_transactions.json file was created
        self.assertFalse(os.path.exists(DELETED_TRANSACTIONS_FILE))


if __name__ == "__main__":
    unittest.main()
