"""Definition of TransferDate concept"""
from uc3m_money.data.attr.attribute import Attribute
from uc3m_money.exception.account_management_exception import AccountManagementException

class TransferAmount(Attribute):
    """Definition of attribute TransferDate class"""
    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute TransferAmount init method"""
        #not necessary the regex
        self._error_message = "Invalid transfer amount"
        self._attr_value = self._validate(attr_value)

    def _validate( self, attr_value ):
        #not necessary the super() method
        try:
            amount_float = float(attr_value)
        except ValueError as exc:
            raise AccountManagementException(self._error_message) from exc
        amount_str = str(amount_float)
        if '.' in amount_str:
            decimal_part_len = len(amount_str.split('.')[1])
            if decimal_part_len > 2:
                raise AccountManagementException(self._error_message)
        if amount_float < 10 or amount_float > 10000:
            raise AccountManagementException(self._error_message)
        return attr_value
