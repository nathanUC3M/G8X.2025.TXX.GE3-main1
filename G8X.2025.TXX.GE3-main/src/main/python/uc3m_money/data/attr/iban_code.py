"""Definition of attribute iban"""
from uc3m_money.exception.account_management_exception import AccountManagementException
from .attribute import Attribute


class IbanCode(Attribute):
    """Definition of attribute IbanCode class"""
    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute email init method"""
        self._validation_pattern = r"^ES[0-9]{22}"
        self._error_message = "Invalid IBAN format"
        self._attr_value = self._validate(attr_value)

    def _validate( self, attr_value ):
        """Overrides the validate method to include the validation of the
        IBAN control digits """
        attr_value = super()._validate(attr_value)
        iban = attr_value
        original_code = iban[2:4]
        iban = iban[:2] + "00" + iban[4:]
        iban = iban[4:] + iban[:4]
        # Convertir el IBAN en una cadena numérica, reemplazando letras por números
        iban = (iban.replace('A', '10').replace('B', '11').
                replace('C', '12').replace('D', '13').replace('E', '14').
                replace('F', '15'))
        iban = (iban.replace('G', '16').replace('H', '17').
                replace('I', '18').replace('J', '19').replace('K', '20').
                replace('L', '21'))
        iban = (iban.replace('M', '22').replace('N', '23').
                replace('O', '24').replace('P', '25').replace('Q', '26').
                replace('R', '27'))
        iban = (iban.replace('S', '28').replace('T', '29').replace('U', '30').
                replace('V', '31').replace('W', '32').replace('X', '33'))
        iban = iban.replace('Y', '34').replace('Z', '35')
        # Convertir la cadena en un número entero
        iban_number = int(iban)
        # Calcular el módulo 97
        iban_mod_97 = iban_number % 97
        # Calcular el dígito de control (97 menos el módulo)
        control_digit = 98 - iban_mod_97
        if int(original_code) != control_digit:
            raise AccountManagementException("Invalid IBAN control digit")
        return attr_value
