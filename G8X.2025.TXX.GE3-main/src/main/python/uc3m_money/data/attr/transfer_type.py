"""Definition of transfer_type concept"""
from .attribute import Attribute

class TransferType(Attribute):
    """Definition of attribute Concept class"""
    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute TransferType init method"""
        self._validation_pattern = r"(ORDINARY|INMEDIATE|URGENT)"
        self._error_message = "Invalid transfer type"
        self._attr_value = self._validate(attr_value)
