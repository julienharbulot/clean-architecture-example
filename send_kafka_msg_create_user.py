import json
from datetime import datetime, timedelta

import pydantic
from kafka import KafkaProducer
from pydantic.json import pydantic_encoder

from src.business_layer.create_user.input_port import CreateUserRequest
from src.business_layer.get_user.input_port import GetUserRequest
from src.business_layer.models import UserRequiredInfo

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
)

# ===============
CreateUserReq = pydantic.dataclasses.dataclass(CreateUserRequest)
data = dict(
    action="create_user",
    payload=CreateUserReq(
        user_data=UserRequiredInfo(
            "email@gmail.com",
            "name",
            datetime.now() - timedelta(minutes=60 * 24 * 365 * 18),
        ),
        password="p@ssw0rD.",
        request_id=5,
    ),
)
dumped = json.dumps(data, indent=4, default=pydantic_encoder).encode("utf-8")
producer.send("input", dumped).get(timeout=10)


# ==================

GetUserReq = pydantic.dataclasses.dataclass(GetUserRequest)

data = dict(
    action="get_user",
    payload=GetUserReq(
        user_email="email@gmail.com",
        access_token="static-access-token-1",
        request_id=42,
        ),
)
dumped = json.dumps(data, indent=4, default=pydantic_encoder).encode("utf-8")
producer.send("input", dumped).get(timeout=10)
