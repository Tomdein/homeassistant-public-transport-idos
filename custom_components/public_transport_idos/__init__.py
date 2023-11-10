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
# Disable all from 'DOMAIN' from recorder history
from homeassistant.components.recorder.__init__ import CONFIG_SCHEMA as Recorder_CONFIG_SCHEMA
from homeassistant.components.recorder.core import Recorder
from homeassistant.components.recorder.const import DATA_INSTANCE as Recorder_DATA_INSTANCE
from homeassistant.components.recorder.const import DOMAIN as Recorder_DOMAIN
from homeassistant.helpers.entityfilter import convert_include_exclude_filter
from homeassistant.const import CONF_EXCLUDE, CONF_DOMAINS
from homeassistant import config as conf_util

from .const import CONF_FLOW_ARRIVAL_STATION

PLATFORMS = [Platform.SENSOR, Platform.TEXT, Platform.BUTTON]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    #hass.states.set(f"{DOMAIN}.connection_data", "No data available - Wheee")# - creates new state that will be removed after reset
    _LOGGER.debug(f"{__name__}:async_setup")
    _LOGGER.debug(f"{hass.data.keys()}")

    # Disable all from 'DOMAIN' from recorder history
    # Get the 'Recorder' instance
    recorder_instance: Recorder = hass.data[Recorder_DATA_INSTANCE]
    # Validate conf[Recorder_DOMAIN] via Recorder_CONFIG_SCHEMA.
    # Also adds default values - needed - This creates all keys in dict
    processed_config = Recorder_CONFIG_SCHEMA(config)[Recorder_DOMAIN]
    # Add exlude public_transport_idos 'DOMAIN'
    processed_config[CONF_EXCLUDE][CONF_DOMAINS].append(DOMAIN)
    # Renew filter
    recorder_instance.entity_filter = convert_include_exclude_filter(processed_config).get_filter()
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Load a config entry
    
    How to handle loading of config entry - either on startup or after adding dev/entity via config flow.
    The config_entry contains data you inputted in the UI while adding the integration.
    """
    #hass.states.set(f"{DOMAIN}.connection_data", "No data available")
    _LOGGER.debug(f"{__name__}:async_setup_entry:{config_entry.domain}")

    # TODO Optionally store an object for your platforms to access. Gets deleted in async_unload_entry
    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = config_entry.data[CONF_FLOW_ARRIVAL_STATION]

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry.
    
    Adds the ability to reload entry. 
    Adds the button 'reload' next to 'delete' and 'disable' after clicking on integration.
    """
    if unload_ok := await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    ):
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok
