from dataclasses import dataclass
from datetime import datetime

from typing_extensions import NewType

UserId = NewType("UserId", str)
SecurityId = NewType("SecurityId", str)
AccessToken = NewType("AccessToken", str)


@dataclass(eq=True)
class UserRequiredInfo:
    email: str
    name: str
    birthdate: datetime


@dataclass
class ActivationData:
    account_activated: bool
    account_created_at: datetime


@dataclass(eq=True)
class User:
    id: UserId
    info: UserRequiredInfo
    security_id: SecurityId
    account_activated: bool
    account_created_at: datetime
