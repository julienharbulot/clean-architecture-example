from datetime import datetime
from unittest import TestCase

from src.adapters.user_repository_mem import UserRepositoryMem
from src.business_layer.activate_user.input_port import ActivateUserRequest
from src.business_layer.activate_user.use_case_impl import (
    ActivateUserUseCaseImpl,
)
from src.business_layer.activate_user.output_port import ActivateUserStatus
from src.business_layer.models import UserRequiredInfo
from src.utils import CaptureResponse


class TestActivateUser(TestCase):
    def test_happy_path(self):
        repo = UserRepositoryMem()
        user_id = repo.create_user(
            UserRequiredInfo("email", "name", datetime.now()),
            "security_id",
            activated=False,
        )

        use_case = ActivateUserUseCaseImpl(
            output_port=CaptureResponse(),
            repository=repo,
            timeout_policy=lambda x, y: False,
        )
        c = use_case(ActivateUserRequest(user_id, datetime.now()))
        self.assertEqual(c.response.status, ActivateUserStatus.ok)

    def test_user_not_found(self):
        repo = UserRepositoryMem()

        use_case = ActivateUserUseCaseImpl(
            output_port=CaptureResponse(),
            repository=repo,
            timeout_policy=lambda x, y: False,
        )
        c = use_case(ActivateUserRequest("xxx", datetime.now()))
        self.assertEqual(c.response.status, ActivateUserStatus.user_not_found)

    def test_user_already_activated(self):
        repo = UserRepositoryMem()
        user_id = repo.create_user(
            UserRequiredInfo("email", "name", datetime.now()),
            "security_id",
            activated=True,
        )

        use_case = ActivateUserUseCaseImpl(
            output_port=CaptureResponse(),
            repository=repo,
            timeout_policy=lambda x, y: False,
        )
        c = use_case(ActivateUserRequest(user_id, datetime.now()))
        self.assertEqual(c.response.status, ActivateUserStatus.already_activated)

    def test_user_timeout(self):
        repo = UserRepositoryMem()
        user_id = repo.create_user(
            UserRequiredInfo("email", "name", datetime.now()),
            "security_id",
            activated=False,
        )

        use_case = ActivateUserUseCaseImpl(
            output_port=CaptureResponse(),
            repository=repo,
            timeout_policy=lambda x, y: True,
        )
        c = use_case(ActivateUserRequest(user_id, datetime.now()))
        self.assertEqual(c.response.status, ActivateUserStatus.too_late)
