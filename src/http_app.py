from typing import Optional

import uvicorn  # type: ignore
from fastapi import FastAPI

from src.adapters.authentication_service_mem import AuthenticationServiceMem
from src.adapters.authorization_service_impl import AuthorizationServiceImpl
from src.adapters.user_repository_mem import UserRepositoryMem
from src.business_layer.activate_user.use_case_impl import ActivateUserUseCaseImpl
from src.business_layer.create_user.use_case_impl import CreateUserUseCaseImpl
from src.business_layer.errors import ErrorCode
from src.business_layer.get_user.use_case_impl import GetUserUseCaseImpl
from src.business_layer.login.use_case_impl import LoginUseCaseImpl
from src.business_layer.policies import (
    create_user_data_validation_policy,
    user_activation_timeout_policy,
)
from src.controllers.http_controller import HttpOutputAdapter, make_http_controller


class HttpApp:
    def __init__(self):
        self.http_controller: Optional[FastAPI] = None
        self.user_repository = UserRepositoryMem()
        self.auth_service = AuthenticationServiceMem()
        self.authorization_service = AuthorizationServiceImpl(self.auth_service)

    def run(self):
        self.run_http_app()

    def run_http_app(self):
        output_adapter = HttpOutputAdapter()
        self.http_controller = make_http_controller(
            user_creator=self._create_user_use_case(output_port=output_adapter),
            activate_user=self._activate_user_use_case(output_port=output_adapter),
            get_user=self._get_user_use_case(output_port=output_adapter),
            login=self._login(output_port=output_adapter),
        )
        uvicorn.run(self.http_controller, host="127.0.0.1", port=8000, log_level="info")  # type: ignore

    def _create_user_use_case(self, output_port):
        return CreateUserUseCaseImpl(
            output_port=output_port,
            user_repository=self.user_repository,
            auth_service=self.auth_service,
            system_error_code=ErrorCode.system_error,
            user_data_validation_policy=create_user_data_validation_policy,
            send_activation_request=lambda name, email: None,
        )

    def _activate_user_use_case(self, output_port):
        return ActivateUserUseCaseImpl(
            output_port=output_port,
            repository=self.user_repository,
            timeout_policy=user_activation_timeout_policy,
        )

    def _get_user_use_case(self, output_port):
        return GetUserUseCaseImpl(
            output_port=output_port,
            repository=self.user_repository,
            authorization=self.authorization_service,
        )

    def _login(self, output_port):
        return LoginUseCaseImpl(
            authentication_service=self.auth_service,
            user_repository=self.user_repository,
            output_port=output_port,
        )


if __name__ == "__main__":
    app = HttpApp()
    app.run()
