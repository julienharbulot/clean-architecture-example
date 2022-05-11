import re
from datetime import datetime, timedelta
from typing import List

from src.business_layer.errors import ErrorCode
from src.business_layer.models import UserRequiredInfo


def create_user_data_validation_policy(user_data: UserRequiredInfo):
    error_codes = []
    error_codes.extend(password_validation_policy(user_data.password))
    error_codes.extend(birthdate_validation_policy(user_data.birthdate))
    error_codes.extend(email_validation_policy(user_data.email))
    return error_codes


def password_validation_policy(password: str) -> List[ErrorCode]:
    error_codes = []
    if len(password) < 8:
        error_codes.append(ErrorCode.password_is_less_than_8_chars)
    if not re.search(r"[a-zA-Z]", password):
        error_codes.append(ErrorCode.password_does_not_contain_char)
    if not re.search(r"[0-9]", password):
        error_codes.append(ErrorCode.password_does_not_contain_number)
    return error_codes


def birthdate_validation_policy(d: datetime) -> List[ErrorCode]:
    days_per_year = 365
    if d > datetime.now() - timedelta(days=18 * days_per_year):
        return [ErrorCode.less_than_18_years_old]
    if d < datetime.now() - timedelta(days=100 * days_per_year):
        return [ErrorCode.more_than_100_years_old]
    return []


def email_validation_policy(email: str) -> List[ErrorCode]:
    r = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    if not re.fullmatch(r, email):
        return [ErrorCode.email_invalid]
    return []


def user_activation_timeout_policy(account_created_at: datetime, activation: datetime):
    return activation - account_created_at > timedelta(hours=72)
