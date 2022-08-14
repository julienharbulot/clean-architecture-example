from dataclasses import dataclass
from typing import Callable, List, Optional

from src.business_layer.create_user.use_case import (
    CreateUserRequest,
    CreateUserUseCase,
    T,
)
from src.business_layer.errors import Error, ErrorCode
from src.business_layer.models import UserId, UserRequiredInfo

# ==================================================
# Types used in the use-case constructor:
from src.business_layer.ports import AuthenticationService, UserRepository

CreateUserResponseListener = Callable[["CreateUserResponse"], T]
CreateUserDataValidationPolicy = Callable[[UserRequiredInfo], List[ErrorCode]]
ActivationRequestSender = Callable[[str, str], None]


@dataclass
class CreateUserResponse:
    user_id: UserId
    request_id: str


# ==================================================
# Use-case implementation


@dataclass
class CreateUserUseCaseImpl(CreateUserUseCase[T]):
    output_port: CreateUserResponseListener
    user_repository: UserRepository
    auth_service: AuthenticationService
    system_error_code: ErrorCode
    user_data_validation_policy: CreateUserDataValidationPolicy
    send_activation_request: ActivationRequestSender

    def create_user(self, r: CreateUserRequest) -> T:
        error_code = self.validate_user_data(r.user_data, r.password)
        if error_code:
            raise Error(error_code)

        user_data = r.user_data
        security_id = self.auth_service.create_user(user_data.email, r.password)
        user_id = self.user_repository.create_user(
            user_data, security_id, activated=False
        )

        self.send_activation_request(user_data.name, user_data.email)

        return self.output_port(CreateUserResponse(user_id, r.request_id))

    def validate_user_data(
        self, data: UserRequiredInfo, password: Optional[str]
    ) -> List[ErrorCode]:
        errors = self.user_data_validation_policy(data)
        if password:
            errors.extend(self.auth_service.validate_password(password))
        return errors
