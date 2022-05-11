from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


# ======================================================================
# Types used in the use-case interface and use-case interface definition


@dataclass
class GetUserRequest:
    user_email: str
    request_id: str = ""


GetUserUseCase = Callable[[GetUserRequest], T]
