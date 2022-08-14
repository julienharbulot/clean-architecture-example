import base64
import hashlib
import hmac
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Dict, List
from uuid import uuid4

from src.business_layer.errors import Error, ErrorCode
from src.business_layer.models import AccessToken, SecurityId
from src.business_layer.ports import AuthenticationService


def password_validation_policy(password: str) -> List[ErrorCode]:
    error_codes = []
    if len(password) < 8:
        error_codes.append(ErrorCode.password_is_less_than_8_chars)
    if not re.search(r"[a-zA-Z]", password):
        error_codes.append(ErrorCode.password_does_not_contain_char)
    if not re.search(r"[0-9]", password):
        error_codes.append(ErrorCode.password_does_not_contain_number)
    return error_codes


@dataclass
class _SecurityRecord:
    hashed_password: str
    security_id: SecurityId


@dataclass
class _AccessRecord:
    username: str
    expire_at: datetime


class AuthenticationServiceMem(AuthenticationService):
    def __init__(
        self,
        password_validator: Callable[
            [str], List[ErrorCode]
        ] = password_validation_policy,
    ):
        self.password_validator = password_validator
        self.data: Dict[str, _SecurityRecord] = {}
        self.access_tokens: Dict[AccessToken, _AccessRecord] = {}

    def create_user(self, username: str, password: str) -> SecurityId:
        if username in self.data:
            raise Error(ErrorCode.user_exists)
        self.data[username] = _SecurityRecord(
            PasswordUtils.hash_password(password),
            SecurityId(f"security-id-{username}"),
        )
        return self.data[username].security_id

    def validate_password(self, password: str) -> List[ErrorCode]:
        return self.password_validator(password)

    def authenticate(self, username: str, password: str) -> AccessToken:
        if username not in self.data:
            raise Error(ErrorCode.user_not_found)

        data = self.data[username]
        if PasswordUtils.is_correct_password(data.hashed_password, password):
            access_token = AccessToken(str(uuid4()))
            self.access_tokens[access_token] = _AccessRecord(
                username=username, expire_at=datetime.now() + timedelta(hours=2)
            )
            return access_token
        else:
            raise Error(ErrorCode.wrong_password)

    def retrieve_identity(self, access_token: AccessToken) -> SecurityId:
        if access_token not in self.access_tokens:
            raise Error(ErrorCode.unknown_access_token)
        username = self.access_tokens[access_token].username
        return self.data[username].security_id


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
