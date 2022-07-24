from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    NumericPasswordValidator,
    CommonPasswordValidator,
    MinimumLengthValidator,
)
from .custom_validators import (
    HasLowerCaseValidator,
    HasUpperCaseValidator,
    HasNumberValidator,
    HasSymbolValidator,
)


def similariy_validator(password, user):
    # THIS VALIDATOR HAS A SPECIAL PARAMETER: USER
    validator = UserAttributeSimilarityValidator()
    validator.validate(password, user=user)


def validate_minimum_length(password):
    validator = MinimumLengthValidator()
    validator.validate(password)


def validate_not_numeric(password):
    validator = NumericPasswordValidator()
    validator.validate(password)


def validate_not_common_password(password):
    validator = CommonPasswordValidator()
    validator.validate(password)


def has_lower_case(password):
    validator = HasLowerCaseValidator()
    validator.validate(password)


def has_upper_case(password):
    validator = HasUpperCaseValidator()
    validator.validate(password)


def has_number(password):
    validator = HasNumberValidator()
    validator.validate(password)


def has_symbol(password):
    validator = HasSymbolValidator()
    validator.validate(password)
