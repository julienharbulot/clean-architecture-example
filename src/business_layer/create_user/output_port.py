from dataclasses import dataclass
from typing import Callable

from src.business_layer.create_user.input_port import T
from src.business_layer.models import UserId

CreateUserResponseListener = Callable[["CreateUserResponse"], T]


@dataclass
class CreateUserResponse:
    user_id: UserId
    request_id: str
