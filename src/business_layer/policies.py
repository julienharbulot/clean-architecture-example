import re
from datetime import datetime, timedelta
from typing import List

from src.business_layer.errors import ErrorCode
from src.business_layer.models import UserRequiredInfo


def create_user_data_validation_policy(user_data: UserRequiredInfo):
    error_codes = []
    error_codes.extend(birthdate_validation_policy(user_data.birthdate))
    error_codes.extend(email_validation_policy(user_data.email))
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
