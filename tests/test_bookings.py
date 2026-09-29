import pytest

from api.bookings_client import BookingsClient
from utils.schema_validator import validate_schema


@pytest.mark.smoke
def test_create_booking(created_booking):
    assert created_booking["bookingid"] > 0
    assert created_booking["booking"]["firstname"] == "Taylor"
    assert created_booking["booking"]["lastname"] == "Automation"


@pytest.mark.smoke
def test_get_booking(booking_client: BookingsClient, created_booking):
    response = booking_client.get_booking(created_booking["bookingid"])

    assert response.status_code == 200
    validate_schema(response.json(), "booking.json")
    assert response.json()["firstname"] == created_booking["booking"]["firstname"]


@pytest.mark.regression
def test_update_booking(booking_client: BookingsClient, created_booking):
    updated_booking = dict(created_booking["booking"])
    updated_booking["firstname"] = "Updated"

    response = booking_client.update_booking(
        created_booking["bookingid"], updated_booking
    )

    assert response.status_code == 200
    validate_schema(response.json(), "booking.json")
    assert response.json()["firstname"] == "Updated"


@pytest.mark.regression
def test_partial_update_booking(booking_client: BookingsClient, created_booking):
    response = booking_client.partial_update_booking(
        created_booking["bookingid"], {"additionalneeds": "Late checkout"}
    )

    assert response.status_code == 200
    validate_schema(response.json(), "booking.json")
    assert response.json()["additionalneeds"] == "Late checkout"


@pytest.mark.smoke
def test_delete_booking(booking_client: BookingsClient, created_booking):
    booking_id = created_booking["bookingid"]
    response = booking_client.delete_booking(booking_id)

    assert response.status_code == 201
    get_response = booking_client.get_booking(booking_id)
    assert get_response.status_code == 404


@pytest.mark.parametrize(
    "client_fixture", ["anonymous_booking_client", "invalid_token_booking_client"]
)
@pytest.mark.regression
def test_update_without_valid_token(
    request: pytest.FixtureRequest, client_fixture: str, created_booking
):
    client: BookingsClient = request.getfixturevalue(client_fixture)
    response = client.update_booking(
        created_booking["bookingid"], created_booking["booking"]
    )

    assert response.status_code == 403
    assert response.text == "Forbidden"


@pytest.mark.parametrize(
    "client_fixture", ["anonymous_booking_client", "invalid_token_booking_client"]
)
@pytest.mark.regression
def test_delete_without_valid_token(
    request: pytest.FixtureRequest, client_fixture: str, created_booking
):
    client: BookingsClient = request.getfixturevalue(client_fixture)
    response = client.delete_booking(created_booking["bookingid"])

    assert response.status_code == 403
    assert response.text == "Forbidden"


@pytest.mark.regression
def test_get_nonexistent_booking(booking_client: BookingsClient):
    response = booking_client.get_booking(0)

    assert response.status_code == 404
    assert response.text == "Not Found"
