"""Class for dealing with iban's balances"""
from datetime import datetime
from datetime import timezone
from uc3m_money.exception.account_management_exception import AccountManagementException
from uc3m_money.data.attr.iban_code import IbanCode
from uc3m_money.storage.balances_json_store import BalancesJsonStore
from uc3m_money.storage.transactions_json_store import TransactionsJsonStore

class IbanBalance():
    """Class that represents the current balance for an IBAN code"""
    def __init__(self, iban_code):
        self._iban = IbanCode(iban_code).value
        self._last_balance_time = datetime.timestamp(datetime.now(timezone.utc))
        self._balance = self.calculate_account_balance()

    def calculate_account_balance(self):
        """calculates the current balance for the object's iban code"""
        transactions_storage = TransactionsJsonStore()

        transactions_list = transactions_storage.find_all("IBAN", self._iban)
        if len(transactions_list) == 0:
            raise AccountManagementException("IBAN not found")
        current_balance = 0
        for transaction in transactions_list:
            current_balance += float(transaction["amount"])
        return current_balance

    def to_json(self):
        """returns the object info in json format"""
        return {"IBAN": self._iban,
                "time": self._last_balance_time,
                "BALANCE": self._balance}

    def save_balance(self):
        """saves the current balance of the iban into a json store"""
        balances_storage = BalancesJsonStore()
        balances_storage.add_item(self)
