"""Platform for sensor integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN
from .firststreet_api import FirstStreetAPI

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=1)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the FirstStreet sensor platform."""
    api: FirstStreetAPI = hass.data[DOMAIN][config_entry.entry_id]
    fsid = config_entry.data["fsid"]
    building_id = config_entry.data.get("building_id", 0)

    coordinator = FirstStreetDataUpdateCoordinator(hass, api, fsid, building_id)

    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [
            FirstStreetFloodSensor(coordinator),
            FirstStreetFireSensor(coordinator),
            FirstStreetHeatSensor(coordinator),
            FirstStreetWindSensor(coordinator),
            FirstStreetAirSensor(coordinator),
        ]
    )

class FirstStreetDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching FirstStreet data."""

    def __init__(self, hass, api, fsid, building_id):
        """Initialize."""
        self.api = api
        self.fsid = fsid
        self.building_id = building_id

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from FirstStreet API."""
        try:
            return await self.hass.async_add_executor_job(
                self.api.get_all_risk_data, self.fsid, self.building_id
            )
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

class FirstStreetBaseSensor(CoordinatorEntity, SensorEntity):
    """Base representation of a FirstStreet Sensor."""

    def __init__(self, coordinator: FirstStreetDataUpdateCoordinator, risk_type: str):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._risk_type = risk_type

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"FirstStreet {self._risk_type.capitalize()}"

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{DOMAIN}_{self.coordinator.fsid}_{self._risk_type}"

    @property
    def state_class(self):
        """Return the state class of the sensor."""
        return SensorStateClass.MEASUREMENT

class FirstStreetFloodSensor(FirstStreetBaseSensor):
    """Representation of a FirstStreet Flood Sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator, "flood")

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data['flood']['flood_factor']

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data['flood']

class FirstStreetFireSensor(FirstStreetBaseSensor):
    """Representation of a FirstStreet Fire Sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator, "fire")

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data['fire']['fire_factor']

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data['fire']

class FirstStreetHeatSensor(FirstStreetBaseSensor):
    """Representation of a FirstStreet Heat Sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator, "heat")

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data['heat']['heat_factor']

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data['heat']

class FirstStreetWindSensor(FirstStreetBaseSensor):
    """Representation of a FirstStreet Wind Sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator, "wind")

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data['wind']['wind_factor']

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data['wind']

class FirstStreetAirSensor(FirstStreetBaseSensor):
    """Representation of a FirstStreet Air Quality Sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator, "air")

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data['air']['air_factor']

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data['air']