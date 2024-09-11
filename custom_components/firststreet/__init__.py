"""The FirstStreet integration."""
from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .firststreet_api import FirstStreetAPI, FirstStreetAPIError

PLATFORMS: list[str] = ["sensor"]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up FirstStreet from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    api = FirstStreetAPI()
    fsid = entry.data["fsid"]
    building_id = entry.data.get("building_id", 0)

    try:
        # Test the connection by fetching data
        await hass.async_add_executor_job(api.get_all_risk_data, fsid, building_id)
    except FirstStreetAPIError as err:
        _LOGGER.error("Failed to connect to FirstStreet API: %s", err.message)
        if err.details:
            _LOGGER.error("Error details: %s", err.details)
        raise ConfigEntryNotReady from err
    except Exception as err:
        _LOGGER.exception("Unexpected error setting up FirstStreet integration")
        raise ConfigEntryNotReady from err

    hass.data[DOMAIN][entry.entry_id] = api

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok