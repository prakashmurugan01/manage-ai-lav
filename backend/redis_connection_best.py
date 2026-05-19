"""Production-ready Redis connection example.

Usage:
1) Set REDIS_URL in environment (prefer rediss:// for managed Redis providers).
2) Run: python redis_connection_best.py
"""

from __future__ import annotations

import os
import time

import redis


def get_redis_url() -> str:
    # Fallback keeps local development simple.
    return os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")


def connect_with_retry(url: str, retries: int = 5, delay_seconds: float = 1.5) -> redis.Redis:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            client = redis.from_url(
                url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                health_check_interval=30,
                retry_on_timeout=True,
            )
            client.ping()
            return client
        except Exception as exc:  # noqa: BLE001 - example script should show full failure context
            last_error = exc
            if attempt < retries:
                time.sleep(delay_seconds)
    raise RuntimeError(f"Redis connection failed after {retries} attempts") from last_error


def main() -> None:
    redis_url = get_redis_url()
    client = connect_with_retry(redis_url)

    ok = client.set("foo", "bar", ex=60)
    result = client.get("foo")

    print(f"Connected: {client.ping()}")
    print(f"SET foo: {ok}")
    print(f"GET foo: {result}")


if __name__ == "__main__":
    main()