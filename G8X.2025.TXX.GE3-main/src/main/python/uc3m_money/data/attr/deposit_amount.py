"""Definition of DepositAmmount """
from uc3m_money.exception.account_management_exception import AccountManagementException
from uc3m_money.data.attr.attribute import Attribute

class DepositAmount(Attribute):
    """Definition of attribute DepositAmount class"""
    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute TransferAmount init method"""
        #not necessary the regex
        self._validation_pattern = r"^EUR [0-9]{4}\.[0-9]{2}"
        self._error_message = "Error - Invalid deposit amount"
        self._attr_value = self._validate(attr_value)

    def _validate( self, attr_value ):
        attr_value = super()._validate(attr_value)
        float_value = float(attr_value[4:])
        if float_value == 0:
            raise AccountManagementException("Error - Deposit must be greater than 0")
        return float(float_value)
