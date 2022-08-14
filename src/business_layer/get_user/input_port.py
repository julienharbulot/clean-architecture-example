from dataclasses import dataclass
from typing import Callable, TypeVar

from src.business_layer.models import AccessToken

T = TypeVar("T")


# ======================================================================
# Types used in the use-case interface and use-case interface definition


@dataclass
class GetUserRequest:
    user_email: str
    access_token: AccessToken
    request_id: str = ""


GetUserUseCase = Callable[[GetUserRequest], T]
