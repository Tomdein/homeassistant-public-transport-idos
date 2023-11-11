import logging
_LOGGER = logging.getLogger(__name__)

from typing import Any
from collections.abc import Mapping

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import homeassistant.helpers.event

from homeassistant.components.text import TextEntity, TextEntityDescription

from .const import (
    CONF_FLOW_ARRIVAL_STATION,
    CONF_FLOW_DEPARTURE_STATION,
    STATION_PATTERN,
)

# The _attr_... always take precedence, they are not overriden
# TextEntityDescription's members:
    # key: str,
    # device_class: str | None = None,
    # entity_category: EntityCategory | None = None,
    # entity_registry_enabled_default: bool = True,
    # entity_registry_visible_default: bool = True,
    # force_update: bool = False,
    # icon: str | None = None,
    # has_entity_name: bool = False,
    # name: str | UndefinedType | None = UNDEFINED,
    # translation_key: str | None = None,
    # unit_of_measurement: str | None = None,
    # native_min: int = 0,
    # native_max: int = MAX_LENGTH_STATE_STATE,
    # mode: TextMode = TextMode.TEXT,
    # pattern: str | None = None

IDOSTextDescriptionDeparture: TextEntityDescription = TextEntityDescription(
    key = "departure",
    translation_key = "departure",
    pattern = STATION_PATTERN,  # Match any words with spaces or commas separating them
)
IDOSTextDescriptionArrival: TextEntityDescription = TextEntityDescription(
    key = "arrival",
    translation_key = "arrival",
    pattern = STATION_PATTERN,  # Match any words with spaces, commas or '-' separating them
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Initialize PublicTransportIDOS config entry."""
    # TODO Optionally validate config entry options before creating entity

    entities = []

    name = f"{config_entry.title} {IDOSTextDescriptionDeparture.key} input"
    unique_id = f"{config_entry.entry_id}-{IDOSTextDescriptionDeparture.key}-input"
    entities.append(PublicTransportIDOSText(unique_id, name, CONF_FLOW_DEPARTURE_STATION, config_entry, IDOSTextDescriptionDeparture))

    name = f"{config_entry.title} {IDOSTextDescriptionArrival.key} input"
    unique_id = f"{config_entry.entry_id}-{IDOSTextDescriptionArrival.key}-input"
    entities.append(PublicTransportIDOSText(unique_id, name, CONF_FLOW_ARRIVAL_STATION, config_entry , IDOSTextDescriptionArrival))
    
    async_add_entities(entities)

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # If needed, implement async_will_remove_from_hass in Entity for cleanup of Entity data

class PublicTransportIDOSText(TextEntity):
    """PublicTransportIDOS Text."""

    _unrecorded_attributes = frozenset(
        {
            "station_type"
        }
    )

    _config_entry: ConfigEntry
    _station_type: str

    def __init__(self, unique_id: str, name: str, station_type: str, config_entry: ConfigEntry, description: TextEntityDescription) -> None:
        """Initialize PublicTransportIDOS Sensor."""
        super().__init__()
        self.entity_description = description
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = unique_id
        # self._state = "Does not matter in sensor - returns _attr_native_value"
        self._station_type = station_type
        self._attr_native_value = config_entry.data[station_type]
        self._config_entry = config_entry

    @property
    def station_type(self):
        return self._station_type

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """Return entity specific state attributes."""
        return {"station_type": self.station_type}

    def set_value(self, value: str) -> None:
        """Change the value."""
        # TODO validate if station is correct (could be also done via custom Lovelace UI card)
        self._attr_native_value = value

        data = self._config_entry.data.copy()
        data[self.station_type] = value
        self.hass.config_entries.async_update_entry(self._config_entry, data=data)

        return