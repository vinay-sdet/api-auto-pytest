from typing import Any

import requests

from api.base_client import BaseClient


class AuthClient(BaseClient):
    def authenticate(self, username: str, password: str) -> requests.Response:
        return self.request(
            "POST",
            "/auth",
            json_body={"username": username, "password": password},
        )

    def login(self, username: str, password: str) -> str:
        response = self.authenticate(username, password)
        response.raise_for_status()
        token: Any = response.json().get("token")
        if not isinstance(token, str) or not token:
            raise ValueError("Authentication response did not contain a token")
        return token
