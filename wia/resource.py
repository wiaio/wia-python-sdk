import time
import logging

from wia import Wia
from wia.rest_client import post, get, put, delete

class Device(object):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.name = (kwargs['name'] if 'name' in kwargs else None)
        self.sensors = (kwargs['sensors'] if 'sensors' in kwargs else None)
        self.events = (kwargs['events'] if 'events' in kwargs else None)
        self.location = (kwargs['location'] if 'location' in kwargs else None)
        self.public = (kwargs['public'] if 'public' in kwargs else None)
        self.isOnline = (kwargs['isOnline'] if 'isOnline' in kwargs else None)
        self.createdAt = (kwargs['createdAt'] if 'createdAt' in kwargs else None)
        self.updatedAt = (kwargs['updatedAt'] if 'updatedAt' in kwargs else None)

    @classmethod
    def create(self, **kwargs):
        path = 'devices'
        created_device = post(path, kwargs)
        return created_device

    @classmethod
    def retrieve(self, id):
        path = 'devices/' + id
        response = get(path)
        return Device(**response.json())

    def save(self):
        path = 'devices/' + self.id
        return put(path, name=self.name)

    def delete(self):
        path = 'devices/' + self.id
        if delete(path).status_code == 200:
            return True
        else:
            return False

    @classmethod
    def list(self, **kwargs):
        list_devices = get('devices', **kwargs)
        for device in list_devices['devices']:
            data = device
            logging.debug("Device: %s", data)
        logging.debug("Count: %s", list_devices['count'])
        return list_devices

