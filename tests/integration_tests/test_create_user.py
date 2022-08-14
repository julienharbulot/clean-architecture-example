from datetime import datetime, timedelta
from unittest import TestCase

from src.adapters.authentication_service_mem import AuthenticationServiceMem
from src.adapters.user_repository_mem import UserRepositoryMem
from src.business_layer.create_user.input_port import CreateUserRequest
from src.business_layer.create_user.use_case_impl import CreateUserUseCaseImpl
from src.business_layer.errors import ErrorCode
from src.business_layer.models import UserRequiredInfo
from src.business_layer.policies import create_user_data_validation_policy
from src.utils import CaptureResponse
from tests.utils import assert_matching


class TestCreateUser(TestCase):
    def test_user_created(self):
        repository = UserRepositoryMem()
        capture = CaptureResponse()
        use_case = CreateUserUseCaseImpl(
            output_port=capture,
            user_repository=repository,
            system_error_code=ErrorCode.system_error,
            user_data_validation_policy=create_user_data_validation_policy,
            auth_service=AuthenticationServiceMem(),
            send_activation_request=lambda name, email: None,
        )
        user_data = UserRequiredInfo(
            "user.data@gmail.com",
            "John Doe",
            datetime.now() - timedelta(days=20 * 365),
        )
        request = CreateUserRequest(
            request_id="rid", user_data=user_data, password="Password1234."
        )
        use_case.create_user(request)
        saved_user = repository.get_by_email(user_data.email)
        assert_matching(saved_user, user_data, self.assertEqual)
        self.assertEqual(saved_user.id, capture.response.user_id)
