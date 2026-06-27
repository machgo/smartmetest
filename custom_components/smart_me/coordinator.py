from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_BASE_URL, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class SmartMeDataUpdateCoordinator(DataUpdateCoordinator[list[dict]]):
    def __init__(self, hass: HomeAssistant, username: str, password: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self._username = username
        self._password = password

    async def _async_update_data(self) -> list[dict]:
        url = f"{API_BASE_URL}/Devices"
        _LOGGER.debug("Fetching devices from %s (user: %s)", url, self._username)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    auth=aiohttp.BasicAuth(self._username, self._password),
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    _LOGGER.debug(
                        "API response status: %s %s", response.status, response.reason
                    )
                    if response.status == 401:
                        raise ConfigEntryAuthFailed("Invalid credentials")
                    response.raise_for_status()
                    data = await response.json()
                    _LOGGER.debug(
                        "API returned %d device(s): %s",
                        len(data) if isinstance(data, list) else "N/A (not a list)",
                        [
                            {"id": d.get("id"), "name": d.get("name"), "serial": d.get("serial")}
                            for d in data
                        ]
                        if isinstance(data, list)
                        else data,
                    )
                    return data
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with smart-me API: {err}") from err
