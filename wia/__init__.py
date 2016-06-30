from wia.version import VERSION

__version__ = VERSION

secret_key = None
api_version = None

rest_api_base = 'https://api.wia.io/v1'
mqtt_api_base = 'https://api.wia.io'

from wia.resource import (
    Device,
    Events,
    Sensors,
    Locations,
    Logs
)

from wia.version import VERSION
