import wia
import unittest2
import time
import os

class LocationsTest(unittest2.TestCase):
    mailbox = {}

    def test_locations_publish(self):
        temp_sk = wia.secret_key
        wia.secret_key = wia.device_secret_key
        wia.Stream.connect()
        time.sleep(1)
        publish_return = wia.Locations.publish(latitude=50, longitude=60)
        self.assertTrue(publish_return['id'])
        wia.Stream.disconnect()
        while wia.Stream.connected:
            pass
        wia.secret_key = temp_sk

    def test_locations_list(self):
        list_return = wia.Locations.list(device=wia.device_id, limit=10, page=0)
        self.__class__.locations_count = list_return['count']
        self.assertTrue(list_return['locations'])
        self.assertTrue(type(list_return['locations']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)

    def test_locations_list_order_sort(self):
        list_return = wia.Locations.list(device=wia.device_id, limit=10, page=0, order='timestamp', sort='desc')
        timestamp_list = []
        for location in list_return['locations']:
            timestamp_list.append(location['timestamp'])
        descending = timestamp_list[:]
        descending.sort(reverse=True)
        self.assertEqual(descending, timestamp_list)
        list_return = wia.Locations.list(device=wia.device_id, order='timestamp', sort='asc')
        timestamp_list = []
        for location in list_return['locations']:
            timestamp_list.append(location['timestamp'])
        ascending = timestamp_list[:]
        ascending.sort()
        self.assertEqual(ascending, timestamp_list)

    def test_locations_list_since_until(self):
        hour_ago = int((time.time())*1000 - 3600000)
        list_return = wia.Locations.list(device=wia.device_id, order='timestamp', sort='desc', since=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.locations_count)
        list_return = {}
        list_return = wia.Locations.list(device=wia.device_id, order='timestamp', sort='desc', until=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.locations_count)

    def test_locations_subscribe(self):
        self.__class__.mailbox = {}
        def location_subscription_func(payload):
            self.__class__.mailbox = payload
        wia.Stream.connect()
        while wia.Stream.connected == False:
            pass
        wia.Locations.subscribe(device='dev_4sEIfy5QbtIdYO5k', func=location_subscription_func)
        time.sleep(1)
        while wia.Stream.subscribed is not True:
            pass
        wia.Locations.publish(longitude=60, latitude=50)
        time.sleep(1)
        self.assertEqual(self.__class__.mailbox['longitude'], 60)
        self.assertEqual(self.__class__.mailbox['latitude'], 50)
        wia.Locations.unsubscribe(device='dev_4sEIfy5QbtIdYO5k')
        while wia.Stream.subscribed:
            pass
        self.assertEqual(wia.Stream.subscribed, False)



if __name__ == '__main__':
    unittest2.main()
