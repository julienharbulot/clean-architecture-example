from src.adapters.authentication_service_mem import AuthenticationServiceMem
from src.adapters.authorization_service_impl import StaticAuthorizationService
from src.adapters.kafka_output_port import KafkaOutputPort
from src.adapters.user_repository_mem import UserRepositoryMem
from src.business_layer.activate_user.use_case_impl import ActivateUserUseCaseImpl
from src.business_layer.create_user.use_case_impl import CreateUserUseCaseImpl
from src.business_layer.errors import ErrorCode
from src.business_layer.get_user.use_case_impl import GetUserUseCaseImpl
from src.business_layer.policies import (
    create_user_data_validation_policy,
    user_activation_timeout_policy,
)
from src.controllers.kafka_controller import KafkaController


class KafkaApp:
    def __init__(self):
        bootstrap_servers = ["localhost:9092"]
        output_port = KafkaOutputPort("output", bootstrap_servers)
        self.user_repository = UserRepositoryMem()
        self.authentication_service = AuthenticationServiceMem()
        self.authorization_service = StaticAuthorizationService(
            {
                "static-access-token-1": {"get-user"},
                "static-access-token-2": set(),
            }
        )

        self.kafka_controller = KafkaController(
            "input",
            bootstrap_servers,
            self._create_user_use_case(output_port),
            self._activate_user_use_case(output_port),
            self._get_user_use_case(output_port),
            lambda e_code: output_port(f"Error: {e_code}"),
        )

    def run(self):
        self.kafka_controller.run()

    def _create_user_use_case(self, output_port):
        return CreateUserUseCaseImpl(
            output_port=output_port,
            user_repository=self.user_repository,
            auth_service=self.authentication_service,
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


if __name__ == "__main__":
    app = KafkaApp()
    app.run()
