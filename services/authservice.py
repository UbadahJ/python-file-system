from dataclasses import dataclass
from typing import Optional

from models.auth import Authentication


@dataclass
class AuthService:
    _auth: Authentication

    @staticmethod
    def init(auth: Authentication):
        global __locator
        __locator = AuthService(auth)

    @staticmethod
    def fetch_auth() -> Authentication:
        global __locator
        if __locator is None:
            raise AttributeError("Service not initialized")

        return __locator._auth


__locator: Optional[AuthService] = None
