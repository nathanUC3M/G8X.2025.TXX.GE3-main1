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
from uc3m_money.data.transaction_deletion import TransactionDeletion


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
            return TransactionDeletion(IBAN, amount).execute()
    instance = None
    def __new__(cls):
        if not AccountManager.instance:
            AccountManager.instance = AccountManager.__AccountManager()
        return AccountManager.instance

    def __getattr__(self, item):
        return getattr(AccountManager.instance, item)

    def __setattr__(self, key, value):
        return setattr(AccountManager.instance,key,value)
