from wia.version import VERSION
import os
import logging

logging.basicConfig(level=logging.DEBUG)

__version__ = VERSION

secret_key = os.environ['secret_key']
device_secret_key = os.environ['device_secret_key']
app_key = os.environ['app_key']
device_id = os.environ['device_id']
api_version = None

rest_api_base = 'https://api.wia.io/v1'
stream_protocol = 'mqtt'
stream_host = 'api.wia.io'
stream_port = 1883

from wia.resource import (
    Device,
    Event,
    Sensor,
    Location,
    Log,
    Function
)

from wia.stream_client import (
    Stream
)

from wia.version import VERSION
