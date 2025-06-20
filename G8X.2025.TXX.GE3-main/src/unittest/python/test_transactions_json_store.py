import os
import unittest

from uc3m_money import AccountManagementException
from uc3m_money.storage.transactions_json_store import TransactionsJsonStore
from uc3m_money.cfg.account_management_config import TRANSACTIONS_STORE_FILE

class TestFindAllFunction(unittest.TestCase):
    """Test cases for the find_all method in TransactionsJsonStore"""

    def setUp(self):
        """Backup the original transactions file before each test."""
        self.original_file = TRANSACTIONS_STORE_FILE
        self.backup_file = self.original_file + ".bak"
        if os.path.exists(self.original_file):
            os.rename(self.original_file, self.backup_file)

    def tearDown(self):
        """Restore the original file and clean up any test-specific files."""
        if os.path.exists(self.original_file):
             os.remove(self.original_file)
        if os.path.exists(self.backup_file):
            os.rename(self.backup_file, self.original_file)

    def test_find_all_file_not_found(self):
        """Returns empty list if transactions.json file is missing"""
        # setUp ensures the file is missing by renaming it
        store = TransactionsJsonStore()
        result = store.find_all("IBAN", "ES3559005439021242088295")
        self.assertEqual(result, [])

    def test_find_all_file_empty(self):
        """Returns empty list if the JSON file is empty ([])"""
        with open(self.original_file, "w", encoding="utf-8") as f:
            f.write("[]")

        store = TransactionsJsonStore()
        result = store.find_all("IBAN", "ES3559005439021242088295")
        self.assertEqual(result, [])

    def test_find_all_json_decode_error(self):
        """Raises AccountManagementException if JSON file is invalid"""
        with open(self.original_file, "w", encoding="utf-8") as f:
            f.write("{,}") # Malformed JSON

        store = TransactionsJsonStore()
        with self.assertRaises(AccountManagementException) as cm:
            store.find_all("IBAN", "ES3559005439021242088295")
        self.assertEqual(cm.exception.message, "JSON Decode Error - Wrong JSON Format")

    def test_find_all_no_match(self):
        """Should return empty list when IBAN is not found in a valid file"""
        with open(self.original_file, "w", encoding="utf-8") as f:
            f.write('[{"IBAN": "ES1234567890123456789012", "amount": "100"}]')

        store = TransactionsJsonStore()
        result = store.find_all("IBAN", "ES0000000000000000000000")
        self.assertEqual(result, [])

    def test_find_all_one_match(self):
        """Should return a list with one item when one IBAN matches"""
        iban_to_find = "ES1111111111111111111111"
        data = [
            {"IBAN": "ES0000000000000000000000", "amount": "100"},
            {"IBAN": iban_to_find, "amount": "200"},
            {"IBAN": "ES2222222222222222222222", "amount": "300"}
        ]
        with open(self.original_file, "w", encoding="utf-8") as f:
            import json
            json.dump(data, f)

        store = TransactionsJsonStore()
        result = store.find_all("IBAN", iban_to_find)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["amount"], "200")

    def test_find_all_all_items_match(self):
        """Should return all items when all transactions in the file match"""
        iban_to_find = "ES1111111111111111111111"
        data = [
            {"IBAN": iban_to_find, "amount": "100"},
            {"IBAN": iban_to_find, "amount": "200"},
            {"IBAN": iban_to_find, "amount": "300"},
        ]
        with open(self.original_file, "w", encoding="utf-8") as f:
            import json
            json.dump(data, f)

        store = TransactionsJsonStore()
        result = store.find_all("IBAN", iban_to_find)
        self.assertEqual(len(result), len(data))

        self.assertCountEqual(result, data)

