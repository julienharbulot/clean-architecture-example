from dataclasses import dataclass
from typing import Generic

from src.business_layer.errors import Error, ErrorCode
from src.business_layer.get_user.input_port import GetUserRequest, T
from src.business_layer.get_user.output_port import (
    GetUserResponse,
    GetUserResponseListener,
)
from src.business_layer.ports import AuthorizationService, UserRepository


@dataclass
class GetUserUseCaseImpl(Generic[T]):
    output_port: GetUserResponseListener
    repository: UserRepository
    authorization: AuthorizationService

    def __call__(self, request: GetUserRequest) -> T:
        self.authorization.ensure_authorized(request.access_token, "get-user")

        user = self.repository.get_by_email(request.user_email)
        if user:
            return self.output_port(
                GetUserResponse(
                    user,
                    request.request_id,
                )
            )
        else:
            raise Error(ErrorCode.user_not_found)
