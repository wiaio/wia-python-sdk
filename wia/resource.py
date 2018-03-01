import time
import logging

from wia import Wia
from wia.rest_client import post, get, put, delete
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class WiaResource():

    @staticmethod
    def is_success(response):
        if response.status_code == 200 or response.status_code == 201:
            return True
        else:
            return False

    @staticmethod
    def error_response(response):
        if response.status_code == 400:
            return WiaValidationError(response)
        elif response.status_code == 401:
            return WiaUnauthorisedError(response)
        elif response.status_code == 403:
            return WiaForbiddenError(response)
        elif response.status_code == 404:
            return WiaNotFoundError(response)
        else:
            return WiaError(response)

class WiaResourceDelete(WiaResource):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.deleted = (kwargs['deleted'] if 'deleted' in kwargs else None)

class Device(WiaResource):
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

    @staticmethod
    def create(**kwargs):
        path = 'devices'
        response = post(path, kwargs)
        if WiaResource.is_success(response):
            return Device(**response.json())
        else:
            return WiaResource.error_response(response)

    @staticmethod
    def retrieve(id):
        path = 'devices/' + id
        response = get(path)
        if WiaResource.is_success(response):
            return Device(**response.json())
        else:
            return WiaResource.error_response(response)

    @staticmethod
    def update(**kwargs):
        path = 'devices/' + kwargs['id']
        dictCopy = dict(kwargs)
        del dictCopy['id']
        response = put(path, dictCopy)
        if WiaResource.is_success(response):
            return Device(**response.json())
        else:
            return WiaResource.error_response(response)

    @staticmethod
    def delete(id):
        path = 'devices/' + id
        response = delete(path)
        if WiaResource.is_success(response):
            return WiaResourceDelete(**response.json())
        else:
            return WiaResource.error_response(response)

    @staticmethod
    def list(**kwargs):
        response = get('devices', **kwargs)
        if WiaResource.is_success(response):
            responseJson = response.json()
            devices = []
            for device in responseJson['devices']:
                devices.append(Device(**device))
            return {'devices':devices,'count': responseJson['count']}
        else:
            return WiaResource.error_response(response)

