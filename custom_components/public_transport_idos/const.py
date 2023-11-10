from typing import Final

import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug(f"loaded")

DOMAIN = "public_transport_idos"

CONF_FLOW_DEPARTURE_STATION: Final = "departure_station"
CONF_FLOW_ARRIVAL_STATION: Final = "arrival_station"

ATTR_DEPARTURE_STATION: Final = CONF_FLOW_DEPARTURE_STATION
ATTR_DEPARTURE_NUMBER: Final = "departure_number"
ATTR_DEPARTURE_TYPE: Final = "departure_type"
ATTR_DEPARTURE_TIME: Final = "departure_time"

ATTR_ARRIVAL_STATION: Final = CONF_FLOW_ARRIVAL_STATION
ATTR_ARRIVAL_NUMBER: Final = "arrival_number"
ATTR_ARRIVAL_TYPE: Final = "arrival_type"
ATTR_ARRIVAL_TIME: Final = "arrival_time"

ATTR_CONNECTIONS: Final = "connections"

STATION_PATTERN: Final = r"^[\w, -]*$"