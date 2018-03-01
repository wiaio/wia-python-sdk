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
        self.assertTrue(event.id is not None)
        wia.access_token = None

    # def test_events_publish(self):
    #     wia = Wia()
    #     wia.access_token = os.environ['device_secret_key']
    #     wia.Stream.connect()
    #     count = 0
    #     while count <= 10:
    #         time.sleep(0.5)
    #         count += 1
    #         if wia.Stream.connected:
    #             time.sleep(1)
    #             break
    #     self.assertTrue(wia.Stream.connected)
    #     result = wia.Event.publish(name='test_event_mqtt', data=130)
    #     self.assertTrue(result is not None)
    #     wia.Stream.disconnect()
    #     count = 0
    #     while count <= 10:
    #         time.sleep(0.5)
    #         count += 1
    #         if not wia.Stream.connected:
    #             break
    #     self.assertFalse(wia.Stream.connected)
    #     wia.access_token = None

    # def test_events_subscribe(self):
    #     wia = Wia()
    #     def wildcard_function(payload):
    #         pass
    #     def specific_function(payload):
    #         pass
    #     wia.access_token = os.environ['org_secret_key']
    #     wia.Stream.connect()
    #     count = 0
    #     # waits for Stream to be connected
    #     while count <= 10:
    #         time.sleep(0.5)
    #         count += 1
    #         if wia.Stream.connected:
    #             time.sleep(1)
    #             break
    #     self.assertTrue(wia.Stream.connected)
    #
    #     # subscirbe to event
    #     wia.Event.subscribe(device=os.environ['device_id'], func=wildcard_function)
    #     wia.Event.subscribe(device=os.environ['device_id'], name='subscribe_test_event', func=specific_function)
    #     count = 0
    #     while count <= 10:
    #         time.sleep(0.5)
    #         count += 1
    #         if wia.Stream.subscribed:
    #             time.sleep(1)
    #             break
    #     self.assertTrue(wia.Stream.subscribed)
    #
    #     wia.Stream.disconnect()
    #     count = 0
    #     while count <= 10:
    #         time.sleep(0.5)
    #         count += 1
    #         if not wia.Stream.connected:
    #             break
    #     self.assertFalse(wia.Stream.connected)
    #
    #     # publish event data
    #     wia.access_token = os.environ['device_secret_key']
    #
    #     wia.Stream.connect()
    #     count = 0
    #     while count <= 10:
    #         time.sleep(0.5)
    #         count += 1
    #         if wia.Stream.connected:
    #             break
    #     self.assertTrue(wia.Stream.connected)
    #
    #     wia.Event.publish(name='subscribe_test_event', data=97)
    #
    #     wia.access_token = os.environ['org_secret_key']
    #     time.sleep(0.5)
    #
    #     count = 0
    #     initial_subscribe_count = wia.Stream.subscribed_count
    #     #print(initial_subscribe_count)
    #
    #     # unsubscribe from event
    #     wia.Event.unsubscribe(device=os.environ['device_id'])
    #     wia.Event.unsubscribe(device=os.environ['device_id'], name='subscribe_test_event')
    #     while count <= 10:
    #         time.sleep(0.5)
    #         count += 1
    #         if wia.Stream.subscribed_count < initial_subscribe_count:
    #             break
    #     self.assertTrue(wia.Stream.subscribed_count < initial_subscribe_count)
    #     wia.Stream.disconnect()
    #     count = 0
    #     while count <= 10:
    #         time.sleep(0.5)
    #         count += 1
    #         if not wia.Stream.connected:
    #             break
    #     self.assertFalse(wia.Stream.connected)
    #     wia.access_token = None

    # ERROR TESTS
    def test_events_publish_rest_error(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        result = wia.Event.publish(abc='def')
        self.assertIsInstance(result, WiaError)
        wia.access_token = None

if __name__ == '__main__':
    unittest.main()
