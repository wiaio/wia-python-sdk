import wia
import unittest2
import time
import os
from wia.util import logger

class EventsTest(unittest2.TestCase):
    mailbox = {}

    def test_events_publish(self):
        temp_sk = wia.secret_key
        wia.secret_key = wia.device_secret_key
        wia.Stream.connect()
        publish_return = wia.Events.publish(name='test_event_other', data=130)
        self.assertTrue(publish_return['id'])
        wia.Stream.disconnect()
        while wia.Stream.connected:
            pass
        wia.secret_key = temp_sk

    def test_events_list(self):
        list_return = wia.Events.list(device=wia.device_id, limit=10, page=0)
        self.__class__.event_count = list_return['count']
        self.assertTrue(list_return['events'])
        self.assertTrue(type(list_return['events']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)

    def test_events_list_order_sort(self):
        list_return = wia.Events.list(device=wia.device_id, limit=10, page=0, order='timestamp', sort='desc')
        timestamp_list = []
        for event in list_return['events']:
            timestamp_list.append(event['timestamp'])
        descending = timestamp_list[:]
        descending.sort(reverse=True)
        self.assertEqual(descending, timestamp_list)
        list_return = wia.Events.list(device=wia.device_id, limit=10, page=0, order='timestamp', sort='asc')
        timestamp_list = []
        for event in list_return['events']:
            timestamp_list.append(event['timestamp'])
        ascending = timestamp_list[:]
        ascending.sort()
        self.assertEqual(ascending, timestamp_list)

    def test_events_list_name(self):
        list_return = wia.Events.list(device = wia.device_id, name='test_event')
        for event in list_return['events']:
            self.assertEqual('test_event', event['name'])

    def test_events_list_since_until(self):
        hour_ago = int((time.time())*1000 - 3600000)
        list_return = wia.Events.list(device=wia.device_id, order='timestamp', sort='desc', since=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.event_count)
        list_return = {}
        list_return = wia.Events.list(device=wia.device_id, order='timestamp', sort='desc', until=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.event_count)

    def test_events_subscribe(self):
        self.__class__.mailbox = {}
        def wildcard_function(payload):
            pass
        def specific_function(payload):
            self.__class__.mailbox = payload
        wia.Stream.connect()
        while wia.Stream.connected == False:
            pass
        wia.Events.subscribe(device='dev_4sEIfy5QbtIdYO5k', func=wildcard_function)
        wia.Events.subscribe(device='dev_4sEIfy5QbtIdYO5k', func=specific_function, name='subscribe_test_event')
        while wia.Stream.subscribed is not True:
            pass
        wia.Events.publish(name='subscribe_test_event', data=99)
        time.sleep(5)
        self.assertEqual(self.__class__.mailbox['name'], 'subscribe_test_event')
        self.assertEqual(self.__class__.mailbox['data'], 99)
        wia.Events.unsubscribe(device='dev_4sEIfy5QbtIdYO5k', name='subscribe_test_event')
        wia.Events.unsubscribe(device='dev_4sEIfy5QbtIdYO5k')
        while wia.Stream.subscribed:
            pass
        self.assertEqual(wia.Stream.subscribed, False)
        wia.Stream.disconnect()
        while wia.Stream.connected:
            pass



if __name__ == '__main__':
    unittest2.main()
