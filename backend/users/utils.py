import re

from django.core.exceptions import ValidationError

from core.strings import INCORRECT_PHONE_NUMBER

PHONE_NUMBER_PATTERN = r"7\d{10}"


def validate_phone_number(phone_number: str) -> None:
    if not re.fullmatch(PHONE_NUMBER_PATTERN, phone_number):
        raise ValidationError(INCORRECT_PHONE_NUMBER)
