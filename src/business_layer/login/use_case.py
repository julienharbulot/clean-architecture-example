from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


@dataclass
class LoginRequest:
    user_email: str
    user_password: str
    request_id: str = ""


LoginUseCase = Callable[[LoginRequest], T]
