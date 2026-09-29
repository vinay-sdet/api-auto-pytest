# Restful-Booker API Test Framework

A small pytest-based framework for live API checks against the Restful-Booker
playground API. It uses `requests`, `jsonschema`, and Python's built-in logging.

## Setup

Use Python 3.10 or newer. Create and activate a virtual environment, then install
the dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

The example file contains the demo credentials documented by Restful-Booker.
For CI, set `API_BASE_URL`, `API_USERNAME`, and `API_PASSWORD` as environment
variables or repository secrets. `API_BASE_URL` defaults to the documented API
host if it is not set.

## Run

Run the complete live suite and create `report.html`:

```powershell
python -m pytest
```

Run only smoke checks or regression checks:

```powershell
python -m pytest -m smoke
python -m pytest -m regression
```

Live API calls are logged to the console at INFO and to
`logs/test_run.log` at DEBUG. The log file is overwritten for each pytest run.
Sensitive credential and token fields are masked in logs and failure details.

The tests create their own bookings and delete them during fixture teardown.
Because the target is a shared public playground service, a failed run or an
interrupted process can leave test data behind.