from dataclasses import dataclass
from datetime import datetime
from typing_extensions import NewType


UserId = NewType("UserId", str)


@dataclass(eq=True)
class UserRequiredInfo:
    email: str
    name: str
    password: str
    birthdate: datetime


@dataclass
class ActivationData:
    account_activated: bool
    account_created_at: datetime


@dataclass(eq=True)
class User:
    id: UserId
    info: UserRequiredInfo
    account_activated: bool
    account_created_at: datetime
