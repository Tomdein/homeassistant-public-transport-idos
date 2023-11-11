from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from homeassistant.util import slugify

import logging
_LOGGER = logging.getLogger(__name__)

from .const import (
    DOMAIN,
    CONF_FLOW_DEPARTURE_STATION,
    CONF_FLOW_ARRIVAL_STATION
    )

def _get_data_schema() -> vol.Schema:
    return vol.Schema({
                vol.Required(CONF_FLOW_DEPARTURE_STATION): str,
                vol.Required(CONF_FLOW_ARRIVAL_STATION): str,
            })

def _get_device_unique_id(start_station: str, end_station: str):
    return slugify(f"{start_station}-{end_station}")

class PublicTransportIDOSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""

        if user_input is not None:
            # Validate and save user input
            await self.async_set_unique_id(_get_device_unique_id(
                user_input.get(CONF_FLOW_DEPARTURE_STATION), 
                user_input.get(CONF_FLOW_ARRIVAL_STATION)
                ))
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title="IDOS Public Transport", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=_get_data_schema()
        )
    