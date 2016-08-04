import wia
import unittest2
import time
import os

class SensorsTest(unittest2.TestCase):
    timeout = 100000000
    mailbox = {}

    def test_sensors_publish(self):
        wia.secret_key = os.environ['device_secret_key']
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
        wia.secret_key = None

    def test_sensors_list(self):
        wia.secret_key = os.environ['org_secret_key']
        list_return = wia.Sensor.list(device=wia.device_id, limit=10, page=0)
        self.__class__.sensor_count = list_return['count']
        self.assertTrue(list_return['sensors'])
        self.assertTrue(type(list_return['sensors']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)
        wia.secret_key = None

    def test_sensors_list_order_sort(self):
        wia.secret_key = os.environ['org_secret_key']
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
        wia.secret_key = None

    def test_sensors_list_name(self):
        wia.secret_key = os.environ['org_secret_key']
        list_return = wia.Sensor.list(device = wia.device_id, name='test_sensor_1')
        for sensor in list_return['sensors']:
            self.assertEqual('test_sensor_1', sensor['name'])
        wia.secret_key = None

    def test_sensors_list_since_until(self):
        wia.secret_key = os.environ['org_secret_key']
        hour_ago = int((time.time())*1000 - 3600000)
        list_return = wia.Sensor.list(device=wia.device_id, order='timestamp', sort='desc', since=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.sensor_count)
        list_return = {}
        list_return = wia.Sensor.list(device=wia.device_id, order='timestamp', sort='desc', until=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.sensor_count)
        wia.secret_key = None

    def test_sensors_subscribe(self):
        pass
        # wia.secret_key = os.environ['org_secret_key']
        # self.__class__.mailbox = {}
        # def wildcard_function(payload):
        #     pass
        # def specific_function(payload):
        #     self.__class__.mailbox = payload
        # wia.Stream.connect()
        # count = 0
        # while count < self.timeout:
        #     count += 1
        #     if wia.Stream.connected:
        #         break
        # if not wia.Stream.connected:
        #     raise Exception("Unable to connect")
        # wia.Sensor.subscribe(device=wia.device_id, func=wildcard_function)
        # wia.Sensor.subscribe(device=wia.device_id, func=specific_function, name='subscribe_test_sensor')
        #
        # wia.secret_key = os.environ['device_secret_key']
        # wia.Sensor.publish(name='subscribe_test_sensor', data=99)
        #
        # # wia.secret_key = os.environ['org_secret_key']
        #
        # self.assertEqual(self.__class__.mailbox['name'], 'subscribe_test_sensor')
        # self.assertEqual(self.__class__.mailbox['data'], 99)
        # wia.Sensor.unsubscribe(device=wia.device_id, name='subscribe_test_sensor')
        # wia.Sensor.unsubscribe(device=wia.device_id)
        #
        # count = 0
        # initial_subscribe_count = wia.Stream.subscribed_count
        # while count < self.timeout:
        #     count += 1
        #     if wia.Stream.subscribed_count < initial_subscribe_count:
        #         break
        # if wia.Stream.subscribed_count == initial_subscribe_count:
        #     raise Exception("Unable to unsubscribe")
        # wia.secret_key = None

if __name__ == '__main__':
    unittest2.main()
