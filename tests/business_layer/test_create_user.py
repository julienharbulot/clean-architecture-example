from typing import Callable
from unittest import TestCase
from unittest.mock import Mock

from src.business_layer.create_user.use_case_impl import CreateUserUseCaseImpl
from src.business_layer.errors import Error, ErrorCode
from src.utils import CaptureResponse


def mock_repository(side_effect: Callable[[], str]):
    repository = Mock()
    repository.create_user = Mock()
    repository.create_user.side_effect = lambda *a, **k: side_effect()
    return repository


class TestCreateUser(TestCase):
    def test_user_created(self):
        user_id = "test-user-id"
        repository = mock_repository(lambda: user_id)

        use_case = CreateUserUseCaseImpl(
            output_port=CaptureResponse(),
            user_repository=repository,
            system_error_code=ErrorCode.system_error,
            user_data_validation_policy=lambda user_data: [],
            password_encryption_policy=lambda x: x,
            send_activation_request=lambda x, y: None,
        )
        request = Mock()
        c = use_case.create_user(request)
        self.assertEqual(c.response.user_id, user_id)

    def test_invalid_user_data(self):
        error_codes = [ErrorCode.testing_error]
        repository = mock_repository(lambda: "user_id")

        use_case = CreateUserUseCaseImpl(
            output_port=CaptureResponse(),
            user_repository=repository,
            system_error_code=ErrorCode.system_error,
            user_data_validation_policy=lambda user_data: error_codes,
            password_encryption_policy=lambda x: x,
            send_activation_request=lambda x, y: None,
        )
        request = Mock()
        self.assertEqual(use_case.validate_user_data(request), error_codes)
        with self.assertRaises(Error) as context:
            use_case.create_user(request)
        self.assertEqual(context.exception.error_codes, error_codes)
