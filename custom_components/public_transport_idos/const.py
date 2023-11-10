from typing import Final

import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug(f"loaded")

DOMAIN = "public_transport_idos"

CONF_FLOW_DEPARTURE_STATION: Final = "departure_station"
CONF_FLOW_ARRIVAL_STATION: Final = "arrival_station"