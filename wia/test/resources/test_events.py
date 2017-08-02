try:
    import unittest2 as unittest
except ImportError:
    import unittest

import logging
import time
import os

from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class EventsTest(unittest.TestCase):
    def test_events_publish_rest(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        event = wia.Event.publish(name='test_event_other_rest', data=130)
        #print event
        self.assertTrue(event.id is not None)
        wia.access_token = None

    def test_events_publish(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        wia.Stream.connect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                time.sleep(1)
                break
        self.assertTrue(wia.Stream.connected)
        result = wia.Event.publish(name='test_event_mqtt', data=130)
        self.assertTrue(result is not None)
        wia.Stream.disconnect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        self.assertFalse(wia.Stream.connected)
        wia.access_token = None

    def test_events_publish_file(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        result = wia.Event.publish(name='test_event_other_filesud', data=1300, file=open('image.jpg', 'rb'))
        wia.access_token = None

    def test_device_org_retrieve(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        wia.Stream.connect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                time.sleep(1)
                break
        self.assertTrue(wia.Stream.connected)
        publish = wia.Event.publish(name='device_org_test_event', data=99)
        wia.access_token = os.environ['org_secret_key']
        response = wia.Device.retrieve(os.environ['device_id'])
        self.assertEqual(response.events['device_org_test_event']['name'], 'device_org_test_event')
        wia.access_token = None

    def test_events_list(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Event.list(device=os.environ['device_id'], limit=10, page=0)
        self.__class__.event_count = result['count']
        self.assertTrue('events' in result)
        self.assertTrue(type(result['events']) == list)
        self.assertTrue('count' in result)
        self.assertTrue(type(result['count']) == int)
        wia.access_token = None

    def test_events_list_order_desc(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Event.list(device=os.environ['device_id'], limit=10, page=0, order='timestamp', sort='desc')
        events_list = []
        #for event in result['events']:
            #print event.timestamp
        wia.access_token = None

    def test_events_list_order_asc(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Event.list(device=os.environ['device_id'], limit=10, page=0, order='timestamp', sort='asc')
        events_list = []
        #for event in result['events']:
            #print event.timestamp
        wia.access_token = None

    def test_events_list_name(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Event.list(device = os.environ['device_id'], name='test_event')
        for event in result['events']:
            self.assertEqual('test_event', event['name'])
        wia.access_token = None

    def test_events_list_since_until(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        hour_ago = int((time.time())*1000 - 3600000)
        result = wia.Event.list(device=os.environ['device_id'], order='timestamp', sort='desc', since=hour_ago)
        self.assertTrue(type(result['count']) == int)
        result = {}
        result = wia.Event.list(device=os.environ['device_id'], order='timestamp', sort='desc', until=hour_ago)
        self.assertTrue(type(result['count']) == int)
        wia.access_token = None

    def test_events_subscribe(self):
        wia = Wia()
        def wildcard_function(payload):
            pass
        def specific_function(payload):
            pass
        wia.access_token = os.environ['org_secret_key']
        wia.Stream.connect()
        count = 0
        # waits for Stream to be connected
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                time.sleep(1)
                break
        self.assertTrue(wia.Stream.connected)

        # subscirbe to event
        wia.Event.subscribe(device=os.environ['device_id'], func=wildcard_function)
        wia.Event.subscribe(device=os.environ['device_id'], name='subscribe_test_event', func=specific_function)
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.subscribed:
                time.sleep(1)
                break
        self.assertTrue(wia.Stream.subscribed)

        wia.Stream.disconnect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        self.assertFalse(wia.Stream.connected)

        # publish event data
        wia.access_token = os.environ['device_secret_key']

        wia.Stream.connect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                break
        self.assertTrue(wia.Stream.connected)

        wia.Event.publish(name='subscribe_test_event', data=97)

        wia.access_token = os.environ['org_secret_key']
        time.sleep(0.5)

        count = 0
        initial_subscribe_count = wia.Stream.subscribed_count
        #print(initial_subscribe_count)

        # unsubscribe from event
        wia.Event.unsubscribe(device=os.environ['device_id'])
        wia.Event.unsubscribe(device=os.environ['device_id'], name='subscribe_test_event')
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.subscribed_count < initial_subscribe_count:
                break
        self.assertTrue(wia.Stream.subscribed_count < initial_subscribe_count)
        wia.Stream.disconnect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        self.assertFalse(wia.Stream.connected)
        wia.access_token = None

    # ERROR TESTS
    def test_events_publish_rest_error(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        result = wia.Event.publish(abc='def')
        self.assertIsInstance(result, WiaError)
        wia.access_token = None

    def test_event_publish_not_authorized(self):
        wia = Wia()
        wia.Stream.disconnect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                time.sleep(1)
                break
        self.assertFalse(wia.Stream.connected)
        wia.access_token = os.environ['user_secret_key']
        event = wia.Event.publish(name='fail', data=100)
        self.assertIsInstance(event, WiaError)
        wia.access_token = None

    def test_event_publish_wrong_params(self):
        wia = Wia()
        wia.access_token = os.environ['user_secret_key']
        event = wia.Event.publish(abc='wrong_param')
        self.assertIsInstance(event, WiaError)
        wia.access_token = None

    def test_list_event_not_found(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Event.list(device='Unknown')
        self.assertIsInstance(result, WiaError)
        wia.access_token = None

if __name__ == '__main__':
    unittest.main()
