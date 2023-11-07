from typing import Final

import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug(f"loaded")

DOMAIN = "public_transport_idos"

CONF_FLOW_DEPARTURE_STATION: Final = "Departure station"
CONF_FLOW_ARRIVAL_STATION: Final = "Arrival station"