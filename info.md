# IDOS Public Transport custom integration
IDOS Public Transport integration scrapes Czech public transport information system [IDOS](idos.idnes.cz) and gets latest data about a bus/tram/train connection.

The integration exposes a few entites:
- 3x Sensor entites - for 3 earliest connections found
  - Exposes remaining time to departure for connection as state
  - Also has additional information about connection as attributes
- 2x Text input entity
  - Enables you to change destination and arrival station
- Button entity
  - Does not work yet 

There is custom lovelace UI card comming soon.

This integration uses python idos-scraper package.