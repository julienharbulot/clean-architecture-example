from datetime import datetime, timedelta
from src.business_layer.activate_user.input_port import ActivateUserRequest
from src.business_layer.create_user.input_port import CreateUserRequest
from src.business_layer.login.input_port import LoginRequest
from src.business_layer.models import UserRequiredInfo
from pydantic.json import pydantic_encoder
import json
import requests


class Color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def post(endpoint, data):
    data = json.dumps(data, default=pydantic_encoder)
    print("-----------------------------------")
    print(f"{Color.BOLD}<-- POST {endpoint}{Color.END}\n", data)
    response = requests.post(
        f"http://127.0.0.1:8000{endpoint}",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        data=data,
    )

    try:
        print(f"{Color.BOLD}--> RESPONSE: {response.status_code}{Color.END}")
        print(response.json())
        print("-----------------------------------")
        return response.json()
    except:
        return None


def get(endpoint, **kwargs):
    access_token = kwargs.get("access_token", "")
    if 'access_token' in kwargs:
        del kwargs['access_token']

    query_str = "&".join(f"{arg[0]}={arg[1]}" for arg in kwargs.items())
    print("-----------------------------------")
    print(f"{Color.BOLD}<-- GET {endpoint}{Color.END}\n", query_str, f"(access={access_token})")

    response = requests.get(
        f"http://127.0.0.1:8000{endpoint}?{query_str}",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "access-token": access_token,
        },
    )
    try:
        print(f"{Color.BOLD}--> RESPONSE: {response.status_code}{Color.END}")
        print(response.json())
        print("-----------------------------------")
        return response.json()
    except:
        return None


if __name__ == "__main__":
    r = post(
        "/users/",
        CreateUserRequest(
            user_data=UserRequiredInfo("email", "name", datetime.now()),
            password="pass",
        ),
    )

    r = post(
        "/users/",
        CreateUserRequest(
            user_data=UserRequiredInfo(
                "email@gmail.com",
                "name",
                datetime.now() - timedelta(days=365 * 20),
            ),
            password="password9.",
        ),
    )
    if type(r) is str:
        r = json.loads(r)

    if "user_id" in r:
        post("/user/activate", ActivateUserRequest(r["user_id"], datetime.now()))

    print("This request is not authorized since access_token is missing")
    get("/user", user_email="email@gmail.com", request_id="rid_42")

    print("Getting an access token")
    r = post("/login", LoginRequest(
        user_email="email@gmail.com",
        user_password="password9.",
    ))
    access_token = r['access_token']

    get("/user", user_email="email@gmail.com", request_id="rid_42", access_token=access_token)

