"""Definition of attribute concept"""
from .attribute import Attribute

class Concept(Attribute):
    """Definition of attribute Concept class"""
    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute concept init method"""
        self._validation_pattern = r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._error_message = "Invalid concept format"
        self._attr_value = self._validate(attr_value)