class Event(object):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.name = (kwargs['name'] if 'name' in kwargs else None)
        self.data = (kwargs['data'] if 'data' in kwargs else None)
        self.file = (kwargs['file'] if 'file' in kwargs else None)
        self.timestamp = (kwargs['timestamp'] if 'timestamp' in kwargs else None)

    @classmethod
    def publish(self, **kwargs):
        path = 'events'
        if not ('file' in kwargs) and Wia().Stream.connected and Wia().client_id is not None:
            topic = 'devices/' + Wia().client_id + '/' + path + '/' + kwargs['name']
            Wia().Stream.publish(topic=topic, **kwargs)
            return Event()
        else:
            response = post(path, kwargs)
            logging.debug('Response: %s', response)
            return Event(**response.json())

    @classmethod
    def subscribe(self, **kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/events/'
        if 'name' in kwargs:
            topic += kwargs['name']
        else:
            topic += '+'
        Wia().Stream.subscribe(topic=topic, func=kwargs['func'])

    @classmethod
    def unsubscribe(self, **kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/events/'
        if 'name' in kwargs:
            topic += kwargs['name']
        else:
            topic += '+'
        Wia().Stream.unsubscribe(topic=topic)

    @classmethod
    def list(self, **kwargs):
        response = get('events', **kwargs)
        responseJson = response.json()
        events = []
        for event in responseJson['events']:
            events.append(Event(**event))
        return {'events':events,'count': responseJson['count']}

class Sensor(object):
    def __init__(self, **kwargs):
        self.name = (kwargs['name'] if 'name' in kwargs else None)
        self.data = (kwargs['data'] if 'data' in kwargs else None)
        self.timestamp = (kwargs['timestamp'] if 'timestamp' in kwargs else None)

    @classmethod
    def publish(self, **kwargs):
        path = 'sensors'
        if Wia().Stream.connected and Wia().client_id is not None:
            topic = 'devices/' + Wia().client_id + '/' + path + '/' + kwargs['name']
            Wia().Stream.publish(topic=topic, **kwargs)
            return {}
        else:
            return post(path, kwargs)

    @classmethod
    def subscribe(self, **kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/sensors/'
        if 'name' in kwargs:
            topic += kwargs['name']
        else:
            topic += '+'
        Wia().Stream.subscribe(topic=topic, func=kwargs['func'])

    @classmethod
    def unsubscribe(self, **kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/sensors/'
        if 'name' in kwargs:
            topic += kwargs['name']
        else:
            topic += '+'
        Wia().Stream.unsubscribe(topic=topic)

    @classmethod
    def list(self, **kwargs):
        return get('sensors', **kwargs)

class Location(object):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.latitude = (kwargs['latitude'] if 'latitude' in kwargs else None)
        self.longitude = (kwargs['longitude'] if 'longitude' in kwargs else None)
        self.altitude = (kwargs['altitude'] if 'altitude' in kwargs else None)
        self.timestamp = (kwargs['timestamp'] if 'timestamp' in kwargs else None)
        self.recievedTimestamp = (kwargs['recievedTimestamp'] if 'recievedTimestamp' in kwargs else None)

    @classmethod
    def publish(self, **kwargs):
        path = 'locations'
        if Wia().Stream.connected and Wia().client_id is not None:
            topic = 'devices/' + Wia().client_id + '/' + path
            Wia().Stream.publish(topic=topic, **kwargs)
            return {}
        else:
            return post(path, kwargs)

    @classmethod
    def subscribe(self, **kwargs):
        device = kwargs['device']
        topic = 'devices/' + device + '/locations'
        Wia().Stream.subscribe(topic=topic, func=kwargs['func'])

    @classmethod
    def unsubscribe(self, **kwargs):
        device = kwargs['device']
        topic = 'devices/' + device + '/locations'
        Wia().Stream.unsubscribe(topic=topic)

    @classmethod
    def list(self, **kwargs):
        list_locations = get('locations', **kwargs)
        for location in list_locations['locations']:
            data = location
            logging.debug("Location: %s", data)
        logging.debug("Count: %s", list_locations['count'])
        return list_locations

class Log(object):
    def __init__(self, **kwargs):
        self.level = (kwargs['level'] if 'level' in kwargs else None)
        self.message = (kwargs['message'] if 'message' in kwargs else None)
        self.data = (kwargs['data'] if 'data' in kwargs else None)
        self.timestamp = (kwargs['timestamp'] if 'timestamp' in kwargs else None)

    @classmethod
    def publish(self, **kwargs):
        path = 'logs'
        if Wia().Stream.connected and Wia().client_id is not None:
            topic = 'devices/' + Wia().client_id + '/' + path + '/' + kwargs['level']
            Wia().Stream.publish(topic=topic, **kwargs)
            return {}
        else:
            return post(path, kwargs)

    @classmethod
    def subscribe(self, **kwargs):
        device = kwargs['device']
        topic = 'devices/' + device + '/logs'
        Wia().Stream.subscribe(topic=topic, func=kwargs['func'])

    @classmethod
    def unsubscribe(self, **kwargs):
        device = kwargs['device']
        topic = 'devices/' + device + '/logs'
        Wia().Stream.unsubscribe(topic=topic)

    @classmethod
    def list(self, **kwargs):
        list_logs = get('logs', **kwargs)
        for log in list_logs['logs']:
            data = log
            logging.info("Log: %s", data)
        logging.info("Count: %s", list_logs['count'])
        return list_logs

class Function(object):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.name = (kwargs['name'] if 'name' in kwargs else None)
        self.isEnabled = (kwargs['isEnabled'] if 'isEnabled' in kwargs else None)
        self.device = (kwargs['device'] if 'device' in kwargs else None)
        self.enabledAt = (kwargs['enabledAt'] if 'enabledAt' in kwargs else None)
        self.createdAt = (kwargs['createdAt'] if 'createdAt' in kwargs else None)
        self.updatedAt = (kwargs['updatedAt'] if 'updatedAt' in kwargs else None)

    @classmethod
    def create(self, **kwargs):
        path = 'functions'
        data = {'name': kwargs['name']}
        new_function = post(path, data)
        topic = 'devices/' + Wia().client_id + '/functions/' + new_function['id'] + '/call'
        attempts = 0
        while attempts < 6:
            Wia().Stream.subscribe(topic=topic, func=kwargs['function'])
            time.sleep(0.5)
            attempts += 1
            if Wia().Stream.subscribed == True:
                break
        if not Wia().Stream.subscribed:
            raise Exception("SUBSCRIPTION UNSUCCESSFUL")
        return new_function

    @classmethod
    def delete(self, func_id):
        path = 'functions/' + func_id
        if delete(path).status_code == 200:
            return True
        else:
            return False

    @classmethod
    def call(self, **kwargs):
        if Wia().Stream.connected:
            topic = 'devices/' + kwargs['device'] + '/functions/' + kwargs['func'] + '/call'
            if 'data' not in kwargs:
                Wia().Stream.publish(topic=topic)
            elif type(kwargs['data']) is dict:
                Wia().Stream.publish(topic=topic, **kwargs['data'])
            else:
                data = kwargs['data']
                kwargs.pop('data')
                kwargs['data'] = {'arg': data}
                Wia().Stream.publish(topic=topic, **kwargs['data'])
        else:
            raise Exception("Unable to call function, not connected to stream")

    @classmethod
    def list(self, **kwargs):
        list_functions = get('functions', **kwargs)
        for function in list_functions['functions']:
            data = function
            logging.debug("Function: %s", data)
        logging.debug("Count: %s", list_functions['count'])
        return list_functions

class Customer(object):
    @classmethod
    def signup(self, **kwargs):
        return post('customers/signup', kwargs)

    @classmethod
    def login(self, **kwargs):
        kwargs['scope'] = 'customer'
        kwargs['grantType'] = 'password'
        return post('auth/token', kwargs)

class WhoAmI(object):
    def __init__(self, **kwargs):
        self.contextData = (kwargs['contextData'] if 'contextData' in kwargs else None)
        self.scope = (kwargs['scope'] if 'scope' in kwargs else None)

    @classmethod
    def retrieve(self):
        response = get('whoami')
        return WhoAmI(**response.json())