class Event(WiaResource):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.name = (kwargs['name'] if 'name' in kwargs else None)
        self.data = (kwargs['data'] if 'data' in kwargs else None)
        self.file = (kwargs['file'] if 'file' in kwargs else None)
        self.timestamp = (kwargs['timestamp'] if 'timestamp' in kwargs else None)

    @staticmethod
    def publish(**kwargs):
        path = 'events'
        if not ('file' in kwargs) and Wia().Stream.connected and Wia().client_id is not None:
            topic = 'devices/' + Wia().client_id + '/' + path + '/' + kwargs['name']
            Wia().Stream.publish(topic=topic, **kwargs)
            return Event()
        else:
            response = post(path, kwargs)
            if WiaResource.is_success(response):
                return Event(**response.json())
            else:
                return WiaResource.error_response(response)

    @staticmethod
    def subscribe(**kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/events/'
        if 'name' in kwargs:
            topic += kwargs['name']
        else:
            topic += '+'
        Wia().Stream.subscribe(topic=topic, func=kwargs['func'])

    @staticmethod
    def unsubscribe(**kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/events/'
        if 'name' in kwargs:
            topic += kwargs['name']
        else:
            topic += '+'
        Wia().Stream.unsubscribe(topic=topic)

    @staticmethod
    def list(**kwargs):
        response = get('events', **kwargs)
        if WiaResource.is_success(response):
            responseJson = response.json()
            events = []
            for event in responseJson['events']:
                events.append(Event(**event))
            return {'events':events,'count': responseJson['count']}
        else:
            return WiaResource.error_response(response)


class Location(WiaResource):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.latitude = (kwargs['latitude'] if 'latitude' in kwargs else None)
        self.longitude = (kwargs['longitude'] if 'longitude' in kwargs else None)
        self.altitude = (kwargs['altitude'] if 'altitude' in kwargs else None)
        self.timestamp = (kwargs['timestamp'] if 'timestamp' in kwargs else None)
        self.recievedTimestamp = (kwargs['recievedTimestamp'] if 'recievedTimestamp' in kwargs else None)

    @classmethod
    def publish(cls, **kwargs):
        path = 'locations'
        if Wia().Stream.connected and Wia().client_id is not None:
            topic = 'devices/' + Wia().client_id + '/' + path
            Wia().Stream.publish(topic=topic, **kwargs)
            return Location()
        else:
            response = post(path, kwargs)
            if WiaResource.is_success(response):
                return cls(**response.json())
            else:
                return WiaResource.error_response(response)

    @staticmethod
    def subscribe(**kwargs):
        device = kwargs['device']
        topic = 'devices/' + device + '/locations'
        Wia().Stream.subscribe(topic=topic, func=kwargs['func'])

    @staticmethod
    def unsubscribe(**kwargs):
        device = kwargs['device']
        topic = 'devices/' + device + '/locations'
        Wia().Stream.unsubscribe(topic=topic)

    @staticmethod
    def list(**kwargs):
        response = get('locations', **kwargs)
        if WiaResource.is_success(response):
            responseJson = response.json()
            locations = []
            for location in responseJson['locations']:
                locations.append(Location(**location))
            return {'locations':locations,'count': responseJson['count']}
        else:
            return WiaResource.error_response(response)

class Log(WiaResource):
    def __init__(self, **kwargs):
        self.level = (kwargs['level'] if 'level' in kwargs else None)
        self.message = (kwargs['message'] if 'message' in kwargs else None)
        self.data = (kwargs['data'] if 'data' in kwargs else None)
        self.timestamp = (kwargs['timestamp'] if 'timestamp' in kwargs else None)

    @staticmethod
    def publish(**kwargs):
        path = 'logs'
        if Wia().Stream.connected and Wia().client_id is not None:
            topic = 'devices/' + Wia().client_id + '/' + path + '/' + kwargs['level']
            Wia().Stream.publish(topic=topic, **kwargs)
            return Log()
        else:
            response = post(path, kwargs)
            if WiaResource.is_success(response):
                return Log(**response.json())
            else:
                return WiaResource.error_response(response)

    @staticmethod
    def subscribe(**kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/logs/'
        if 'level' in kwargs:
            topic += kwargs['level']
        else:
            topic += '+'
        Wia().Stream.subscribe(topic=topic, func=kwargs['func'])

    @staticmethod
    def unsubscribe(**kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/logs/'
        if 'level' in kwargs:
            topic += kwargs['level']
        else:
            topic += '+'
        Wia().Stream.unsubscribe(topic=topic)

    @staticmethod
    def list(**kwargs):
        response = get('logs', **kwargs)
        if WiaResource.is_success(response):
            responseJson = response.json()
            logs = []
            for log in responseJson['logs']:
                logs.append(Log(**log))
            return {'logs':logs,'count': responseJson['count']}
        else:
            return WiaResource.error_response(response)


class AccessToken(WiaResource):
    def __init__(self, **kwargs):
        self.accessToken = (kwargs['accessToken'] if 'accessToken' in kwargs else None)
        self.refreshToken = (kwargs['refreshToken'] if 'refreshToken' in kwargs else None)
        self.tokenType = (kwargs['tokenType'] if 'tokenType' in kwargs else None)
        self.expiresIn = (kwargs['expiresIn'] if 'expiresIn' in kwargs else None)
        self.scope = (kwargs['scope'] if 'scope' in kwargs else None)

    @staticmethod
    def create(**kwargs):
        response = post('auth/token', kwargs)
        if WiaResource.is_success(response):
            return AccessToken(**response.json())
        else:
            return WiaResource.error_response(response)

class WhoAmI(WiaResource):
    def __init__(self, **kwargs):
        self.contextData = (kwargs if kwargs else None)
        self.scope = (kwargs['scope'] if 'scope' in kwargs else None)

    @classmethod
    def retrieve(cls):
        response = get('whoami')
        if WiaResource.is_success(response):
            return cls(**response.json())
        else:
            return WiaResource.error_response(response)
