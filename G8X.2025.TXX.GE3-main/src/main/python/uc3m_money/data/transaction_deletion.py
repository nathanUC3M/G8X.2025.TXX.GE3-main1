import os
import json
from uc3m_money.data.iban_balance import IbanBalance
from uc3m_money.data.attr.iban_code import IbanCode
from uc3m_money.storage.transactions_json_store import TransactionsJsonStore
from uc3m_money.cfg.account_management_config import JSON_FILES_PATH
from uc3m_money.exception.account_management_exception import AccountManagementException

class TransactionDeletion:
    """Handles transaction deletion logic based on IBAN and amount."""

    def __init__(self, iban: str, amount: int):
        self.iban = self._validate_iban(iban)
        self.amount = self._validate_amount(amount)
        self.transactions_store = TransactionsJsonStore()

    def _validate_iban(self, iban_input: str) -> str:
        try:
            return IbanCode(iban_input).value
        except AccountManagementException as ex:
            raise AccountManagementException(ex.message) from ex

    def _validate_amount(self, amount_input) -> int:
        if not isinstance(amount_input, int) or amount_input < -5000 or amount_input > 5000:
            raise AccountManagementException("Invalid amount value")
        return amount_input

    def execute(self) -> float:
        # Find all transactions for the IBAN
        transactions = self.transactions_store.find_all("IBAN", self.iban)
        if not transactions:
            raise AccountManagementException("No transactions for the given IBAN")

        # Determine which transactions to delete
        if self.amount >= 0:
            to_delete = [tx for tx in transactions if float(tx["amount"]) >= self.amount]
        else:
            to_delete = [tx for tx in transactions if float(tx["amount"]) <= self.amount]

        if not to_delete:
            raise AccountManagementException("No transactions match the deletion criteria")

        # Remove matching transactions from file
        self.transactions_store.load_list_from_file()
        self.transactions_store._data_list = [
            tx for tx in self.transactions_store._data_list if tx not in to_delete
        ]
        self.transactions_store.save_list_to_file()

        # Archive deleted transactions
        self.deleted_transactions(to_delete)

        # Return updated balance
        return IbanBalance(self.iban)._balance

    def deleted_transactions(self, to_delete: list):
        deleted_file_path = os.path.join(JSON_FILES_PATH, "deleted_transactions.json")

        if os.path.exists(deleted_file_path):
            with open(deleted_file_path, "r", encoding="utf-8", newline="") as file:
                deleted_data = json.load(file)
        else:
            deleted_data = []

        deleted_data.extend(to_delete)

        with open(deleted_file_path, "w", encoding="utf-8", newline="") as file:
            json.dump(deleted_data, file, indent=2)
