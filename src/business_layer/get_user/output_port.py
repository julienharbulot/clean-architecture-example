from dataclasses import dataclass
from typing import Callable

from src.business_layer.get_user.input_port import T
from src.business_layer.models import User


@dataclass
class GetUserResponse:
    user: User
    request_id: str


GetUserResponseListener = Callable[[GetUserResponse], T]
