from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Callable, Generic, Optional

from src.business_layer.activate_user.use_case import ActivateUserRequest, T

# ==================================================
# Types used in the use-case constructor:
from src.business_layer.ports import UserRepository

UserActivationTimeoutPolicy = Callable[[datetime, datetime], bool]
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


# ==================================================
# Use-case implementation


@dataclass
class ActivateUserUseCaseImpl(Generic[T]):
    output_port: ActivateUserResponseListener
    repository: UserRepository
    timeout_policy: UserActivationTimeoutPolicy

    def __call__(self, r: ActivateUserRequest) -> T:
        def output(status: ActivateUserStatus):
            return self.output_port(ActivateUserResponse(status, r.request_id))

        data = self.repository.get_activation_data(r.user_id)

        if not data:
            return output(ActivateUserStatus.user_not_found)

        if data.account_activated:
            return output(ActivateUserStatus.already_activated)

        if self.timeout_policy(data.account_created_at, r.activated_at):
            return output(ActivateUserStatus.too_late)

        self.repository.activate(r.user_id)
        return output(ActivateUserStatus.ok)
