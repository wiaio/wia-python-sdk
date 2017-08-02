try:
    import unittest2 as unittest
except ImportError:
    import unittest

import logging
import time
import os

from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class SensorsTest(unittest.TestCase):
    def test_sensors_publish_rest(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        sensor = wia.Sensor.publish(name='test_sensor_rest_1', data=99)
        self.assertTrue(sensor is not None)
        wia.access_token = None

    def test_sensors_publish(self):
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
        sensor = wia.Sensor.publish(name='test_sensor_mqtt', data=130)
        self.assertTrue(sensor is not None)
        wia.Stream.disconnect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        self.assertFalse(wia.Stream.connected)
        wia.access_token = None

    def test_sensors_list(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Sensor.list(device=os.environ['device_id'], limit=10, page=0)
        #print('LIST', result)
        self.__class__.sensor_count = result['count']
        self.assertTrue('sensors' in result)
        self.assertTrue(type(result['sensors']) == list)
        self.assertTrue('count' in result)
        self.assertTrue(type(result['count']) == int)
        wia.access_token = None

    def test_sensors_list_name(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Sensor.list(device = os.environ['device_id'], name='test_sensor_1')
        self.assertFalse('error' in result)
        for sensor in result['sensors']:
            self.assertEqual('test_sensor_1', sensor.name)
        wia.access_token = None

    def test_sensors_list_since_until(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        hour_ago = int((time.time())*1000 - 3600000)
        result = wia.Sensor.list(device=os.environ['device_id'], order='timestamp', sort='desc', since=hour_ago)
        self.assertFalse('error' in result)
        self.assertTrue('count' in result)
        self.assertTrue(type(result['count']) == int)
        wia.access_token = None

    def test_sensors_subscribe(self):
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

        # subscirbe to sensor
        wia.Sensor.subscribe(device=os.environ['device_id'], func=wildcard_function)
        wia.Sensor.subscribe(device=os.environ['device_id'], name='subscribe_test_sensor', func=specific_function)
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

        # publish sensor data
        wia.access_token = os.environ['device_secret_key']

        wia.Stream.connect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                break
        self.assertTrue(wia.Stream.connected)

        wia.Sensor.publish(name='subscribe_test_sensor', data=29)

        wia.access_token = os.environ['org_secret_key']
        time.sleep(0.5)

        count = 0
        initial_subscribe_count = wia.Stream.subscribed_count

        # unsubscribe from sensor
        wia.Sensor.unsubscribe(device=os.environ['device_id'])
        wia.Sensor.unsubscribe(device=os.environ['device_id'], name='subscribe_test_sensor')
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

    # ERROR TESTING
    def test_publish_sensor_not_authorized(self):
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
        wia.access_token = os.environ['org_secret_key']
        sensor = wia.Sensor.publish(name='fail', data=401)
        self.assertIsInstance(sensor, WiaError)
        wia.access_token = None

    def test_publish_sensor_wrong_params(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        sensor = wia.Sensor.publish(abc='not_param')
        self.assertIsInstance(sensor, WiaError)
        wia.access_token = None

    def test_list_sensor_not_found(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Sensor.list(device='Unknown')
        self.assertIsInstance(result, WiaError)
        wia.access_token = None

if __name__ == '__main__':
    unittest2.main()
