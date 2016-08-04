from wia.version import VERSION
import os
import logging

logging.basicConfig(level=logging.DEBUG)

__version__ = VERSION

secret_key = ''
user_secret_key = ''
device_secret_key = ''
device_id = ''
app_key = ''
org_secret_key = ''

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
    Function,
    Customer
)

from wia.stream_client import (
    Stream
)

from wia.version import VERSION
