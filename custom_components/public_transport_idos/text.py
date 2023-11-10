import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug(f"loaded")

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
    key = "text-departure",
    translation_key = "",
    pattern = STATION_PATTERN,  # Match any words with spaces or commas separating them
)
IDOSTextDescriptionArrival: TextEntityDescription = TextEntityDescription(
    key = "text-arrival",
    translation_key = "",
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

    name = f"Name: {config_entry.title} ({IDOSTextDescriptionDeparture.key})"
    unique_id = f"{config_entry.entry_id}-{IDOSTextDescriptionDeparture.key}"
    station = config_entry.data[CONF_FLOW_DEPARTURE_STATION]
    entities.append(PublicTransportIDOSText(unique_id, name, station, IDOSTextDescriptionDeparture))

    name = f"Name: {config_entry.title} ({IDOSTextDescriptionArrival.key})"
    unique_id = f"{config_entry.entry_id}-{IDOSTextDescriptionArrival.key}"
    station = config_entry.data[CONF_FLOW_ARRIVAL_STATION]
    entities.append(PublicTransportIDOSText(unique_id, name, station, IDOSTextDescriptionArrival))
    
    async_add_entities(entities)

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # If needed, implement async_will_remove_from_hass in Entity for cleanup of Entity data

class PublicTransportIDOSText(TextEntity):
    """PublicTransportIDOS Text."""

    def __init__(self, unique_id: str, name: str, station: str, description: TextEntityDescription) -> None:
        """Initialize PublicTransportIDOS Sensor."""
        super().__init__()
        self.entity_description = description
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._station = station
        self._state = "Does not matter in sensor - returns _attr_native_value"
        self._attr_native_value = "VSB-TUO"
        _LOGGER.debug(f"{__name__}:PublicTransportIDOSText:__init__")

    def set_value(self, value: str) -> None:
        """Change the value."""
        self._attr_native_value = value
        return