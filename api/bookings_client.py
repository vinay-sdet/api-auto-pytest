from typing import Any

import requests

from api.base_client import BaseClient


class BookingsClient(BaseClient):
    def __init__(
        self, base_url: str, token: str | None = None, test_node: Any = None
    ) -> None:
        super().__init__(base_url, test_node)
        self.token = token

    def _headers(self) -> dict[str, str]:
        return {"Accept": "application/json"}

    def _cookies(self) -> dict[str, str] | None:
        return {"token": self.token} if self.token else None

    def create_booking(self, booking: dict[str, Any]) -> requests.Response:
        return self.request(
            "POST", "/booking", json_body=booking, headers=self._headers()
        )

    def get_booking(self, booking_id: int) -> requests.Response:
        return self.request("GET", f"/booking/{booking_id}", headers=self._headers())

    def update_booking(
        self, booking_id: int, booking: dict[str, Any]
    ) -> requests.Response:
        return self.request(
            "PUT",
            f"/booking/{booking_id}",
            json_body=booking,
            headers=self._headers(),
            cookies=self._cookies(),
        )

    def partial_update_booking(
        self, booking_id: int, updates: dict[str, Any]
    ) -> requests.Response:
        return self.request(
            "PATCH",
            f"/booking/{booking_id}",
            json_body=updates,
            headers=self._headers(),
            cookies=self._cookies(),
        )

    def delete_booking(self, booking_id: int) -> requests.Response:
        return self.request(
            "DELETE",
            f"/booking/{booking_id}",
            headers=self._headers(),
            cookies=self._cookies(),
        )
