import wia
import unittest2
import time
import os

class SensorsTest(unittest2.TestCase):
    mailbox = {}

    def test_sensors_publish(self):
        wia.secret_key = wia.device_secret_key
        publish_return = wia.Sensors.publish(name='test_sensor_1', data=99)
        self.assertTrue(publish_return['id'])

    def test_sensors_list(self):
        list_return = wia.Sensors.list(device=wia.device_id, limit=10, page=0)
        self.__class__.sensor_count = list_return['count']
        self.assertTrue(list_return['sensors'])
        self.assertTrue(type(list_return['sensors']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)

    def test_sensors_list_order_sort(self):
        list_return = wia.Sensors.list(device=wia.device_id, limit=10, page=0, order='timestamp', sort='desc')
        timestamp_list = []
        for sensor in list_return['sensors']:
            timestamp_list.append(sensor['timestamp'])
        descending = timestamp_list[:]
        descending.sort(reverse=True)
        self.assertEqual(descending, timestamp_list)
        list_return = wia.Sensors.list(device=wia.device_id, limit=10, page=0, order='timestamp', sort='asc')
        timestamp_list = []
        for sensor in list_return['sensors']:
            timestamp_list.append(sensor['timestamp'])
        ascending = timestamp_list[:]
        ascending.sort()
        self.assertEqual(ascending, timestamp_list)

    def test_sensors_list_name(self):
        list_return = wia.Sensors.list(device = wia.device_id, name='test_sensor_1')
        for sensor in list_return['sensors']:
            self.assertEqual('test_sensor_1', sensor['name'])

    def test_sensors_list_since_until(self):
        hour_ago = int((time.time())*1000 - 3600000)
        list_return = wia.Sensors.list(device=wia.device_id, order='timestamp', sort='desc', since=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.sensor_count)
        list_return = {}
        list_return = wia.Sensors.list(device=wia.device_id, order='timestamp', sort='desc', until=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.sensor_count)

    def test_sensors_subscribe(self):
        self.__class__.mailbox = {}
        def wildcard_function(payload):
            pass
        def specific_function(payload):
            self.__class__.mailbox = payload
        wia.Stream.connect()
        while wia.Stream.connected == False:
            pass
        print("HERE")
        wia.Sensors.subscribe(device='dev_4sEIfy5QbtIdYO5k', func=wildcard_function)
        wia.Sensors.subscribe(device='dev_4sEIfy5QbtIdYO5k', func=specific_function, name='subscribe_test_sensor')
        while wia.Stream.subscribed is not True:
            pass
        wia.Sensors.publish(name='subscribe_test_sensor', data=99)
        time.sleep(5)
        self.assertEqual(self.__class__.mailbox['name'], 'subscribe_test_sensor')
        self.assertEqual(self.__class__.mailbox['data'], 99)
        wia.Sensors.unsubscribe(device='dev_4sEIfy5QbtIdYO5k', name='subscribe_test_sensor')
        wia.Sensors.unsubscribe(device='dev_4sEIfy5QbtIdYO5k')
        while wia.Stream.subscribed:
            pass
        self.assertEqual(wia.Stream.subscribed, False)

if __name__ == '__main__':
    unittest2.main()
