from copy import deepcopy
from datetime import datetime
from typing import Dict, Optional
from uuid import uuid1

from src.business_layer.errors import Error, ErrorCode
from src.business_layer.models import (
    ActivationData,
    SecurityId,
    User,
    UserId,
    UserRequiredInfo,
)
from src.business_layer.ports import UserRepository


class UserRepositoryMem(UserRepository):  # in memory
    def __init__(self):
        self.data: Dict[UserId, User] = {}
        self.email_to_id: Dict[str, UserId] = {}

    def _create_entry(self, user: User):
        self.data[user.id] = deepcopy(user)
        self.email_to_id[user.info.email.lower()] = user.id

    def _update(self, user: User):
        self.data[user.id] = deepcopy(user)

    def get_by_id(self, user_id: UserId) -> Optional[User]:
        return deepcopy(self.data.get(user_id))

    def get_by_email(self, email: str) -> Optional[User]:
        user_id = self.email_to_id.get(email.lower())
        if user_id:
            return self.get_by_id(user_id)
        return None

    def create_user(
        self,
        user_data: UserRequiredInfo,
        security_id: SecurityId,
        activated: bool = False,
    ) -> UserId:
        print(f"Create user: {user_data}")

        if self.get_by_email(user_data.email):
            raise Error(ErrorCode.user_exists)

        user_id = UserId(str(uuid1()))
        self._create_entry(
            User(
                user_id,
                user_data,
                security_id,
                activated,
                account_created_at=datetime.now(),
            )
        )

        return user_id

    def get_activation_data(self, user_id: UserId) -> Optional[ActivationData]:
        user = self.get_by_id(user_id)
        if user:
            return ActivationData(user.account_activated, user.account_created_at)
        return None

    def activate(self, user_id: UserId) -> None:
        user = self.get_by_id(user_id)
        if not user:
            raise Error(ErrorCode.user_not_found)

        user.account_activated = True
        self._update(user)
