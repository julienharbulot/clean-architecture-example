import json
from dataclasses import dataclass
from typing import Callable, List

import pydantic
from kafka import KafkaConsumer  # type: ignore

from src.business_layer.activate_user.input_port import (
    ActivateUserRequest,
    ActivateUserUseCase,
)
from src.business_layer.create_user.input_port import (
    CreateUserRequest,
    CreateUserUseCase,
)
from src.business_layer.errors import Error, ErrorCode
from src.business_layer.get_user.input_port import GetUserRequest, GetUserUseCase


@dataclass
class KafkaController:
    topic_name: str  # kafka-topic
    bootstrap_servers: List[str]  # ['localhost:9092']
    user_creator: CreateUserUseCase[None]
    activate_user: ActivateUserUseCase[None]
    get_user: GetUserUseCase[None]
    on_error: Callable[[ErrorCode], None]

    def run(self):
        consumer = KafkaConsumer(
            self.topic_name,
            bootstrap_servers=self.bootstrap_servers,
        )

        for record in consumer:
            value = record.value.decode("utf-8")
            print(f"Received message: {record}, {value}")
            msg = json.loads(value)

            try:
                if msg["action"] == "create_user":
                    self._create_user(msg["payload"])
                elif msg["action"] == "activate_user":
                    self._activate_user(msg["payload"])
                elif msg["action"] == "get_user":
                    self._get_user(msg["payload"])
                else:
                    self.on_error(ErrorCode.system_error)
            except Error as e:
                self.on_error(e.error_codes[0])

    def _create_user(self, payload):
        request = self._parse(CreateUserRequest, payload)
        self.user_creator.create_user(request)

    def _activate_user(self, payload):
        request = self._parse(ActivateUserRequest, payload)
        self.activate_user(request)

    def _get_user(self, payload):
        request = self._parse(GetUserRequest, payload)
        self.get_user(request)

    @staticmethod
    def _parse(cls, payload):
        return pydantic.dataclasses.dataclass(cls)(**payload)
