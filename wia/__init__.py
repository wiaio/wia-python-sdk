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
            Location,
            Command,
            #Log,
            Space,
            WhoAmI,
            AccessToken
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
        self.Location = Location()
        self.Command = Command()
        #self.Log = Log()
        self.Space = Space()
        self.Stream = Stream()
        self.WhoAmI = WhoAmI()
        self.AccessToken = AccessToken()

    @property
    def access_token(self):
        return self.__access_token

    @access_token.setter
    def access_token(self, value):
        self.__access_token = value
        if self.__access_token is not None:
            self.__auth_info = self.WhoAmI.retrieve()
            if self.__auth_info is not None:
                self.__client_id = self.__auth_info.id
                logging.debug("Setting client_id as %s", self.__client_id)
        else:
            self.__auth_info = None
            self.__client_id = None
            logging.debug("Resetting client info.")

    @staticmethod
    def access_token_create(**kwargs):
        if kwargs['username'] is None or kwargs['password'] is None:
            return "No Username/password supplied"
        if 'skope' not in kwargs:
            kwargs['scope'] = 'user'
        if 'grantType' not in kwargs:
            kwargs['grantType'] = 'password'
        token = Wia().AccessToken.create(kwargs)
        Wia().access_token = token.accessToken
        return token

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
