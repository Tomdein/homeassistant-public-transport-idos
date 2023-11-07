from .const import DOMAIN

import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug(f"loaded")


from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.core import Event, HomeAssistant
from homeassistant.const import (
    Platform,
)

from .const import CONF_FLOW_ARRIVAL_STATION

PLATFORMS = [Platform.SENSOR]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    #hass.states.set(f"{DOMAIN}.connection_data", "No data available - Wheee")# - creates new state that will be removed after reset
    _LOGGER.debug(f"{__name__}:async_setup")
    _LOGGER.debug(f"{hass.data.keys()}")
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Load a config entry
    
    How to handle loading of config entry - either on startup or after adding dev/entity via config flow.
    The config_entry contains data you inputted in the UI while adding the integration.
    """
    #hass.states.set(f"{DOMAIN}.connection_data", "No data available")
    _LOGGER.debug(f"{__name__}:async_setup_entry:{config_entry.domain}")

    return True
