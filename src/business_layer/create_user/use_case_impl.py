from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, List, Protocol

from src.business_layer.create_user.use_case import (
    CreateUserRequest,
    CreateUserUseCase,
    T,
)
from src.business_layer.errors import Error, ErrorCode
from src.business_layer.models import UserRequiredInfo

# ==================================================
# Types used in the use-case constructor:


CreateUserResponseListener = Callable[["CreateUserResponse"], T]
CreateUserDataValidationPolicy = Callable[[UserRequiredInfo], List[ErrorCode]]
PasswordEncryptionPolicy = Callable[[str], str]
ActivationRequestSender = Callable[[str, str], None]


@dataclass
class CreateUserResponse:
    user_id: str
    request_id: str


class UserRepository(Protocol):
    def create_user(self, user_data: UserRequiredInfo, activated: bool) -> str:
        raise NotImplementedError


# ==================================================
# Use-case implementation


@dataclass
class CreateUserUseCaseImpl(CreateUserUseCase[T]):
    output_port: CreateUserResponseListener
    user_repository: UserRepository
    system_error_code: ErrorCode
    user_data_validation_policy: CreateUserDataValidationPolicy
    password_encryption_policy: PasswordEncryptionPolicy
    send_activation_request: ActivationRequestSender

    def create_user(self, r: CreateUserRequest) -> T:
        error_code = self.validate_user_data(r.user_data)
        if error_code:
            raise Error(error_code)

        user_data = deepcopy(r.user_data)
        user_data.password = self.password_encryption_policy(user_data.password)

        user_id = self.user_repository.create_user(user_data, activated=False)
        self.send_activation_request(user_data.name, user_data.email)

        return self.output_port(CreateUserResponse(user_id, r.request_id))

    def validate_user_data(self, data: UserRequiredInfo) -> List[ErrorCode]:
        return self.user_data_validation_policy(data)
