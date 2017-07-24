import os
import logging

if 'wia_env' in os.environ:
    wia_env = os.environ['wia_env']
else:
    wia_env = 'production'

if wia_env == 'test':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Wia(_Singleton('SingletonMeta', (object,), {})):
    def __init__(self):
        from wia.resource import (
            Device,
            Event,
            Sensor,
            Location,
            Log,
            Function,
            Customer,
            WhoAmI
        )

        from wia.stream_client import (
            Stream
        )

        from wia.version import VERSION

        self.__access_token = None
        self.__app_key = None
        self.__auth_info = None
        self.__client_id = None
        self.__rest_config = {"protocol":'https',"host":'api.wia.io',"port":443,"basePath":'v1'}
        self.__stream_config = {"protocol":'mqtt',"host":'api.wia.io',"port":1883}

        self.__version = VERSION

        self.Device = Device()
        self.Event = Event()
        self.Sensor = Sensor()
        self.Location = Location()
        self.Log = Log()
        self.Function = Function()
        self.Customer = Customer()
        self.WhoAmI = WhoAmI()
        self.Stream = Stream()

    @property
    def access_token(self):
        return self.__access_token

    @access_token.setter
    def access_token(self, value):
        self.__access_token = value
        self.__auth_info = self.WhoAmI.retrieve()
        if self.__access_token is not None and self.__auth_info is not None:
            self.__client_id = self.__auth_info.contextData['id']
            logging.debug("Setting client_id as %s", self.__client_id)
        else:
            logging.debug("Could not retrieve client info. Unable to set client_id")

    @property
    def app_key(self):
        return self.__app_key

    @app_key.setter
    def app_key(self, value):
        self.__app_key = value

    @property
    def rest_config(self):
        return self.__rest_config

    @rest_config.setter
    def rest_config(self, value):
        self.__rest_config = value

    @property
    def stream_config(self):
        return self.__stream_config

    @stream_config.setter
    def stream_config(self, value):
        self.__stream_config = value

    @property
    def client_id(self):
        return self.__client_id

    @client_id.setter
    def client_id(self, value):
        self.__client_id = value
