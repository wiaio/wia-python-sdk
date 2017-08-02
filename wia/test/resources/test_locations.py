try:
    import unittest2 as unittest
except ImportError:
    import unittest

import logging
import time
import os

from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class LocationsTest(unittest.TestCase):
    def test_locations_publish(self):
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
        self.assertTrue(wia.Stream.connect)
        location = wia.Location.publish(latitude=50, longitude=60)
        self.assertTrue(location is not None)
        wia.Stream.disconnect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        self.assertFalse(wia.Stream.connected)
        wia.access_token = None

    def test_locations_list(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Location.list(device=os.environ['device_id'], limit=10, page=0)
        self.__class__.locations_count = result['count']
        self.assertTrue('locations' in result)
        self.assertTrue(type(result['locations']) == list)
        self.assertTrue('count' in result)
        self.assertTrue(type(result['count']) == int)
        wia.access_token = None

    def test_locations_list_order_desc(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Location.list(device=os.environ['device_id'], limit=10, page=0, order='timestamp', sort='desc')
        locations_list = []
        #for location in result['locations']:
            #print location.timestamp
        wia.access_token = None

    def test_locations_list_order_asc(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Location.list(device=os.environ['device_id'], limit=10, page=0, order='timestamp', sort='asc')
        locations_list = []
        #for location in result['locations']:
            #print location.timestamp
        wia.access_token = None

    def test_locations_list_since_until(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        hour_ago = int((time.time())*1000 - 3600000)
        result = wia.Location.list(device=os.environ['device_id'], order='timestamp', sort='desc', since=hour_ago)
        self.assertTrue(type(result['count']) == int)
        result = {}
        result = wia.Location.list(device=os.environ['device_id'], order='timestamp', sort='desc', until=hour_ago)
        self.assertTrue(type(result['count']) == int)
        wia.access_token = None

    def test_locations_subscribe(self):
        wia = Wia()
        def location_function(payload):
            pass
        wia.access_token = os.environ['org_secret_key']
        wia.Stream.connect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                time.sleep(1)
                break
        self.assertTrue(wia.Stream.connected)

        # subscribe to location
        wia.Location.subscribe(device=os.environ['device_id'], func=location_function)
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

        # publish location
        wia.access_token = os.environ['device_secret_key']

        wia.Stream.connect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                break
        self.assertTrue(wia.Stream.connected)

        wia.Location.publish(longitude=60, latitude=50)

        wia.access_token = os.environ['org_secret_key']
        time.sleep(0.5)

        # unsubscribe from location
        initial_subscribe_count = wia.Stream.subscribed_count
        wia.Location.unsubscribe(device=os.environ['device_id'])
        count = 0
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
    def test_location_publish_not_authorized(self):
        wia = Wia()
        wia.Stream.disconnect()
        count = 0
        while count < 10:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        self.assertFalse(wia.Stream.connected)
        wia.access_token = os.environ['org_secret_key']
        location = wia.Location.publish(latitude=10, longitude=10)
        self.assertIsInstance(location, WiaError)
        wia.access_token = None

    def test_location_publish_wrong_params(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        location = wia.Location.publish(name='fail')
        self.assertIsInstance(location, WiaError)
        wia.access_token = None

    def test_list_location_not_found(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Location.list(device='Unknown')
        self.assertIsInstance(result, WiaError)
        wia.access_token = None

if __name__ == '__main__':
    unittest2.main()
