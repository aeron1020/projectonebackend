from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password

def validate_password_strength(value):
    try:
        validate_password(value)
    except ValidationError as e:
        raise ValidationError({'password': e.messages})
