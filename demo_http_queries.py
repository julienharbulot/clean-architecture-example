from datetime import datetime, timedelta
from src.business_layer.activate_user.use_case import ActivateUserRequest
from src.business_layer.create_user.use_case import CreateUserRequest
from src.business_layer.models import UserRequiredInfo
from pydantic.json import pydantic_encoder
import json
import requests


class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def post(endpoint, data):
    data = json.dumps(data, default=pydantic_encoder)
    print("-----------------------------------")
    print(f"{Color.BOLD}<-- POST {endpoint}{Color.END}\n", data)
    response = requests.post(
        f'http://127.0.0.1:8000{endpoint}',
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/json',
        },
        data=data
    )

    try:
        print(f"{Color.BOLD}--> RESPONSE: {response.status_code}{Color.END}")
        print(response.json())
        print("-----------------------------------")
        return response.json()
    except:
        return None


def get(endpoint, **kwargs):
    query_str = "&".join(f"{arg[0]}={arg[1]}" for arg in kwargs.items())
    print("-----------------------------------")
    print(f"{Color.BOLD}<-- GET {endpoint}{Color.END}\n", query_str)

    response = requests.get(
        f'http://127.0.0.1:8000{endpoint}?{query_str}',
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/json',
        },
    )
    try:
        print(f"{Color.BOLD}--> RESPONSE: {response.status_code}{Color.END}")
        print(response.json())
        print("-----------------------------------")
        return response.json()
    except:
        return None


if __name__=="__main__":
    get(
        "/user",
        user_email="bad_email@gmail.com",
        request_id="rid_42"
    )

    r = post(
        "/users/",
        CreateUserRequest(user_data=UserRequiredInfo(
            "email", "name", "pass", datetime.now()
        ))
    )

    r = post(
        "/users/",
        CreateUserRequest(user_data=UserRequiredInfo(
            "email@gmail.com", "name", "password9.", datetime.now() - timedelta(days = 365*20)
        ))
    )
    if type(r) is str:
        r = json.loads(r)

    if 'user_id' in r:
        post(
            "/user/activate",
            ActivateUserRequest(r['user_id'], datetime.now())
        )

    get(
        "/user",
        user_email="email@gmail.com",
        request_id="rid_42"
    )
