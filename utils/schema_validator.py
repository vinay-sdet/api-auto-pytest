import json
from pathlib import Path
from typing import Any

from jsonschema import validate

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"


def validate_schema(response_json: Any, schema_name: str) -> None:
    schema_path = SCHEMA_DIR / schema_name
    with schema_path.open(encoding="utf-8") as schema_file:
        schema = json.load(schema_file)
    validate(instance=response_json, schema=schema)
