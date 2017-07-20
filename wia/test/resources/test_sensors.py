import wia
import unittest2
import time
import os
import logging

class SensorsTest(unittest2.TestCase):
    timeout = 100000000
    mailbox = {}

    def test_sensors_publish_rest(self):
        wia.secret_key = os.environ['device_secret_key']
        publish_return = wia.Sensor.publish(name='test_sensor_rest_1', data=99)
        self.assertTrue(publish_return['id'])
        wia.secret_key = None

    def test_sensors_publish(self):
        wia.secret_key = os.environ['device_secret_key']
        wia.Stream.connect()
        count = 0
        while count < 6:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                time.sleep(1)
                break
        if not wia.Stream.connected:
            raise Exception("Unable to connect")
        wia.Sensor.publish(name='test_sensor_mqtt', data=130)
        wia.Stream.disconnect()
        count = 0
        while count < 6:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        if wia.Stream.connected:
            raise Exception("Unable to disconnect")
        wia.secret_key = None

    def test_sensors_list(self):
        wia.secret_key = os.environ['org_secret_key']
        result = wia.Sensor.list(device=os.environ['device_id'], limit=10, page=0)
        self.__class__.sensor_count = result['count']
        self.assertTrue(result['sensors'])
        self.assertTrue(type(result['sensors']) == list)
        self.assertTrue(result['count'])
        self.assertTrue(type(result['count']) == int)
        wia.org_secret_key = None

    def test_sensors_list_name(self):
        wia.secret_key = os.environ['org_secret_key']
        # could be temporary fix? will this only take one sensor and not multiple?
        result = wia.Sensor.list(device = os.environ['device_id'], name='test_sensor_1')
        self.assertFalse(result.has_key('error'))
        for sensor in result['sensors']:
            self.assertEqual('test_sensor_1', sensor['name'])
        wia.secret_key = None

    def test_sensors_list_since_until(self):
        wia.secret_key = os.environ['org_secret_key']
        hour_ago = int((time.time())*1000 - 3600000)
        result = wia.Sensor.list(device=os.environ['device_id'], order='timestamp', sort='desc', since=hour_ago)
        self.assertFalse(result.has_key('error'))
        self.assertTrue(result.has_key('count'))
        self.assertTrue(type(result['count']) == int)
        wia.secret_key = None

    def test_sensors_subscribe(self):
        self.__class__.mailbox = {}
        def wildcard_function(payload):
            pass
        def specific_function(payload):
            self.__class__.mailbox = payload
        wia.secret_key = os.environ['org_secret_key']
        wia.Stream.connect()
        count = 0
        # waits for Stream to be connected
        while count < 6:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                time.sleep(1)
                break
        if not wia.Stream.connected:
            raise Exception("Unable to connect")

        # subscirbe to sensor
        wia.Sensor.subscribe(device=os.environ['device_id'], func=wildcard_function)
        wia.Sensor.subscribe(device=os.environ['device_id'], name='subscribe_test_sensor', func=specific_function)
        count = 0
        while count < 6:
            time.sleep(0.5)
            count += 1
            if wia.Stream.subscribed:
                time.sleep(1)
                break
        if not wia.Stream.subscribed:
            raise Exception("Unable to subscribe")

        wia.Stream.disconnect()
        count = 0
        while count < 6:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        if wia.Stream.connected:
            raise Exception("Unable to disconnect")

        # publish sensor data
        wia.secret_key = os.environ['device_secret_key']

        wia.Stream.connect()
        count = 0
        while count < 6:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                break
        if not wia.Stream.connected:
            raise Exception("Unable to connect")

        wia.Sensor.publish(name='subscribe_test_sensor', data=29)

        wia.secret_key = os.environ['org_secret_key']
        time.sleep(0.5)

        count = 0
        initial_subscribe_count = wia.Stream.subscribed_count

        # unsubscribe from sensor
        wia.Sensor.unsubscribe(device=os.environ['device_id'])
        wia.Sensor.unsubscribe(device=os.environ['device_id'], name='subscribe_test_sensor')
        while count < 6:
            time.sleep(0.5)
            count += 1
            if wia.Stream.subscribed_count < initial_subscribe_count:
                break
        if wia.Stream.subscribed_count == initial_subscribe_count:
            raise Exception("Unable to unsubscribe")
        wia.Stream.disconnect()
        count = 0
        while count < 6:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        if wia.Stream.connected:
            raise Exception("Unable to disconnect")
        wia.secret_key = None

if __name__ == '__main__':
    unittest2.main()
