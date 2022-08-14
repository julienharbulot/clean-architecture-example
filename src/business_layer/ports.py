from abc import ABC, abstractmethod
from typing import List, Optional

from src.business_layer.errors import ErrorCode
from src.business_layer.models import (
    AccessToken,
    ActivationData,
    SecurityId,
    User,
    UserId,
    UserRequiredInfo,
)


class UserRepository(ABC):
    @abstractmethod
    def create_user(
        self, user_data: UserRequiredInfo, security_id: SecurityId, activated: bool
    ) -> UserId:
        raise NotImplementedError

    @abstractmethod
    def get_activation_data(self, user_id: UserId) -> Optional[ActivationData]:
        raise NotImplementedError

    @abstractmethod
    def activate(self, user_id: UserId) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError


class AuthenticationService(ABC):
    @abstractmethod
    def create_user(self, username: str, password: str) -> SecurityId:
        raise NotImplementedError

    @abstractmethod
    def validate_password(self, password: str) -> List[ErrorCode]:
        raise NotImplementedError

    @abstractmethod
    def authenticate(self, username: str, password: str) -> AccessToken:
        raise NotImplementedError

    @abstractmethod
    def retrieve_identity(self, access_token: AccessToken) -> SecurityId:
        raise NotImplementedError


class AuthorizationService(ABC):
    @abstractmethod
    def ensure_authorized(self, token: AccessToken, target: str) -> None:
        raise NotImplementedError
