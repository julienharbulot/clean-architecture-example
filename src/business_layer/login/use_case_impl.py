from dataclasses import dataclass
from typing import Callable, Generic

from src.business_layer.errors import Error, ErrorCode
from src.business_layer.login.use_case import LoginRequest, T
from src.business_layer.models import AccessToken
from src.business_layer.ports import AuthenticationService, UserRepository


@dataclass
class LoginResponse:
    access_token: AccessToken
    request_id: str


LoginResponseListener = Callable[[LoginResponse], T]


@dataclass
class LoginUseCaseImpl(Generic[T]):
    authentication_service: AuthenticationService
    user_repository: UserRepository
    output_port: LoginResponseListener

    def __call__(self, request: LoginRequest) -> T:
        user = self.user_repository.get_by_email(request.user_email)
        if not user:
            raise Error(ErrorCode.user_not_found)
        if not user.account_activated:
            raise Error(ErrorCode.user_not_activated)

        token = self.authentication_service.authenticate(
            request.user_email, request.user_password
        )
        response = LoginResponse(
            access_token=token,
            request_id=request.request_id,
        )
        return self.output_port(response)
