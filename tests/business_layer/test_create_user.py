from datetime import datetime, timedelta
from unittest import TestCase

from src.adapters.authentication_service_mem import AuthenticationServiceMem
from src.adapters.user_repository_mem import UserRepositoryMem
from src.business_layer.create_user.use_case import CreateUserRequest
from src.business_layer.create_user.use_case_impl import CreateUserUseCaseImpl
from src.business_layer.errors import Error, ErrorCode
from src.business_layer.models import UserRequiredInfo
from src.utils import CaptureResponse

request = CreateUserRequest(
    user_data=UserRequiredInfo(
        email="email",
        name="Firstname Lastname",
        birthdate=datetime.now() - timedelta(days=10 * 365),
    ),
    password="password",
)


class TestCreateUser(TestCase):
    def test_user_created(self):
        repository = UserRepositoryMem()
        auth_service = AuthenticationServiceMem(password_validator=lambda password: [])

        use_case = CreateUserUseCaseImpl(
            output_port=CaptureResponse(),
            user_repository=repository,
            system_error_code=ErrorCode.system_error,
            user_data_validation_policy=lambda user_data: [],
            auth_service=auth_service,
            send_activation_request=lambda x, y: None,
        )
        c = use_case.create_user(request)

        user = repository.get_by_email(request.user_data.email)
        self.assertEqual(c.response.user_id, user.id)

    def test_invalid_user_data(self):
        error_codes = [ErrorCode.testing_error]
        repository = UserRepositoryMem()

        use_case = CreateUserUseCaseImpl(
            output_port=CaptureResponse(),
            user_repository=repository,
            auth_service=AuthenticationServiceMem(lambda p: []),
            system_error_code=ErrorCode.system_error,
            user_data_validation_policy=lambda user_data: error_codes,
            send_activation_request=lambda x, y: None,
        )
        self.assertEqual(
            use_case.validate_user_data(request.user_data, request.password),
            error_codes,
        )
        with self.assertRaises(Error) as context:
            use_case.create_user(request)
        self.assertEqual(context.exception.error_codes, error_codes)
