import wia
from wia.rest_client import post, get, put, delete
from wia.util import logger
from wia.stream_client import Stream
import time

unsubscribe_flag = False

class Device(object):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.name = (kwargs['name'] if 'name' in kwargs else None)
        self.events = (kwargs['events'] if 'events' in kwargs else None)
        self.isOnline = (kwargs['isOnline'] if 'isOnline' in kwargs else None)
        self.createdAt = (kwargs['createdAt'] if 'createdAt' in kwargs else None)
        self.updatedAt = (kwargs['updatedAt'] if 'updatedAt' in kwargs else None)

    @classmethod
    def create(self, **kwargs):
        path = 'devices'
        created_device = post(path, kwargs)
        return created_device

    @classmethod
    def retrieve(self, id, sk=None):
        path = 'devices/' + id
        if (id == 'me') and sk:
            retrieved_device = get(path, sk=sk)
        elif (id == 'me') and not sk:
            raise SyntaxError('Must provide device secret key if retrieving self')
        else:
            retrieved_device = get(path)
        return Device(**retrieved_device)

    @classmethod
    def update(self, id, **kwargs):
        path = 'devices/' + id
        return put(path, **kwargs)

    @classmethod
    def delete(self, id):
        path = 'devices/' + id
        if delete(path).status_code == 200:
            return True
        else:
            return False

    @classmethod
    def list(self, **kwargs):
        list_devices = get('devices', **kwargs)
        for device in list_devices['devices']:
            data = device
            logger.info("device: %s", data)
        logger.info("count: %s", list_devices['count'])
        return list_devices

class Event(object):
    def __init__(self, **kwargs):
        self.name = (kwargs['name'] if 'name' in kwargs else None)
        self.data = (kwargs['data'] if 'data' in kwargs else None)
        self.timestamp = (kwargs['timestamp'] if 'timestamp' in kwargs else None)

    @classmethod
    def publish(self, **kwargs):
        path = 'events'
        new_event = post(path, kwargs)
        if wia.Stream.connected:
            topic = 'devices/' + wia.device_id + '/' + path + '/' + kwargs['name']
            Stream.publish(topic=topic, **kwargs)
        return new_event

    @classmethod
    def subscribe(self, **kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/events/'
        if 'name' in kwargs:
            topic += kwargs['name']
        else:
            topic += '+'
        Stream.subscribe(topic=topic, func=kwargs['func'])

    @classmethod
    def unsubscribe(self, **kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/events/'
        if 'name' in kwargs:
            topic += kwargs['name']
        else:
            topic += '+'
        Stream.unsubscribe(topic=topic)

    @classmethod
    def list(self, **kwargs):
        list_events = get('events', **kwargs)
        for event in list_events['events']:
            data = event
            logger.info("event: %s", data)
        logger.info("count: %s", list_events['count'])
        return list_events

class Sensor(object):
    def __init__(self, **kwargs):
        self.name = (kwargs['name'] if 'name' in kwargs else None)
        self.data = (kwargs['data'] if 'data' in kwargs else None)
        self.timestamp = (kwargs['timestamp'] if 'timestamp' in kwargs else None)

    @classmethod
    def publish(self, **kwargs):
        path = 'sensors'
        new_sensor = post(path, kwargs)
        if wia.Stream.connected:
            topic = 'devices/' + wia.device_id + '/' + path + '/' + kwargs['name']
            Stream.publish(topic=topic, **kwargs)
        return new_sensor

    @classmethod
    def subscribe(self, **kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/sensors/'
        if 'name' in kwargs:
            topic += kwargs['name']
        else:
            topic += '+'
        Stream.subscribe(topic=topic, func=kwargs['func'])

    @classmethod
    def unsubscribe(self, **kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/sensors/'
        if 'name' in kwargs:
            topic += kwargs['name']
        else:
            topic += '+'
        Stream.unsubscribe(topic=topic)

    @classmethod
    def list(self, **kwargs):
        list_sensors = get('sensors', **kwargs)
        for sensor in list_sensors['sensors']:
            data = sensor
            logger.info("sensor: %s", data)
        logger.info("count: %s", list_sensors['count'])
        return list_sensors

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
        new_location = post(path, kwargs)
        if wia.Stream.connected:
            topic = 'devices/' + wia.device_id + '/' + path
            Stream.publish(topic=topic, **kwargs)
        return new_location

    @classmethod
    def subscribe(self, **kwargs):
        device = kwargs['device']
        topic = 'devices/' + device + '/locations'
        Stream.subscribe(topic=topic, func=kwargs['func'])

    @classmethod
    def unsubscribe(self, **kwargs):
        device = kwargs['device']
        topic = 'devices/' + device + '/locations'
        Stream.unsubscribe(topic=topic)

    @classmethod
    def list(self, **kwargs):
        list_locations = get('locations', **kwargs)
        for location in list_locations['locations']:
            data = location
            logger.info("location: %s", data)
        logger.info("count: %s", list_locations['count'])
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
        new_log = post(path, kwargs)
        if wia.Stream.connected:
            topic = 'devices/' + wia.device_id + '/' + path
            Stream.publish(topic=topic, **kwargs)
        return new_log

    @classmethod
    def subscribe(self, **kwargs):
        device = kwargs['device']
        topic = 'devices/' + device + '/logs'
        Stream.subscribe(topic=topic, func=kwargs['func'])

    @classmethod
    def unsubscribe(self, **kwargs):
        device = kwargs['device']
        topic = 'devices/' + device + '/logs'
        Stream.unsubscribe(topic=topic)

    @classmethod
    def list(self, **kwargs):
        list_logs = get('logs', **kwargs)
        for log in list_logs['logs']:
            data = log
            logger.info("log: %s", data)
        logger.info("count: %s", list_logs['count'])
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
        device = wia.device_id
        topic = 'devices/' + device + '/functions/' + new_function['id'] + '/call'
        attempts = 0
        while attempts < 6:
            Stream.subscribe(topic=topic, func=kwargs['function'])
            time.sleep(0.5)
            attempts += 1
            if Stream.subscribed == True:
                break
        if not Stream.subscribed:
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
        if wia.Stream.connected:
            topic = 'devices/' + kwargs['device'] + '/functions/' + kwargs['func'] + '/call'
            Stream.publish(topic=topic, **kwargs['data'])
        else:
            path = 'functions/' + kwargs['func'] + '/call'
            data = kwargs['data']
            request_return = post(path, kwargs)

    @classmethod
    def list(self, **kwargs):
        list_functions = get('functions', **kwargs)
        for function in list_functions['functions']:
            data = function
            logger.info("function: %s", data)
        logger.info("count: %s", list_functions['count'])
        return list_functions