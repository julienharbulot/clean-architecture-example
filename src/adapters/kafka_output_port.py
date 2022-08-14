import json
from dataclasses import dataclass
from typing import Any, List

from kafka import KafkaProducer  # type: ignore
from pydantic.json import pydantic_encoder


@dataclass
class KafkaOutputPort:
    def __init__(
        self,
        topic: str,
        bootstrap_servers: List[str],
        timeout: int = 10,
    ):
        self._topic = topic
        self._bootstrap_servers = bootstrap_servers
        self._timeout = timeout
        self._producer = KafkaProducer(
            bootstrap_servers=["localhost:9092"],
            value_serializer=self._serialize,
        )

    def __call__(self, x: Any) -> None:
        self._producer.send(self._topic, x).get(timeout=self._timeout)

    @staticmethod
    def _serialize(x: Any):
        return json.dumps(
            x,
            default=pydantic_encoder,
            ensure_ascii=False,
            indent=None,
        ).encode("utf-8")
