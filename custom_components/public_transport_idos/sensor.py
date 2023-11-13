import logging
_LOGGER = logging.getLogger(__name__)

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import UNDEFINED
from homeassistant.util.dt import now, parse_time
import datetime as dt

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    CONF_FLOW_ARRIVAL_STATION,
    CONF_FLOW_DEPARTURE_STATION,
    ATTR_DEPARTURE_STATION,
    ATTR_DEPARTURE_NUMBER,
    ATTR_DEPARTURE_TYPE,
    ATTR_DEPARTURE_TIME,
    ATTR_ARRIVAL_STATION,
    ATTR_ARRIVAL_NUMBER,
    ATTR_ARRIVAL_TYPE,
    ATTR_ARRIVAL_TIME,
    ATTR_CONNECTIONS,
)
from .coordinator import IDOSDataCoordinator

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
    key = "sensor3",                   # str
    translation_key = "connection",    # str | None
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
    coordinator: IDOSDataCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    # TODO Optionally validate config entry options before creating entity

    entities = []

    name = f"{config_entry.title} ({IDOSSensorDescription1.key})"
    unique_id = f"{config_entry.entry_id}-{IDOSSensorDescription1.key}"
    entities.append(PublicTransportIDOSSensor(unique_id, name, 0, coordinator, IDOSSensorDescription1))

    name = f"{config_entry.title} ({IDOSSensorDescription2.key})"
    unique_id = f"{config_entry.entry_id}-{IDOSSensorDescription2.key}"
    entities.append(PublicTransportIDOSSensor(unique_id, name, 1, coordinator, IDOSSensorDescription2))

    name = f"{config_entry.title} ({IDOSSensorDescription3.key})"
    unique_id = f"{config_entry.entry_id}-{IDOSSensorDescription3.key}"
    entities.append(PublicTransportIDOSSensor(unique_id, name, 2, coordinator, IDOSSensorDescription2))

    async_add_entities(entities, update_before_add=True)

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # If needed, implement async_will_remove_from_hass in Entity for cleanup of Entity data

class PublicTransportIDOSSensor(CoordinatorEntity[IDOSDataCoordinator], SensorEntity):
    """PublicTransportIDOS Sensor."""

    _unrecorded_attributes = frozenset(
        {
            "native_value",
            ATTR_DEPARTURE_STATION,
            ATTR_DEPARTURE_NUMBER,
            ATTR_DEPARTURE_TYPE,
            ATTR_DEPARTURE_TIME,
            ATTR_ARRIVAL_STATION,
            ATTR_ARRIVAL_NUMBER,
            ATTR_ARRIVAL_TYPE,
            ATTR_ARRIVAL_TIME,
            ATTR_CONNECTIONS,
        }
    )

    connections: dict[list[dict]]
    _sensor_index: int = 0  # What position in list of data to look at (first, second or third)

    def __init__(self,
                 unique_id: str,
                 name: str,
                 sensor_index: int,
                 coordinator: IDOSDataCoordinator,
                 description: SensorEntityDescription) -> None:
        """Initialize PublicTransportIDOS Sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._sensor_index = sensor_index
        # self._state = "Does not matter in sensor - returns _attr_native_value"
        self._attr_native_value=None
        return

    # All info about connections
    @property
    def connections(self):
        return self._connections

    # Breakout of connections into departure attributes
    @property
    def departure_station(self):
        return self._departure_station

    @property
    def departure_station(self):
        return self._departure_station

    @property
    def departure_number(self):
        return self._departure_number

    @property
    def departure_type(self):
        return self._departure_type

    @property
    def departure_time(self):
        return self._departure_time

    # Breakout of connections into arrival attributes
    @property
    def arrival_station(self):
        return self._arrival_station

    @property
    def arrival_station(self):
        return self._arrival_station

    @property
    def arrival_number(self):
        return self._arrival_number

    @property
    def arrival_type(self):
        return self._arrival_type

    @property
    def arrival_time(self):
        return self._arrival_time

    def get_data_from_coordinator(self) -> None:
        single_connections = self.coordinator.connections_data[self._sensor_index]["single_connections"]
        self._connections = single_connections

        self._departure_station = single_connections[0]["stations"][0]
        self._departure_number = single_connections[0]["number"]
        self._departure_type = single_connections[0]["type"]
        self._departure_time = single_connections[0]["times"][0]

        self._arrival_station = single_connections[-1]["stations"][-1]
        self._arrival_number = single_connections[-1]["number"]
        self._arrival_type = single_connections[-1]["type"]
        self._arrival_time = single_connections[-1]["times"][-1]

        dtime_now: dt.datetime = dt.datetime.now()
        dtime_departure: dt.datetime = dt.datetime.combine(dt.date.today(), parse_time(self._departure_time))

        dt_delta: dt.timedelta = dtime_departure - dtime_now
        minutes = dt_delta.seconds//60 if dt_delta > dt.timedelta() else 0

        _LOGGER.warning(dt_delta)
        _LOGGER.warning(minutes)

        self._attr_native_value = minutes
        return

    async def async_update(self) -> None:
        """Update the sensor data

        Called by `async_add_entities` if `update_before_add=True` parameter is set.
        Also called perriodicaly by HA if `should_pool` property returns True.
        """
        self.get_data_from_coordinator()
        return

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.get_data_from_coordinator()
        self.async_write_ha_state()
        return

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the sun."""
        return {
            ATTR_DEPARTURE_STATION: self.departure_station,
            ATTR_DEPARTURE_NUMBER: self.departure_number,
            ATTR_DEPARTURE_TYPE: self.departure_type,
            ATTR_DEPARTURE_TIME: self.departure_time,
            ATTR_ARRIVAL_STATION: self.arrival_station,
            ATTR_ARRIVAL_NUMBER: self.arrival_number,
            ATTR_ARRIVAL_TYPE: self.arrival_type,
            ATTR_ARRIVAL_TIME: self.arrival_time,
            ATTR_CONNECTIONS: self.connections,
        }
