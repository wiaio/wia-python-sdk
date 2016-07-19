import wia
import unittest2
import time
import os

class LocationsTest(unittest2.TestCase):
    timeout = 100000000
    mailbox = {}

    def test_locations_publish(self):
        temp_sk = wia.secret_key
        wia.secret_key = wia.device_secret_key
        wia.Stream.connect()
        count = 0
        while(count < self.timeout):
            count += 1
            if wia.Stream.connected:
                break
        if not wia.Stream.connected:
            raise Exception("unable to connect")
        print("PUBLISHING LOCATION")
        publish_return = wia.Location.publish(latitude=50, longitude=60)
        print("SHOULD HAVE PUBLISHED LOCATION")
        self.assertTrue(publish_return['id'])
        wia.Stream.disconnect()
        count = 0
        while(count < self.timeout):
            count += 1
            if not wia.Stream.connected:
                break
        if wia.Stream.connected:
            raise Exception("Unable to disconnect")
        wia.secret_key = temp_sk

    def test_locations_list(self):
        list_return = wia.Location.list(device=wia.device_id, limit=10, page=0)
        self.__class__.locations_count = list_return['count']
        self.assertTrue(list_return['locations'])
        self.assertTrue(type(list_return['locations']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)

    def test_locations_list_order_sort(self):
        list_return = wia.Location.list(device=wia.device_id, limit=10, page=0, order='timestamp', sort='desc')
        timestamp_list = []
        for location in list_return['locations']:
            timestamp_list.append(location['timestamp'])
        descending = timestamp_list[:]
        descending.sort(reverse=True)
        self.assertEqual(descending, timestamp_list)
        list_return = wia.Location.list(device=wia.device_id, order='timestamp', sort='asc')
        timestamp_list = []
        for location in list_return['locations']:
            timestamp_list.append(location['timestamp'])
        ascending = timestamp_list[:]
        ascending.sort()
        self.assertEqual(ascending, timestamp_list)

    def test_locations_list_since_until(self):
        hour_ago = int((time.time())*1000 - 3600000)
        list_return = wia.Location.list(device=wia.device_id, order='timestamp', sort='desc', since=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.locations_count)
        list_return = {}
        list_return = wia.Location.list(device=wia.device_id, order='timestamp', sort='desc', until=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.locations_count)

    def test_locations_subscribe(self):
        self.__class__.mailbox = {}
        def location_subscription_func(payload):
            self.__class__.mailbox = payload
        wia.Stream.connect()
        count = 0
        while count < self.timeout:
            count += 1
            if wia.Stream.connected:
                break
        if not wia.Stream.connected:
            raise Exception("Unable to connect")
        wia.Location.subscribe(device=wia.device_id, func=location_subscription_func)
        count = 0
        while count < self.timeout:
            count += 1
            if wia.Stream.subscribed:
                break
        if not wia.Stream.subscribed:
            raise Exception("Unable to subscribe")
        temp_sk = wia.secret_key
        wia.secret_key = wia.device_secret_key
        publish_return = wia.Location.publish(longitude=60, latitude=50)
        wia.secret_key = temp_sk
        time.sleep(1)
        self.assertEqual(self.__class__.mailbox['longitude'], 60)
        self.assertEqual(self.__class__.mailbox['latitude'], 50)
        wia.Location.unsubscribe(device=wia.device_id)
        count = 0
        initial_subscribe_count = wia.Stream.subscribed_count
        while count < self.timeout:
            count += 1
            if wia.Stream.subscribed_count < initial_subscribe_count:
                break
        if wia.Stream.subscribed_count == initial_subscribe_count:
            raise Exception("Unable to unsubscribe")
        wia.Stream.disconnect()
        count = 0
        while count < self.timeout:
            count += 1
            if not wia.Stream.connected:
                break
        if wia.Stream.connected:
            raise Exception("Unable to disconnect")


if __name__ == '__main__':
    unittest2.main()
