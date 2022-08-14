from dataclasses import dataclass
from typing import Dict, Set

from src.business_layer.errors import Error, ErrorCode
from src.business_layer.models import AccessToken
from src.business_layer.ports import AuthenticationService, AuthorizationService


@dataclass
class AuthorizationServiceImpl(AuthorizationService):
    authentication: AuthenticationService

    def ensure_authorized(self, token: AccessToken, target: str) -> None:
        security_id = self.authentication.retrieve_identity(token)
        # check if security_id has the required roles here.
        del security_id


@dataclass
class StaticAuthorizationService(AuthorizationService):
    data: Dict[AccessToken, Set[str]]

    def ensure_authorized(self, token: AccessToken, target: str) -> None:
        if token not in self.data:
            raise Error(ErrorCode.unknown_access_token)

        if target not in self.data[token]:
            raise Error(ErrorCode.illegal_access)
