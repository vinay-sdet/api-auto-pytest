import json
import logging
import time
from typing import Any

import requests

LOGGER = logging.getLogger("api_client")
SENSITIVE_KEYS = ("password", "token", "authorization", "cookie")


def mask_sensitive(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: (
                "[REDACTED]"
                if any(secret in str(key).lower() for secret in SENSITIVE_KEYS)
                else mask_sensitive(item)
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [mask_sensitive(item) for item in value]
    return value


def _response_body(response: requests.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return response.text


class BaseClient:
    def __init__(self, base_url: str, test_node: Any = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.test_node = test_node

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
    ) -> requests.Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        started_at = time.perf_counter()

        try:
            response = self.session.request(
                method,
                url,
                json=json_body,
                headers=headers,
                cookies=cookies,
                timeout=30,
            )
        except requests.RequestException:
            elapsed_ms = round((time.perf_counter() - started_at) * 1000, 2)
            LOGGER.info("%s %s -> NO RESPONSE", method.upper(), url)
            LOGGER.debug(
                "request headers=%s body=%s response headers=%s body=%s time_ms=%s",
                mask_sensitive(headers or {}),
                mask_sensitive(json_body),
                {},
                "<no response>",
                elapsed_ms,
            )
            raise

        elapsed_ms = round((time.perf_counter() - started_at) * 1000, 2)
        request_headers = mask_sensitive(dict(response.request.headers))
        request_body = mask_sensitive(json_body)
        response_headers = mask_sensitive(dict(response.headers))
        response_body = mask_sensitive(_response_body(response))
        details = {
            "method": method.upper(),
            "url": url,
            "status_code": response.status_code,
            "request_headers": request_headers,
            "request_body": request_body,
            "response_headers": response_headers,
            "response_body": response_body,
            "response_time_ms": elapsed_ms,
        }

        LOGGER.info("%s %s -> %s", method.upper(), url, response.status_code)
        LOGGER.debug("API exchange: %s", json.dumps(details, default=str))
        if self.test_node is not None:
            exchanges = getattr(self.test_node, "_api_exchanges", [])
            exchanges.append(details)
            self.test_node._api_exchanges = exchanges
        return response

    def close(self) -> None:
        self.session.close()
