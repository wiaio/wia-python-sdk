import wia
import unittest2
import time
import os
from wia.util import logger

class EventsTest(unittest2.TestCase):
    timeout = 100000000
    mailbox = {}

    def test_events_publish(self):
        temp_sk = wia.secret_key
        wia.secret_key = wia.device_secret_key
        wia.Stream.connect()
        count = 0
        while count < self.timeout:
            count += 1
            if wia.Stream.connected:
                break
        if not wia.Stream.connected:
            raise Exception("Unable to connect")
        publish_return = wia.Event.publish(name='test_event_other', data=130)
        self.assertTrue(publish_return['id'])
        wia.Stream.disconnect()
        count = 0
        while count < self.timeout:
            count += 1
            if not wia.Stream.connected:
                break
        if wia.Stream.connected:
            raise Exception("Unable to disconnect")
        wia.secret_key = temp_sk

    def test_events_list(self):
        list_return = wia.Event.list(device=wia.device_id, limit=10, page=0)
        self.__class__.event_count = list_return['count']
        self.assertTrue(list_return['events'])
        self.assertTrue(type(list_return['events']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)

    def test_events_list_order_sort(self):
        list_return = wia.Event.list(device=wia.device_id, limit=10, page=0, order='timestamp', sort='desc')
        timestamp_list = []
        for event in list_return['events']:
            timestamp_list.append(event['timestamp'])
        descending = timestamp_list[:]
        descending.sort(reverse=True)
        self.assertEqual(descending, timestamp_list)
        list_return = wia.Event.list(device=wia.device_id, limit=10, page=0, order='timestamp', sort='asc')
        timestamp_list = []
        for event in list_return['events']:
            timestamp_list.append(event['timestamp'])
        ascending = timestamp_list[:]
        ascending.sort()
        self.assertEqual(ascending, timestamp_list)

    def test_events_list_name(self):
        list_return = wia.Event.list(device = wia.device_id, name='test_event')
        for event in list_return['events']:
            self.assertEqual('test_event', event['name'])

    def test_events_list_since_until(self):
        hour_ago = int((time.time())*1000 - 3600000)
        list_return = wia.Event.list(device=wia.device_id, order='timestamp', sort='desc', since=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.event_count)
        list_return = {}
        list_return = wia.Event.list(device=wia.device_id, order='timestamp', sort='desc', until=hour_ago)
        self.assertTrue(list_return['count'] <= self.__class__.event_count)

    def test_events_subscribe(self):
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
        wia.Event.subscribe(device=wia.device_id, func=wildcard_function)
        wia.Event.subscribe(device=wia.device_id, func=specific_function, name='subscribe_test_event')
        count = 0
        while count < self.timeout:
            count += 1
            if wia.Stream.subscribed:
                break
        if not wia.Stream.subscribed:
            raise Exception("Unable to subscribe")
        temp_sk = wia.secret_key
        wia.secret_key = wia.device_secret_key
        wia.Event.publish(name='subscribe_test_event', data=99)
        wia.secret_key = temp_sk
        time.sleep(5)
        self.assertEqual(self.__class__.mailbox['name'], 'subscribe_test_event')
        self.assertEqual(self.__class__.mailbox['data'], 99)
        wia.Event.unsubscribe(device=wia.device_id, name='subscribe_test_event')
        wia.Event.unsubscribe(device=wia.device_id)
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