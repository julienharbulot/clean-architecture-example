from dataclasses import dataclass
from datetime import datetime


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
    id: str
    info: UserRequiredInfo
    account_activated: bool
    account_created_at: datetime
