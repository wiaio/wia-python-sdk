import wia
import unittest2
import time
import os

class SensorsTest(unittest2.TestCase):
    timeout = 100000000
    mailbox = {}

    def test_sensors_publish(self):
        wia.secret_key = wia.device_secret_key
        wia.Stream.connect()
        count = 0
        while count < self.timeout:
            count += 1
            if wia.Stream.connected:
                break
        if not wia.Stream.connected:
            raise Exception("Unable to connect")
        publish_return = wia.Sensor.publish(name='test_sensor_1', data=99)
        self.assertTrue(publish_return['id'])
        wia.Stream.disconnect()
        count = 0
        while count < self.timeout:
            count += 1
            if not wia.Stream.connected:
                break
        if wia.Stream.connected:
            raise Exception("Unable to disconnect")

    def test_sensors_list(self):
        list_return = wia.Sensor.list(device=wia.device_id, limit=10, page=0)
        self.__class__.sensor_count = list_return['count']
        self.assertTrue(list_return['sensors'])
        self.assertTrue(type(list_return['sensors']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)

    def test_sensors_list_order_sort(self):
        list_return = wia.Sensor.list(device=wia.device_id, limit=10, page=0, order='timestamp', sort='desc')
        timestamp_list = []
        for sensor in list_return['sensors']:
            timestamp_list.append(sensor['timestamp'])
        descending = timestamp_list[:]
        descending.sort(reverse=True)
        self.assertEqual(descending, timestamp_list)
        list_return = wia.Sensor.list(device=wia.device_id, limit=10, page=0, order='timestamp', sort='asc')
        timestamp_list = []
        for sensor in list_return['sensors']:
            timestamp_list.append(sensor['timestamp'])
        ascending = timestamp_list[:]
        ascending.sort()
        self.assertEqual(ascending, timestamp_list)

    def test_sensors_list_name(self):
        list_return = wia.Sensor.list(device = wia.device_id, name='test_sensor_1')
        for sensor in list_return['sensors']:
            self.assertEqual('test_sensor_1', sensor['name'])

    def test_sensors_list_since_until(self):
        hour_ago = int((time.time())*1000 - 3600000)
        list_return = wia.Sensor.list(device=wia.device_id, order='timestamp', sort='desc', since=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.sensor_count)
        list_return = {}
        list_return = wia.Sensor.list(device=wia.device_id, order='timestamp', sort='desc', until=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.sensor_count)

    def test_sensors_subscribe(self):
        self.__class__.mailbox = {}
        def wildcard_function(payload):
            pass
        def specific_function(payload):
            self.__class__.mailbox = payload
        wia.Stream.connect()
        count = 0
        while count < self.timeout:
            count += 1
            if wia.Stream.connected:
                break
        if not wia.Stream.connected:
            raise Exception("Unable to connect")
        wia.Sensor.subscribe(device=wia.device_id, func=wildcard_function)
        wia.Sensor.subscribe(device=wia.device_id, func=specific_function, name='subscribe_test_sensor')
        count = 0
        while count < self.timeout:
            count += 1
            if wia.Stream.subscribed:
                break
        if not wia.Stream.subscribed:
            raise Exception("Unable to subscribe")
        temp_sk = wia.secret_key
        wia.secret_key = wia.device_secret_key
        wia.Sensor.publish(name='subscribe_test_sensor', data=99)
        wia.secret_key = temp_sk
        time.sleep(5)
        self.assertEqual(self.__class__.mailbox['name'], 'subscribe_test_sensor')
        self.assertEqual(self.__class__.mailbox['data'], 99)
        wia.Sensor.unsubscribe(device=wia.device_id, name='subscribe_test_sensor')
        wia.Sensor.unsubscribe(device=wia.device_id)
        count = 0
        initial_subscribe_count = wia.Stream.subscribed_count
        while count < self.timeout:
            count += 1
            if wia.Stream.subscribed_count < initial_subscribe_count:
                break
        if wia.Stream.subscribed_count == initial_subscribe_count:
            raise Exception("Unable to unsubscribe")

if __name__ == '__main__':
    unittest2.main()
