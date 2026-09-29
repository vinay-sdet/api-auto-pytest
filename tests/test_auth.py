import pytest

from config.settings import settings
from utils.schema_validator import validate_schema


@pytest.mark.smoke
def test_create_token(auth_client):
    username, password = settings.require_credentials()
    response = auth_client.authenticate(username, password)

    assert response.status_code == 200
    validate_schema(response.json(), "auth.json")
    assert response.json()["token"]


@pytest.mark.regression
def test_invalid_credentials_return_reason(auth_client):
    response = auth_client.authenticate("invalid-user", "invalid-password")

    assert response.status_code == 200
    assert response.json() == {"reason": "Bad credentials"}
