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
from homeassistant.helpers.typing import UNDEFINED

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
    SensorDeviceClass,
)

from .const import (
    CONF_FLOW_ARRIVAL_STATION,
    CONF_FLOW_DEPARTURE_STATION,
)

# The _attr_... always take precedence, they are not overriden
# SensorEntityDescription's members:
    # key: str,
    # device_class: SensorDeviceClass | None = None,
    # entity_category: EntityCategory | None = None,
    # entity_registry_enabled_default: bool = True,
    # entity_registry_visible_default: bool = True,
    # force_update: bool = False,
    # icon: str | None = None,
    # has_entity_name: bool = False,
    # name: str | UndefinedType | None = UNDEFINED,
    # translation_key: str | None = None,
    # unit_of_measurement: None = None,
    # last_reset: datetime | None = None,
    # native_unit_of_measurement: str | None = None,
    # options: list[str] | None = None,
    # state_class: SensorStateClass | str | None = None,
    # suggested_display_precision: int | None = None,
    # suggested_unit_of_measurement: str | None = None      # Type override in SensorEntityDescription, use native_unit_of_measurement

IDOSSensorDescription1: SensorEntityDescription = SensorEntityDescription(
    # EntityDescription (device_class, translation_key and unit_of_measurement are overriden in SensorEntityDescription)
    key = "sensor1",                        # str
    translation_key = "connection",         # str | None
    # SensorEntityDescription:
    device_class = SensorDeviceClass.DURATION,  # SensorDeviceClass | None
    native_unit_of_measurement = "min",     # str | None
    state_class = SensorStateClass.MEASUREMENT, # SensorStateClass | str | None
    )

IDOSSensorDescription2: SensorEntityDescription = SensorEntityDescription(
    # EntityDescription (device_class, translation_key and unit_of_measurement are overriden in SensorEntityDescription)
    key = "sensor2",                        # str
    translation_key = "connection",         # str | None
    # SensorEntityDescription:
    device_class = SensorDeviceClass.DURATION,  # SensorDeviceClass | None
    native_unit_of_measurement = "min",     # str | None
    state_class = SensorStateClass.MEASUREMENT, # SensorStateClass | str | None
    )

IDOSSensorDescription3: SensorEntityDescription = SensorEntityDescription(
    # EntityDescription (device_class, translation_key and unit_of_measurement are overriden in SensorEntityDescription)
    key = "sensor3-rest",                   # str
    translation_key = "connection-rest",    # str | None
    # SensorEntityDescription:
    device_class = SensorDeviceClass.DURATION,  # SensorDeviceClass | None
    native_unit_of_measurement = "min",     # str | None
    state_class = SensorStateClass.MEASUREMENT, # SensorStateClass | str | None
    )

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Initialize PublicTransportIDOS config entry."""
    registry = er.async_get(hass)
    # TODO Optionally validate config entry options before creating entity

    entities = []

    name = f"Name: {config_entry.title} ({IDOSSensorDescription1.key})"
    unique_id = f"{config_entry.entry_id}-{IDOSSensorDescription1.key}"
    departure_station = config_entry.data[CONF_FLOW_DEPARTURE_STATION]
    arrival_station = config_entry.data[CONF_FLOW_ARRIVAL_STATION]
    entities.append(PublicTransportIDOSSensor(unique_id, name, departure_station, arrival_station, IDOSSensorDescription1))

    name = f"Name: {config_entry.title} ({IDOSSensorDescription2.key})"
    unique_id = f"{config_entry.entry_id}-{IDOSSensorDescription2.key}"
    entities.append(PublicTransportIDOSSensor(unique_id, name, departure_station, arrival_station, IDOSSensorDescription2))

    name = f"Name: {config_entry.title} ({IDOSSensorDescription3.key})"
    unique_id = f"{config_entry.entry_id}-{IDOSSensorDescription3.key}"
    entities.append(PublicTransportIDOSSensor(unique_id, name, departure_station, arrival_station, IDOSSensorDescription2, True))

    async_add_entities(entities)

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # If needed, implement async_will_remove_from_hass in Entity for cleanup of Entity data

class PublicTransportIDOSSensor(SensorEntity):
    """PublicTransportIDOS Sensor."""

    _unrecorded_attributes = frozenset(
        {
            "departure_station",
            "arrival_station",
            "native_value",
        }
    )

    def __init__(self, unique_id: str, name: str, departure_station: str, arrival_station: str, description: SensorEntityDescription, has_paged_connections: bool = False) -> None:
        """Initialize PublicTransportIDOS Sensor."""
        super().__init__()
        self.entity_description = description
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._departure_station = departure_station
        self._arrival_station = arrival_station
        self._state = "Does not matter in sensor - returns _attr_native_value"
        self._attr_native_value="5"
        self._has_paged_connections = has_paged_connections
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
        if not self._has_paged_connections:
            return {
                "departure_station": self.departure_station,
                "arrival_station": self.arrival_station,
            }

        return {"connections":
                [
                    {"connection":
                     {
                        "departure_station": self.departure_station,
                        "arrival_station": self.arrival_station
                     }
                    },
                    {"connection":
                     {
                        "departure_station": self.departure_station,
                        "arrival_station": self.arrival_station
                     }
                    }
                ]
            }
