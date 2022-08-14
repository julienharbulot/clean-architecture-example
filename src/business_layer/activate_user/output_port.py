from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Optional

from src.business_layer.activate_user.input_port import T

ActivateUserResponseListener = Callable[["ActivateUserResponse"], T]


class ActivateUserStatus(Enum):
    ok = auto()
    already_activated = auto()
    user_not_found = auto()
    too_late = auto()


@dataclass
class ActivateUserResponse:
    status: ActivateUserStatus
    request_id: Optional[str]
