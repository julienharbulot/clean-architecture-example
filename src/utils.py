import base64
import hashlib
import hmac
import threading
from dataclasses import dataclass
from typing import Any


class PasswordUtils:
    @classmethod
    def salt(cls):
        return bytes("SALT-EXAMPLE", "utf-8")

    @classmethod
    def hash_password(cls, password: str) -> str:
        h = hashlib.pbkdf2_hmac("sha256", password.encode(), cls.salt(), 100000)
        return base64.b64encode(h).decode("ascii")

    @classmethod
    def is_correct_password(cls, pw_hash: str, password: str) -> bool:
        h = base64.b64decode(pw_hash.encode("ascii"))
        return hmac.compare_digest(pw_hash, cls.hash_password(password))


@dataclass
class CapturedResponse:
    response: Any


class CaptureResponse:
    def __init__(self):
        self._data = threading.local()

    def __call__(self, response: Any) -> CapturedResponse:
        self._data.response = response
        return CapturedResponse(response)

    @property
    def response(self):
        return self._data.response
