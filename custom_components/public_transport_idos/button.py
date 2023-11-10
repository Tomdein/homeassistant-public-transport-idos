import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug(f"loaded")

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription

from .const import (
    CONF_FLOW_ARRIVAL_STATION,
    CONF_FLOW_DEPARTURE_STATION,
    STATION_PATTERN,
)

# The _attr_... always take precedence, they are not overriden
# ButtonEntityDescription's members:
    # key: str
    # device_class: ButtonDeviceClass | None = None
    # entity_category: EntityCategory | None = None
    # entity_registry_enabled_default: bool = True
    # entity_registry_visible_default: bool = True
    # force_update: bool = False
    # icon: str | None = None
    # has_entity_name: bool = False
    # name: str | UndefinedType | None = UNDEFINED
    # translation_key: str | None = None
    # unit_of_measurement: str | None = None

IDOSButtonDescriptionPaging: ButtonEntityDescription = ButtonEntityDescription(
    key = "text-departure",
    translation_key = "",
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Initialize PublicTransportIDOS config entry."""
    # TODO Optionally validate config entry options before creating entity

    entities = []

    name = f"Name: {config_entry.title} ({IDOSButtonDescriptionPaging.key})"
    unique_id = f"{config_entry.entry_id}-{IDOSButtonDescriptionPaging.key}"
    station = config_entry.data[CONF_FLOW_DEPARTURE_STATION]
    entities.append(PublicTransportIDOSButtonPaging(unique_id, name, IDOSButtonDescriptionPaging))

    async_add_entities(entities)

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # If needed, implement async_will_remove_from_hass in Entity for cleanup of Entity data

class PublicTransportIDOSButtonPaging(ButtonEntity):
    """PublicTransportIDOS Text."""

    def __init__(self, unique_id: str, name: str, description: ButtonEntityDescription) -> None:
        """Initialize PublicTransportIDOS Sensor."""
        super().__init__()
        self.entity_description = description
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._state = "Does not matter in sensor - returns _attr_native_value"
        self._attr_native_value = "Page mooooore"
        _LOGGER.debug(f"{__name__}:PublicTransportIDOSButtonPaging:__init__")

    def press(self) -> None:
        """Press the button."""
        _LOGGER.debug(f"{__name__}:PublicTransportIDOSButtonPaging:press")
