import time
import logging

from wia import Wia
from wia.rest_client import post, get, put, delete
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class WiaResource(object):
    @classmethod
    def is_success(self, response):
        if response.status_code == 200 or response.status_code == 201:
            return True
        else:
            return False

    @classmethod
    def error_response(self, response):
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

    @classmethod
    def create(self, **kwargs):
        path = 'devices'
        response = post(path, kwargs)
        if WiaResource.is_success(response):
            return Device(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def retrieve(self, id):
        path = 'devices/' + id
        response = get(path)
        if WiaResource.is_success(response):
            return Device(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def update(self, **kwargs):
        path = 'devices/' + kwargs['id']
        dictCopy = dict(kwargs)
        del dictCopy['id']
        response = put(path, dictCopy)
        if WiaResource.is_success(response):
            return Device(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def delete(self, id):
        path = 'devices/' + id
        response = delete(path)
        if WiaResource.is_success(response):
            return WiaResourceDelete(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def list(self, **kwargs):
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

    @classmethod
    def publish(self, **kwargs):
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
        if WiaResource.is_success(response):
            responseJson = response.json()
            events = []
            for event in responseJson['events']:
                events.append(Event(**event))
            return {'events':events,'count': responseJson['count']}
        else:
            return WiaResource.error_response(response)

class Sensor(WiaResource):
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
            return Sensor()
        else:
            response = post(path, kwargs)
            if WiaResource.is_success(response):
                return Sensor(**response.json())
            else:
                return WiaResource.error_response(response)

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
        response = get('sensors', **kwargs)
        if WiaResource.is_success(response):
            responseJson = response.json()
            sensors = []
            for sensor in responseJson['sensors']:
                sensors.append(Sensor(**sensor))
            return {'sensors':sensors,'count': responseJson['count']}
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
    def publish(self, **kwargs):
        path = 'locations'
        if Wia().Stream.connected and Wia().client_id is not None:
            topic = 'devices/' + Wia().client_id + '/' + path
            Wia().Stream.publish(topic=topic, **kwargs)
            return Location()
        else:
            response = post(path, kwargs)
            if WiaResource.is_success(response):
                return Location(**response.json())
            else:
                return WiaResource.error_response(response)

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

    @classmethod
    def publish(self, **kwargs):
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

    @classmethod
    def subscribe(self, **kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/logs/'
        if 'level' in kwargs:
            topic += kwargs['level']
        else:
            topic += '+'
        Wia().Stream.subscribe(topic=topic, func=kwargs['func'])

    @classmethod
    def unsubscribe(self, **kwargs):
        device=kwargs['device']
        topic='devices/' + device + '/logs/'
        if 'level' in kwargs:
            topic += kwargs['level']
        else:
            topic += '+'
        Wia().Stream.unsubscribe(topic=topic)

    @classmethod
    def list(self, **kwargs):
        response = get('logs', **kwargs)
        if WiaResource.is_success(response):
            responseJson = response.json()
            logs = []
            for log in responseJson['logs']:
                logs.append(Log(**log))
            return {'logs':logs,'count': responseJson['count']}
        else:
            return WiaResource.error_response(response)

class Function(WiaResource):
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
        response = post(path, kwargs)

        if WiaResource.is_success(response):
            return Function(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def delete(self, id):
        path = 'functions/' + id
        repsonse = delete(path)

        if WiaResource.is_success(response):
            return WiaResourceDelete(**response.json())
        else:
            return WiaResource.error_response(response)

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
        response = get('functions', **kwargs)
        if WiaResource.is_success(response):
            responseJson = response.json()
            functions = []
            for func in responseJson['functions']:
                functions.append(Function(**func))
            return {'functions':functions,'count': responseJson['count']}
        else:
            return WiaResource.error_response(response)

class Customer(WiaResource):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.username = (kwargs['username'] if 'username' in kwargs else None)
        self.email = (kwargs['email'] if 'email' in kwargs else None)
        self.fullName = (kwargs['fullName'] if 'fullName' in kwargs else None)

    @classmethod
    def signup(self, **kwargs):
        response = post('customers/signup', kwargs)
        if WiaResource.is_success(response):
            return Customer(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def create(self, **kwargs):
        path = 'customers'
        response = post(path, kwargs)
        if WiaResource.is_success(response):
            return Customer(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def retrieve(self, id):
        path = 'customers/' + id
        response = get(path)
        if WiaResource.is_success(response):
            return Customer(**response.json())
        else:
            return WiaResource.error_response(response)

    def delete(self, id):
        path = 'customers/' + id
        repsonse = delete(path)

        if WiaResource.is_success(response):
            return WiaResourceDelete(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def list(self, **kwargs):
        response = get('customers', **kwargs)
        if WiaResource.is_success(response):
            responseJson = response.json()
            customers = []
            for customer in responseJson['customers']:
                customers.append(Customer(**customer))
            return {'customers':customers,'count': responseJson['count']}
        else:
            return WiaResource.error_response(response)

class AccessToken(WiaResource):
    def __init__(self, **kwargs):
        self.accessToken = (kwargs['accessToken'] if 'accessToken' in kwargs else None)
        self.refreshToken = (kwargs['refreshToken'] if 'refreshToken' in kwargs else None)
        self.tokenType = (kwargs['tokenType'] if 'tokenType' in kwargs else None)
        self.expiresIn = (kwargs['expiresIn'] if 'expiresIn' in kwargs else None)
        self.scope = (kwargs['scope'] if 'scope' in kwargs else None)

    @classmethod
    def create(self, **kwargs):
        response = post('auth/token', kwargs)
        if WiaResource.is_success(response):
            return AccessToken(**response.json())
        else:
            return WiaResource.error_response(response)

class WhoAmI(WiaResource):
    def __init__(self, **kwargs):
        self.contextData = (kwargs['contextData'] if 'contextData' in kwargs else None)
        self.scope = (kwargs['scope'] if 'scope' in kwargs else None)

    @classmethod
    def retrieve(self):
        response = get('whoami')
        if WiaResource.is_success(response):
            return WhoAmI(**response.json())
        else:
            return WiaResource.error_response(response)
