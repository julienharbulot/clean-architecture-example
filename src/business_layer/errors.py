from enum import Enum, auto
from typing import List, Union


class ErrorCode(Enum):
    ok = auto()
    system_error = auto()
    testing_error = auto()

    # age validation
    less_than_18_years_old = auto()
    more_than_100_years_old = auto()

    # email validation
    email_invalid = auto()

    # password validation
    password_does_not_contain_number = auto()
    password_does_not_contain_char = auto()
    password_is_less_than_8_chars = auto()

    # user repository
    user_exists = auto()
    user_not_found = auto()

    def __bool__(self):
        return self != ErrorCode.ok

    def __repr__(self):
        return self.name


class Error(Exception):
    def __init__(self, error_codes: Union[ErrorCode, List[ErrorCode]]):
        if isinstance(error_codes, ErrorCode):
            error_codes = [error_codes]

        super().__init__(self, f"Error{error_codes}")
        self.error_codes = error_codes
