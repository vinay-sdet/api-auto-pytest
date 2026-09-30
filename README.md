# Restful-Booker API Test Framework

A pytest framework for live API checks against the [Restful-Booker API](https://restful-booker.herokuapp.com).
It uses Python, `requests`, `jsonschema`, and Python's built-in logging. The API
documentation is the source of truth for endpoint behavior:
[Restful-Booker API docs](https://restful-booker.herokuapp.com/apidoc/index.html).

## Project Layout

```text
api/       Reusable authentication, HTTP, and booking clients
config/    Environment-based settings
schemas/   JSON schemas for authentication and booking responses
tests/     Shared pytest fixtures and API tests
utils/     Schema validation and file logging
logs/      Runtime log output (ignored by Git)
```

`tests/conftest.py` provides a session-scoped auth token, per-test clients, and a
booking fixture that removes created data after each test. Auth and booking
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

Set `API_BASE_URL`, `API_USERNAME`, and `API_PASSWORD` in `.env` for local runs.
The example file uses the demo credentials documented by Restful-Booker;
`.env` is excluded from Git. The base URL defaults to
`https://restful-booker.herokuapp.com`.

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

The suite checks token creation and invalid credentials; booking creation,
retrieval, full update, partial update, and deletion; missing and invalid tokens
for protected operations; and retrieval of a nonexistent booking. The create
and get responses are schema-validated.

## CI

Install dependencies and run `python -m pytest` in the CI job. Provide
`API_USERNAME` and `API_PASSWORD` as CI environment variables or repository
secrets; optionally override `API_BASE_URL`. Preserve `report.html` as a CI
artifact so the test report is available after the job completes.

## Logs and Reports

Pytest prints live API progress at INFO level. Detailed request and response
data is written at DEBUG level to `logs/test_run.log`, which is overwritten at
the start of each run. Sensitive values such as passwords, tokens, authorization
headers, and cookies are masked. Failed tests include the recorded API exchange
details in the self-contained HTML report.

## Live API Notes

Tests call the shared public playground API and create real bookings. Fixtures
delete their own bookings during teardown, but an interrupted process or an API
failure can leave test data behind. Avoid running destructive tests against a
production service by changing `API_BASE_URL` only to an environment intended
for testing.