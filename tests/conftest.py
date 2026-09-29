import html
import json
from typing import Any

import pytest
import pytest_html

from api.auth_client import AuthClient
from api.bookings_client import BookingsClient
from config.settings import settings
from utils.logging_config import configure_file_logging
from utils.schema_validator import validate_schema

BOOKING_DATA: dict[str, Any] = {
    "firstname": "Taylor",
    "lastname": "Automation",
    "totalprice": 120,
    "depositpaid": True,
    "bookingdates": {"checkin": "2026-10-01", "checkout": "2026-10-05"},
    "additionalneeds": "Window seat",
}


def pytest_configure(config: pytest.Config) -> None:
    configure_file_logging()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]):
    outcome = yield
    report = outcome.get_result()
    exchanges = getattr(item, "_api_exchanges", [])
    if report.failed and exchanges and not getattr(item, "_api_report_attached", False):
        details = html.escape(json.dumps(exchanges, indent=2, default=str))
        report.extras = getattr(report, "extras", [])
        report.extras.append(
            pytest_html.extras.html(
                f"<h3>API request and response details</h3><pre>{details}</pre>"
            )
        )
        item._api_report_attached = True


@pytest.fixture(scope="session")
def auth_token() -> str:
    username, password = settings.require_credentials()
    client = AuthClient(settings.base_url)
    try:
        return client.login(username, password)
    finally:
        client.close()


@pytest.fixture
def auth_client(request: pytest.FixtureRequest) -> AuthClient:
    client = AuthClient(settings.base_url, request.node)
    yield client
    client.close()


@pytest.fixture
def booking_client(auth_token: str, request: pytest.FixtureRequest) -> BookingsClient:
    client = BookingsClient(settings.base_url, auth_token, request.node)
    yield client
    client.close()


@pytest.fixture
def anonymous_booking_client(request: pytest.FixtureRequest) -> BookingsClient:
    client = BookingsClient(settings.base_url, test_node=request.node)
    yield client
    client.close()


@pytest.fixture
def invalid_token_booking_client(request: pytest.FixtureRequest) -> BookingsClient:
    client = BookingsClient(settings.base_url, "invalid-token", request.node)
    yield client
    client.close()


@pytest.fixture
def created_booking(booking_client: BookingsClient) -> dict[str, Any]:
    response = booking_client.create_booking(BOOKING_DATA)
    payload = response.json()
    booking_id = payload.get("bookingid") if isinstance(payload, dict) else None
    try:
        assert response.status_code == 200, response.text
        validate_schema(payload, "create_booking.json")
        yield payload
    finally:
        if isinstance(booking_id, int):
            cleanup_response = booking_client.delete_booking(booking_id)
            if cleanup_response.status_code not in (200, 201, 404, 405):
                pytest.fail(
                    f"Booking cleanup failed with status {cleanup_response.status_code}"
                )
