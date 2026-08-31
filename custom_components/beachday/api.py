"""Async client for Beach Day API."""

from __future__ import annotations

from typing import Any

import aiohttp
from aiohttp import ClientTimeout


class BeachDayApiError(Exception):
    """Raised when Beach Day API returns an error."""


class BeachDayApi:
    """Small API client kept independent from Home Assistant."""

    def __init__(self, api_key: str, base_url: str, beach_id: str | int) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._beach_id = beach_id

    async def async_get_beach(self) -> dict[str, Any]:
        """Fetch the selected beach and latest conditions."""
        url = f"{self._base_url}/beaches/{self._beach_id}/"
        headers = {"Authorization": f"Bearer {self._api_key}"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=ClientTimeout(total=30)) as response:
                    if response.status >= 400:
                        raise BeachDayApiError(f"API returned HTTP {response.status}")
                    payload = await response.json()
        except (aiohttp.ClientError, TimeoutError) as err:
            raise BeachDayApiError(str(err)) from err
        if not isinstance(payload, dict):
            raise BeachDayApiError("API returned an invalid response")
        return payload

    async def async_validate(self) -> None:
        """Validate credentials and beach ID by fetching the beach."""
        await self.async_get_beach()
