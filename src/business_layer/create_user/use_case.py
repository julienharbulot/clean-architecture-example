from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, TypeVar

from src.business_layer.errors import ErrorCode
from src.business_layer.models import UserRequiredInfo

T = TypeVar("T")


# ======================================================================
# Types used in the use-case interface and use-case interface definition


@dataclass
class CreateUserRequest:
    user_data: UserRequiredInfo
    request_id: str = ""


class CreateUserUseCase(ABC, Generic[T]):
    @abstractmethod
    def create_user(self, r: CreateUserRequest) -> T:
        pass

    @abstractmethod
    def validate_user_data(self, r: UserRequiredInfo) -> List[ErrorCode]:
        pass
