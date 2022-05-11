from dataclasses import dataclass
from typing import Callable, Generic, Optional, Protocol

from src.business_layer.errors import Error, ErrorCode
from src.business_layer.get_user.use_case import GetUserRequest, T
from src.business_layer.models import User

# ==================================================
# Types used in the use-case constructor:


@dataclass
class GetUserResponse:
    user: User
    request_id: str


GetUserResponseListener = Callable[[GetUserResponse], T]


class UserRepository(Protocol):
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError


# ==================================================
# Use-case implementation


@dataclass
class GetUserUseCaseImpl(Generic[T]):
    output_port: GetUserResponseListener
    repository: UserRepository

    def __call__(self, request: GetUserRequest) -> T:
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
