from dataclasses import dataclass
from typing import Callable

from src.business_layer.login.input_port import T
from src.business_layer.models import AccessToken


@dataclass
class LoginResponse:
    access_token: AccessToken
    request_id: str


LoginResponseListener = Callable[[LoginResponse], T]
