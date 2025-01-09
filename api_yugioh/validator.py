import re
from django.core.exceptions import ValidationError

def validate_password_strength(value):
    """
    Valida que la contraseña cumpla con los requisitos:
    - Al menos una letra mayúscula.
    - Al menos un número.
    - Al menos un símbolo.
    """
    if not re.search(r'[A-Z]', value):
        raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
    if not re.search(r'[0-9]', value):
        raise ValidationError("La contraseña debe contener al menos un número.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError("La contraseña debe contener al menos un símbolo especial.")
