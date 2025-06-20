"""Account manager module """
import os
import json
from uc3m_money.data.attr.iban_code import IbanCode
from uc3m_money.exception.account_management_exception import AccountManagementException
from uc3m_money.data.transfer_request import TransferRequest
from uc3m_money.data.account_deposit import AccountDeposit
from uc3m_money.data.iban_balance import IbanBalance
from uc3m_money.storage.transactions_json_store import TransactionsJsonStore
from uc3m_money.cfg.account_management_config import JSON_FILES_PATH

class AccountManager:
    """singleton account manager"""
    class __AccountManager:
        """Class for providing the methods for managing the orders"""
        def __init__(self):
            pass

        #pylint: disable=too-many-arguments
        def transfer_request(self, from_iban: str,
                             to_iban: str,
                             concept: str,
                             transfer_type: str,
                             date: str,
                             amount: float)->str:
            """first method: receives transfer info and
            stores it into a file"""
            my_request = TransferRequest(from_iban=from_iban,
                                         to_iban=to_iban,
                                         transfer_concept=concept,
                                         transfer_type=transfer_type,
                                         transfer_date=date,
                                         transfer_amount=amount)

            my_request.save_transfer()
            return my_request.transfer_code

        def deposit_into_account(self, input_file:str)->str:
            """manages the deposits received for accounts"""
            deposit_obj = AccountDeposit.get_account_deposit_from_file(input_file)
            deposit_obj.save_deposit()
            return deposit_obj.deposit_signature

        def calculate_balance(self, iban:str)->bool:
            """calculate the balance for a given iban"""
            iban_balance = IbanBalance(iban)
            iban_balance.save_balance()
            return True

        def delete_transactions(self, IBAN: str, amount: int) -> float:
            """Deletes transactions for an IBAN based on the given amount"""
            # Validate IBAN format and control digit
            try:
                iban_obj = IbanCode(IBAN)
                iban = iban_obj.value
            except AccountManagementException:
                raise AccountManagementException("Invalid IBAN format")

            # Validate amount range
            if not isinstance(amount, int) or amount < -5000 or amount > 5000:
                raise AccountManagementException("Invalid amount value")

            transactions_store = TransactionsJsonStore()
            transactions = transactions_store.find_all("IBAN", iban)

            if not transactions:
                raise AccountManagementException("No transactions for the given IBAN")

            # Determine transactions to delete
            if amount >= 0:
                to_delete = [tx for tx in transactions if float(tx["amount"]) >= amount]
            else:
                to_delete = [tx for tx in transactions if float(tx["amount"]) <= amount]

            if not to_delete:
                raise AccountManagementException("No transactions match the deletion criteria")

            # Delete matching transactions
            transactions_store.load_list_from_file()
            transactions_store._data_list = [tx for tx in transactions_store._data_list if
                                             tx not in to_delete]
            transactions_store.save_list_to_file()

            # Save deleted transactions
            deleted_file_path = os.path.join(JSON_FILES_PATH, "deleted_transactions.json")
            if os.path.exists(deleted_file_path):
                with open(deleted_file_path, "r", encoding="utf-8", newline="") as f:
                    deleted = json.load(f)
            else:
                deleted = []

            deleted.extend(to_delete)

            with open(deleted_file_path, "w", encoding="utf-8", newline="") as f:
                json.dump(deleted, f, indent=2)

            # Return updated balance
            iban_balance = IbanBalance(iban)
            return iban_balance._balance  # Or use a public method/property if preferred
    instance = None
    def __new__(cls):
        if not AccountManager.instance:
            AccountManager.instance = AccountManager.__AccountManager()
        return AccountManager.instance

    def __getattr__(self, item):
        return getattr(AccountManager.instance, item)

    def __setattr__(self, key, value):
        return setattr(AccountManager.instance,key,value)
