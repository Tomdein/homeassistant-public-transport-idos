import logging
_LOGGER = logging.getLogger(__name__)

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry, UpdateListenerType
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from datetime import timedelta
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_FLOW_DEPARTURE_STATION, CONF_FLOW_ARRIVAL_STATION

import idos_scraper

async def _async_update_listener(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Handle options update."""
    coordinator: IDOSDataCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    if (config_entry.data[CONF_FLOW_DEPARTURE_STATION] != coordinator.departure_station
        or config_entry.data[CONF_FLOW_ARRIVAL_STATION] != coordinator.arrival_station):
        await hass.config_entries.async_reload(config_entry.entry_id)

    return

class IDOSCannotConnect(HomeAssistantError):
    """Unable to connect to the IDOS web site."""

class IDOSDataCoordinator(DataUpdateCoordinator):
    """IDOSDataCoordinator coordinator."""

    departure_station: str = "Ostrava"
    arrival_station: str = "Brno"
    connections_data: list[dict] = [{}]
    _config_entry: ConfigEntry | None = None

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="IDOSDataCoordinator",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=60),
            update_method=self.async_update_data
        )    
        self.departure_station = config_entry.data[CONF_FLOW_DEPARTURE_STATION]
        self.arrival_station = config_entry.data[CONF_FLOW_ARRIVAL_STATION]
        
        self._config_entry = config_entry
        return

    async def async_update_data(self) -> None:
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        session = async_get_clientsession(self.hass)
        data = await idos_scraper.async_SearchConnectionsByStation(
            self.departure_station,
            self.arrival_station,
            session = session,
            )

        if data is None:
            raise IDOSCannotConnect()

        self.connections_data = data["connections"] if len(data["connections"]) == 3 else None
        return

    async def async_shutdown(self) -> None:
        """Handle removal (hopefuly)

        Hopefuly this triggers when being removed,
        so we can gracefuly shut down our session
        """
        await super().async_shutdown()
        return
