from .const import DOMAIN

import logging
_LOGGER = logging.getLogger(__name__)


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
from .coordinator import IDOSDataCoordinator, _async_update_listener

PLATFORMS = [Platform.SENSOR, Platform.TEXT, Platform.BUTTON]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    # Add WebSocket command
    hass.components.websocket_api.async_register_command(ws_handle_search_station)

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
    coordinator: IDOSDataCoordinator = IDOSDataCoordinator(hass, config_entry)
    config_entry.async_on_unload(
        config_entry.add_update_listener(_async_update_listener)
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

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



import re
import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from idos_scraper.scrapers import async_search_station

@websocket_api.websocket_command(
    {
        vol.Required("type"): "idos/search_stations",
        vol.Required("station"): str,
        vol.Optional("count", default="3"): str,
        vol.Optional("search_by_location"): {
            vol.Required("latitude"): str,
            vol.Required("longitude"): str,
            vol.Optional("accuracy", default="10"): str,
            vol.Optional("only_stations", default="true"): str,
        },
    }
)
@websocket_api.async_response
async def ws_handle_search_station(
    hass: HomeAssistant, connection: websocket_api.connection.ActiveConnection, msg: dict
) -> None:
    """Handle IDOS search station command."""
    # Check if we are searching by location
    if "search_by_location" in msg:
        # stations = await async_search_station.async_SearchStationByLocation()
        # connection.send_result(
        # msg["id"],
        # {
        #     #"content_type": content_type,
        #     "content": stations,
        # },
        # )
        # return
        connection.send_error(
                msg["id"],
                "not_implemented_yet",
                "Searching stations by location is not implemented yet"
            )

    aiohttp_session = async_get_clientsession(hass)
    stations = await async_search_station.async_SearchStation(msg["station"], msg["count"], aiohttp_session)

    connection.send_result(
        msg["id"],
        {
            "stations": stations,
        },
    )