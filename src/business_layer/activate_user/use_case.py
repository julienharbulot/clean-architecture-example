from dataclasses import dataclass
from datetime import datetime
from typing import Callable, TypeVar

# ======================================================================
# Types used in the use-case interface and use-case interface definition
from src.business_layer.models import UserId


@dataclass
class ActivateUserRequest:
    user_id: UserId
    activated_at: datetime
    request_id: str = ""


T = TypeVar("T")
ActivateUserUseCase = Callable[[ActivateUserRequest], T]
