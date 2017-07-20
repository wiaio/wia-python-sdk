import wia
import unittest2
import time
import os

class LocationsTest(unittest2.TestCase):
    timeout = 100000000
    mailbox = {}

    def test_locations_publish(self):
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
            raise Exception("unable to connect")
        publish_return = wia.Location.publish(latitude=50, longitude=60)
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

    def test_locations_list(self):
        wia.secret_key = os.environ['org_secret_key']
        list_return = wia.Location.list(device=os.environ['device_id'], limit=10, page=0)
        self.__class__.locations_count = list_return['count']
        self.assertTrue(list_return['locations'])
        self.assertTrue(type(list_return['locations']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)
        wia.secret_key = None

    def test_locations_list_order_sort(self):
        wia.secret_key = os.environ['org_secret_key']
        list_return = wia.Location.list(device=os.environ['device_id'], limit=10, page=0, order='timestamp', sort='desc')
        timestamp_list = []
        for location in list_return['locations']:
            timestamp_list.append(location['timestamp'])
        descending = timestamp_list[:]
        descending.sort(reverse=True)
        self.assertEqual(descending, timestamp_list)
        list_return = wia.Location.list(device=os.environ['device_id'], order='timestamp', sort='asc')
        timestamp_list = []
        for location in list_return['locations']:
            timestamp_list.append(location['timestamp'])
        ascending = timestamp_list[:]
        ascending.sort()
        self.assertEqual(ascending, timestamp_list)
        wia.secret_key = None

    def test_locations_list_since_until(self):
        wia.secret_key = os.environ['org_secret_key']
        hour_ago = int((time.time())*1000 - 3600000)
        list_return = wia.Location.list(device=os.environ['device_id'], order='timestamp', sort='desc', since=hour_ago)
        self.assertTrue(type(list_return['count']) == int)
        list_return = {}
        list_return = wia.Location.list(device=os.environ['device_id'], order='timestamp', sort='desc', until=hour_ago)
        self.assertTrue(type(list_return['count']) == int)
        wia.secret_key = None

    def test_locations_subscribe(self):
        self.__class__.mailbox = {}
        def location_function(payload):
            self.__class__.mailbox = payload
        wia.secret_key = os.environ['org_secret_key']
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

        # subscribe to location
        wia.Location.subscribe(device=os.environ['device_id'], func=location_function)
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

        # publish location
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

        wia.Location.publish(longitude=60, latitude=50)

        wia.secret_key = os.environ['org_secret_key']
        time.sleep(5)

        # unsubscribe from location
        initial_subscribe_count = wia.Stream.subscribed_count
        print('initial sub', initial_subscribe_count)
        wia.Location.unsubscribe(device=os.environ['device_id'])
        count = 0
        while count < 6:
            time.sleep(0.5)
            count += 1
            if wia.Stream.subscribed_count < initial_subscribe_count:
                break
        print('now sub', wia.Stream.subscribed_count)
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
