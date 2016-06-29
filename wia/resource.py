from wia.rest_client import post, get, put, delete
from wia.util import logger

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

class Events(object):
    def __init__(self, **kwargs):
        self.name = (kwargs['name'] if 'name' in kwargs else None)
        self.data = (kwargs['data'] if 'data' in kwargs else None)
        self.timestamp = (kwargs['timestamp'] if 'timestamp' in kwargs else None)

    @classmethod
    def publish(self, **kwargs):
        path = 'events'
        new_event = post(path, kwargs, True)
        return new_event

    @classmethod
    def list(self, **kwargs):
        list_events = get('events', **kwargs)
        for event in list_events['events']:
            data = event
            logger.info("event: %s", data)
        logger.info("count: %s", list_events['count'])
        return list_events

class Sensors(object):
    def __init__(self, **kwargs):
        self.name = (kwargs['name'] if 'name' in kwargs else None)
        self.data = (kwargs['data'] if 'data' in kwargs else None)
        self.timestamp = (kwargs['timestamp'] if 'timestamp' in kwargs else None)

    @classmethod
    def publish(self, **kwargs):
        path = 'sensors'
        new_sensor = post(path, kwargs, True)
        return new_sensor

    @classmethod
    def list(self, **kwargs):
        list_sensors = get('sensors', **kwargs)
        for sensor in list_sensors['sensors']:
            data = sensor
            logger.info("sensor: %s", data)
        logger.info("count: %s", list_events['sensor'])
        return list_sensors

class Locations(object):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.latitude = (kwargs['latitude'] if 'latitude' in kwargs else None)
        self.longitude = (kwargs['longitude'] if 'longitude' in kwargs else None)
