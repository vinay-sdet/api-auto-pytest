# Restful-Booker API Test Framework

A pytest framework for live API checks against the [Restful-Booker API](https://restful-booker.herokuapp.com).
It uses `requests`, `jsonschema`, `python-dotenv`, `pytest-html`, and Python's
built-in logging. The API documentation is the source of truth for endpoint
behavior:
[Restful-Booker API docs](https://restful-booker.herokuapp.com/apidoc/index.html).

## Project Layout

```text
api/        Reusable authentication, HTTP, and booking clients
config/     Environment-based settings
schemas/    JSON schemas for authentication and booking responses
tests/      Shared pytest fixtures and API tests
utils/      Schema validation and file logging
logs/       Runtime log output (ignored by Git)
pytest.ini  Test paths, markers, HTML report, and console logging
```

`tests/conftest.py` provides a session-scoped auth token, per-test clients, and a
booking fixture that removes created data after each test. Update, partial
update, and delete send that token as a `token` cookie. Create and get call the
API without a token. Each HTTP call times out after 30 seconds. Auth and booking
responses are validated against the schemas in `schemas/`.

## Setup

Use Python 3.10 or newer. Create and activate a virtual environment, then install
the dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `API_USERNAME` and `API_PASSWORD` in `.env`. The example file leaves those
values blank. Restful-Booker documents the demo account `admin` / `password123`.
`.env` is excluded from Git. `API_BASE_URL` is optional and defaults to
`https://restful-booker.herokuapp.com`. If either credential is missing, the
session fixture stops the run with:

```text
API_USERNAME and API_PASSWORD must be set in the environment or .env
```

## Run Tests

Run the full live suite and generate `report.html`:

```powershell
python -m pytest
```

Run a selected marker group:

```powershell
python -m pytest -m smoke
python -m pytest -m regression
```

`smoke` covers token creation, booking creation, retrieval, and deletion.
`regression` covers invalid credentials, full and partial updates, update and
delete with a missing or invalid token, and retrieval of a nonexistent booking.

Checked results:

- A valid login returns a token validated with `schemas/auth.json`.
- Invalid credentials return HTTP 200 and `{"reason": "Bad credentials"}`.
- Create responses are validated with `schemas/create_booking.json`.
- Get, full update, and partial update responses are validated with `schemas/booking.json`.
- Update or delete without a valid token returns `403` and `Forbidden`.
- Deleting an existing booking returns `201`. The following get returns `404`.
- Getting booking id `0` returns `404` and `Not Found`.

## CI

Install dependencies and run `python -m pytest` in the CI job. Provide
`API_USERNAME` and `API_PASSWORD` as CI environment variables or repository
secrets; optionally override `API_BASE_URL`. Preserve `report.html` as a CI
artifact so the test report is available after the job completes.

## Logs and Reports

Pytest prints live API progress at INFO level. Detailed request and response
data is written at DEBUG level to `logs/test_run.log`, which is overwritten at
the start of each run. Passwords, tokens, authorization headers, and cookies are
stored as `[REDACTED]` in the log and in report attachments. Failed tests include
the recorded API exchange details in the self-contained HTML report.

## Live API Notes

Tests call the shared public playground API and create real bookings. The
`created_booking` fixture deletes its booking during teardown and accepts cleanup
statuses 200, 201, 404, and 405. Any other cleanup status fails the test. An
interrupted process can still leave a booking behind. Point `API_BASE_URL` only
at an environment intended for testing.
