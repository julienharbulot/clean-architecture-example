from abc import ABC, abstractmethod
from typing import Optional

from src.business_layer.models import ActivationData, UserRequiredInfo, User, UserId


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user_data: UserRequiredInfo, activated: bool) -> UserId:
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
