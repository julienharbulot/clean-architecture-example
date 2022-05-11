import json
from datetime import datetime, timedelta

import pydantic
from kafka import KafkaProducer
from pydantic.json import pydantic_encoder

from src.business_layer.create_user.use_case import CreateUserRequest
from src.business_layer.models import UserRequiredInfo

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
)

Req = pydantic.dataclasses.dataclass(CreateUserRequest)

data = dict(
    action='create_user',
    payload=Req(
        user_data=UserRequiredInfo(
            "email@gmail.com",
            "name",
            "p@ssw0rD.",
            datetime.now() - timedelta(minutes=60*24*365*18),
        ),
        request_id=5,
    )
)

dumped = json.dumps(data, indent=4, default=pydantic_encoder).encode("utf-8")
producer.send('input', dumped).get(timeout=10)
# producer.flush()