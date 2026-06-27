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
                    raw = await response.json()

                    if not isinstance(raw, list):
                        _LOGGER.error("Expected a list from API, got: %s", type(raw))
                        return []

                    # The API returns PascalCase keys; normalise to camelCase so
                    # field names match the sensor descriptions (e.g. Id → id).
                    data = [_to_camel_case(device) for device in raw]

                    if data:
                        _LOGGER.debug("Raw keys on first device: %s", list(raw[0].keys()))

                    _LOGGER.debug(
                        "API returned %d device(s): %s",
                        len(data),
                        [
                            {"id": d.get("id"), "name": d.get("name"), "serial": d.get("serial")}
                            for d in data
                        ],
                    )
                    return data
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with smart-me API: {err}") from err


def _to_camel_case(device: dict) -> dict:
    """Lower-case the first character of every key (PascalCase → camelCase)."""
    return {k[0].lower() + k[1:] if k else k: v for k, v in device.items()}
