import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug(f"loaded")

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry, UpdateListenerType
from homeassistant.core import HomeAssistant

from datetime import timedelta
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, CONF_FLOW_DEPARTURE_STATION, CONF_FLOW_ARRIVAL_STATION

async def _async_update_listener(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Handle options update."""
    coordinator: IDOSDataCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    if config_entry.title != coordinator.title:
        await hass.config_entries.async_reload(config_entry.entry_id)

    return

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
        _LOGGER.debug(f"{__name__}:async_update_data")

        # TODO: Implement web scraping and data retrieval here
        self.connections_data = [
        {'single_connections': [
            {'delay': None, 'icon': '2.svg', 'type': 'Bus', 'number': '46', 'times': ['9:11', '9:26'], 'stations': [f'Horní Polanka', 'Svinov,mosty'], 'platforms': ['2', 'D12']},
            {'delay': None, 'icon': '3.svg', 'type': 'Tram', 'number': '17', 'times': ['9:31', '9:40'], 'stations': ['Svinov,mosty', 'VŠB-TUO'], f'platforms': ['H1', '1']}
            ],
         'id': '1744759255'
        }, 
        {'single_connections': [
            {'delay': None, 'icon': '2.svg', 'type': 'Bus', 'number': '46', 'times': ['9:46', '10:01'], 'stations': ['Horní Polanka', 'Svinov,mosty'], 'platforms': ['2', 'D12']},
            {'delay': None, 'icon': '3.svg', 'type': 'Tram', 'number': '7', 'times': ['10:04', '10:13'], 'stations': ['Svinov,mosty', 'VŠB-TUO'], 'platforms': ['H1', '1']}
            ],
         'id': '1744759400'
        }, 
        {'single_connections': [
            {'delay': None, 'icon': '2.svg', 'type': 'Bus', 'number': '46', 'times': ['10:11', '10:26'], 'stations': ['Horní Polanka', 'Svinov,mosty'], 'platforms': ['2', 'D12']},
            {'delay': None, 'icon': '3.svg', 'type': 'Tram', 'number': '17', 'times': ['10:31', '10:40'], 'stations': ['Svinov,mosty', 'VŠB-TUO'], 'platforms': ['H1', '1']}
            ],
         'id': '1744759401'
        }
        ]
        return
        
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                return await self.my_api.fetch_data(listening_idx)
        except ApiAuthError as err:
            # Raising ConfigEntryAuthFailed will cancel future updates
            # and start a config flow with SOURCE_REAUTH (async_step_reauth)
            raise ConfigEntryAuthFailed from err
        except ApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
