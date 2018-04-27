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

class Space(WiaResource):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.name = (kwargs['name'] if 'name' in kwargs else None)
        self.createdAt = (kwargs['createdAt'] if 'createdAt' in kwargs else None)
        self.updatedAt = (kwargs['updatedAt'] if 'updatedAt' in kwargs else None)

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a Space in Wia for devices
        :param kwargs:
        :return: Returns a newly created space
        """
        path = 'spaces'
        response = post(path, kwargs)
        if WiaResource.is_success(response):
            return cls(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def retrieve(cls, id):
        """
        Retrieves a Space by ID
        :param id: ID of the space
        :return: Instance of the Space object
        """
        path = 'spaces/' + id
        response = get(path)
        if WiaResource.is_success(response):
            return cls(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def update(cls, **kwargs):
        path = 'spaces/' + kwargs['id']
        dictCopy = dict(kwargs)
        del dictCopy['id']
        response = put(path, dictCopy)
        if WiaResource.is_success(response):
            return cls(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def list(cls, **kwargs):
        response = get('spaces', **kwargs)
        if WiaResource.is_success(response):
            responseJson = response.json()
            spaces = []
            for space in responseJson['spaces']:
                spaces.append(cls(**space))
            return {'spaces':spaces,'count': responseJson['count']}
        else:
            return WiaResource.error_response(response)


class Device(WiaResource):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.name = (kwargs['name'] if 'name' in kwargs else None)
        self.events = (kwargs['events'] if 'events' in kwargs else None)
        self.location = (kwargs['location'] if 'location' in kwargs else None)
        self.createdAt = (kwargs['createdAt'] if 'createdAt' in kwargs else None)
        self.updatedAt = (kwargs['updatedAt'] if 'updatedAt' in kwargs else None)

    @classmethod
    def create(cls, **kwargs):
        path = 'devices'
        response = post(path, kwargs)
        if WiaResource.is_success(response):
            return cls(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def retrieve(cls, id):
        path = 'devices/' + id
        response = get(path)
        if WiaResource.is_success(response):
            return cls(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def update(cls, **kwargs):
        path = 'devices/' + kwargs['id']
        dictCopy = dict(kwargs)
        #del dictCopy['id']
        response = put(path, dictCopy)
        if WiaResource.is_success(response):
            return cls(**response.json())
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

    @classmethod
    def list(cls, **kwargs):
        response = get('devices', **kwargs)
        if WiaResource.is_success(response):
            responseJson = response.json()
            devices = []
            for device in responseJson['devices']:
                devices.append(cls(**device))
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
    def publish(cls, **kwargs):
        path = 'events'
        if not ('file' in kwargs) and Wia().Stream.connected and Wia().client_id is not None:
            topic = 'devices/' + Wia().client_id + '/' + path + '/' + kwargs['name']
            Wia().Stream.publish(topic=topic, **kwargs)
            return cls()
        else:
            response = post(path, kwargs)
            if WiaResource.is_success(response):
                return cls(**response.json())
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

    @classmethod
    def list(cls, **kwargs):
        response = get('events', **kwargs)
        if WiaResource.is_success(response):
            responseJson = response.json()
            events = []
            for event in responseJson['events']:
                events.append(cls(**event))
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
            return cls()
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

    @classmethod
    def list(cls, **kwargs):
        response = get('locations', **kwargs)
        if WiaResource.is_success(response):
            responseJson = response.json()
            locations = []
            for location in responseJson['locations']:
                locations.append(cls(**location))
            return {'locations':locations,'count': responseJson['count']}
        else:
            return WiaResource.error_response(response)

class Command(WiaResource):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.name = (kwargs['name'] if 'name' in kwargs else None)
        self.slug = (kwargs['slug'] if 'slug' in kwargs else None)
        self.createdAt = (kwargs['createdAt'] if 'createdAt' in kwargs else None)
        self.updatedAt = (kwargs['updatedAt'] if 'updatedAt' in kwargs else None)

    @classmethod
    def create(cls, **kwargs):
        path = 'commands'
        response = post(path, kwargs)
        if WiaResource.is_success(response):
            return cls(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def retrieve(cls, id):
        path = 'commands/' + id
        response = get(path)
        if WiaResource.is_success(response):
            return cls(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def update(cls, **kwargs):
        path = 'commands/' + kwargs['id']
        dictCopy = dict(kwargs)
        del dictCopy['id']
        response = put(path, dictCopy)
        if WiaResource.is_success(response):
            return cls(**response.json())
        else:
            return WiaResource.error_response(response)

    @staticmethod
    def delete(id):
        path = 'commands/' + id
        response = delete(path)
        if WiaResource.is_success(response):
            return WiaResourceDelete(**response.json())
        else:
            return WiaResource.error_response(response)

    @classmethod
    def list(cls, **kwargs):
        response = get('commands', **kwargs)
        if WiaResource.is_success(response):
            responseJson = response.json()
            commands = []
            for command in responseJson['commands']:
                commands.append(cls(**command))
            return {'commands':commands,'count': responseJson['count']}
        else:
            return WiaResource.error_response(response)

    @staticmethod
    def subscribe(**kwargs):
        topic='devices/' + kwargs['device'] + '/commands/' + kwargs['slug'] + '/run'
        Wia().Stream.subscribe(topic=topic, func=kwargs['func'])

    @staticmethod
    def unsubscribe(**kwargs):
        topic='devices/' + kwargs['device'] + '/commands/' + kwargs['slug'] + '/run'
        Wia().Stream.unsubscribe(topic=topic)

    @classmethod
    def run(cls, **kwargs):

        if Wia().Stream.connected and Wia().client_id is not None:
            command = 'devices/' + Wia().client_id + '/commands/' + (kwargs['slug'] or kwargs['name']) + '/run'
            Wia().Stream.run(command=command)
            return cls()
        else:
            response = post('commands/run', kwargs)
            if WiaResource.is_success(response):
                return cls(**response.json())
            else:
                return WiaResource.error_response(response)


# class Log(WiaResource):
#     def __init__(self, **kwargs):
#         self.level = (kwargs['level'] if 'level' in kwargs else None)
#         self.message = (kwargs['message'] if 'message' in kwargs else None)
#         self.data = (kwargs['data'] if 'data' in kwargs else None)
#         self.timestamp = (kwargs['timestamp'] if 'timestamp' in kwargs else None)
#
#     @classmethod
#     def publish(cls, **kwargs):
#         path = 'logs'
#         if Wia().Stream.connected and Wia().client_id is not None:
#             topic = 'devices/' + Wia().client_id + '/' + path + '/' + kwargs['level']
#             Wia().Stream.publish(topic=topic, **kwargs)
#             return cls()
#         else:
#             response = post(path, kwargs)
#             if WiaResource.is_success(response):
#                 return cls(**response.json())
#             else:
#                 return WiaResource.error_response(response)
#
#     @staticmethod
#     def subscribe(**kwargs):
#         device=kwargs['device']
#         topic='devices/' + device + '/logs/'
#         if 'level' in kwargs:
#             topic += kwargs['level']
#         else:
#             topic += '+'
#         Wia().Stream.subscribe(topic=topic, func=kwargs['func'])
#
#     @staticmethod
#     def unsubscribe(**kwargs):
#         device=kwargs['device']
#         topic='devices/' + device + '/logs/'
#         if 'level' in kwargs:
#             topic += kwargs['level']
#         else:
#             topic += '+'
#         Wia().Stream.unsubscribe(topic=topic)
#
#     @classmethod
#     def list(cls, **kwargs):
#         response = get('logs', **kwargs)
#         if WiaResource.is_success(response):
#             responseJson = response.json()
#             logs = []
#             for log in responseJson['logs']:
#                 logs.append(cls(**log))
#             return {'logs':logs,'count': responseJson['count']}
#         else:
#             return WiaResource.error_response(response)


class AccessToken(WiaResource):
    def __init__(self, **kwargs):
        self.accessToken = kwargs['token'] if 'token' in kwargs else None
        self.refreshToken = (kwargs['refreshToken'] if 'refreshToken' in kwargs else None)
        self.tokenType = (kwargs['tokenType'] if 'tokenType' in kwargs else None)
        self.expiresIn = (kwargs['expiresIn'] if 'expiresIn' in kwargs else None)
        self.scope = (kwargs['scope'] if 'scope' in kwargs else None)

    @classmethod
    def create(cls, kwargs):
        response = post('auth/token', kwargs)
        if WiaResource.is_success(response):
            return cls(**response.json())
        else:
            return WiaResource.error_response(response)

class WhoAmI(WiaResource):
    def __init__(self, **kwargs):
        self.id = (kwargs['id'] if 'id' in kwargs else None)
        self.contextData = (kwargs['contextData'] if 'contextData' in kwargs else None)
        self.scope = (kwargs['scope'] if 'scope' in kwargs else None)

    @classmethod
    def retrieve(cls):
        response = get('whoami')
        if WiaResource.is_success(response):
            return cls(**response.json())
        else:
            return WiaResource.error_response(response)
