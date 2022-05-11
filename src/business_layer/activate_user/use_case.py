from dataclasses import dataclass
from datetime import datetime
from typing import Callable, TypeVar

# ======================================================================
# Types used in the use-case interface and use-case interface definition


@dataclass
class ActivateUserRequest:
    user_id: str
    activated_at: datetime
    request_id: str = ""


T = TypeVar("T")
ActivateUserUseCase = Callable[[ActivateUserRequest], T]
