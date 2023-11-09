import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug(f"loaded")

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, HomeAssistant
from homeassistant.const import CONF_ENTITY_ID
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.components.sensor import SensorEntity

from .const import (
    CONF_FLOW_ARRIVAL_STATION,
    CONF_FLOW_DEPARTURE_STATION,
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Initialize PublicTransportIDOS config entry."""
    registry = er.async_get(hass)
    # TODO Optionally validate config entry options before creating entity
    name = f"Name: {config_entry.title}"
    unique_id = f"{config_entry.entry_id}-sensor"
    departure_station = config_entry.data[CONF_FLOW_DEPARTURE_STATION]
    arrival_station = config_entry.data[CONF_FLOW_ARRIVAL_STATION]

    async_add_entities([PublicTransportIDOSSensor(unique_id, name, departure_station, arrival_station)])


class PublicTransportIDOSSensor(SensorEntity):
    """PublicTransportIDOS Sensor."""

    _unrecorded_attributes = frozenset(
        {
            "departure_station",
            "arrival_station",
        }
    )

    def __init__(self, unique_id: str, name: str, departure_station: str, arrival_station: str) -> None:
        """Initialize PublicTransportIDOS Sensor."""
        super().__init__()
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._departure_station = departure_station
        self._arrival_station = arrival_station
        self._state = "Does not matter in sensor - returns _attr_native_value"
        self._attr_native_value="Whee"
        _LOGGER.debug(f"{__name__}:PublicTransportIDOSSensor:__init__")

    async def async_update(self):
        # Implement web scraping and data retrieval here
        # Update self._state with the gathered data
        _LOGGER.debug(f"{__name__}:PublicTransportIDOSSensor:async_update")

    @property
    def departure_station(self):
        return self._departure_station

    @property
    def arrival_station(self):
        return self._arrival_station

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the sun."""
        return {
            "departure_station": self.departure_station,
            "arrival_station": self.arrival_station,
        }
