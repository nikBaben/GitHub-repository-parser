import asyncio
from typing import Any, Self

import httpx

from infrastructure.github.config import settings


class BaseHttpClient:
    def __init__(self) -> None:
        """
        Базовый асинхронный HTTP-клиент 
        для выполнения запросов к внешним API.
        """
        self._client = httpx.AsyncClient()

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def get_json(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        retries: int = settings.DEFAULT_RETRIES,
        timeout: int = settings.DEFAULT_TIMEOUT,
    ) -> tuple[Any, dict[str, str]]:
        """
        Выполняет GET-запрос и возвращает JSON-ответ с заголовками.

        Поддерживает повторные попытки (retries) при возникновении
        secondary rate limit (HTTP 403), с линейной задержкой между попытками.
        """
        for attempt in range(retries):
            response = await self._client.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
            )

            if (
                response.status_code == 403
                and "secondary rate limit" in response.text.lower()
            ):
                wait_seconds = 8 * (attempt + 1)
                print(
                    f"[WARN] Secondary rate limit, "
                    f"sleep {wait_seconds}s: {response.url}"
                )
                await asyncio.sleep(wait_seconds)
                continue

            if response.status_code >= 400:
                print(f"[HTTP {response.status_code}] {response.url}")
                print("Body:", response.text[:400])
                print(
                    "X-RateLimit-Remaining:",
                    response.headers.get("X-RateLimit-Remaining"),
                )
                print(
                    "X-RateLimit-Reset:",
                    response.headers.get("X-RateLimit-Reset"),
                )
                response.raise_for_status()

            return response.json(), dict(response.headers)

        raise RuntimeError("HTTP request failed after retries")