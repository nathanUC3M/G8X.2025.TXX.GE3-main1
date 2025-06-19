"""Contains the class OrderShipping"""
import json
from datetime import datetime, timezone
import hashlib
from uc3m_money.data.attr.iban_code import IbanCode
from uc3m_money.data.attr.deposit_amount import DepositAmount
from uc3m_money.exception.account_management_exception import AccountManagementException
from uc3m_money.storage.deposits_json_store import DepositsJsonStore


class AccountDeposit():
    """Class representing the information required for shipping of an order"""

    def __init__(self,
                 to_iban: str,
                 deposit_amount: float):
        self.__alg = "SHA-256"
        self.__type = "DEPOSIT"
        self.__to_iban = IbanCode(to_iban).value
        self.__deposit_amount = DepositAmount(deposit_amount).value
        justnow = datetime.now(timezone.utc)
        self.__deposit_date = datetime.timestamp(justnow)

    @classmethod
    def get_account_deposit_from_file(cls, input_file:str):
        """class method that returns a new instance of account deposit
        from the content of the input_file received as a parameter"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                input_data = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Error: file input not found") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # comprobar valores del fichero
        try:
            deposit_iban = input_data["IBAN"]
            deposit_amount = input_data["AMOUNT"]
        except KeyError as e:
            raise AccountManagementException("Error - Invalid Key in JSON") from e
        new_deposit = cls(to_iban=deposit_iban, deposit_amount=deposit_amount)
        return new_deposit

    def to_json(self):
        """returns the object data in json format"""
        return {"alg": self.__alg,
                "type": self.__type,
                "to_iban": self.__to_iban,
                "deposit_amount": self.__deposit_amount,
                "deposit_date": self.__deposit_date,
                "deposit_signature": self.deposit_signature}

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + str(self.__alg) +",typ:" + str(self.__type) +",iban:" + \
               str(self.__to_iban) + ",amount:" + str(self.__deposit_amount) + \
               ",deposit_date:" + str(self.__deposit_date) + "}"

    @property
    def to_iban(self):
        """Property that represents the product_id of the patient"""
        return self.__to_iban

    @to_iban.setter
    def to_iban(self, value):
        self.__to_iban = value

    @property
    def deposit_amount(self):
        """Property that represents the order_id"""
        return self.__deposit_amount
    @deposit_amount.setter
    def deposit_amount(self, value):
        self.__deposit_amount = value

    @property
    def deposit_date(self):
        """Property that represents the phone number of the client"""
        return self.__deposit_date
    @deposit_date.setter
    def deposit_date( self, value ):
        self.__deposit_date = value


    @property
    def deposit_signature( self ):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def save_deposit(self):
        """saves the deposit into the store"""
        deposits_storage = DepositsJsonStore()
        deposits_storage.add_item(self)
