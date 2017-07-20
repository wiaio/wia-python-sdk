import wia
import unittest2
import time
import os
from wia.util import logger

class EventsTest(unittest2.TestCase):
    timeout = 100000000
    mailbox = {}

    def test_events_publish_rest(self):
        wia.secret_key = os.environ['device_secret_key']
        publish_return = wia.Event.publish(name='test_event_other_rest', data=130)
        self.assertTrue(publish_return['id'])
        wia.secret_key = None

    def test_events_publish(self):
        wia.secret_key = os.environ['device_secret_key']
        wia.Stream.connect()
        count = 0
        while count < 5:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                time.sleep(1)
                break
        if not wia.Stream.connected:
            raise Exception("Unable to connect")
        publish_return = wia.Event.publish(name='test_event_mqtt', data=130)
        self.assertTrue(publish_return is not None)
        wia.Stream.disconnect()
        count = 0
        while count < 5:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        if wia.Stream.connected:
            raise Exception("Unable to disconnect")
        wia.secret_key = None

    def test_events_publish_file(self):
        wia.secret_key = os.environ['device_secret_key']
        publish_return = wia.Event.publish(name='test_event_other_filesud', data=1300, file=open('image.jpg', 'rb'))
        wia.secret_key = None

    def test_device_org_retrieve(self):
        wia.secret_key = os.environ['device_secret_key']
        wia.Stream.connect()
        time.sleep(2)
        publish = wia.Event.publish(name='device_org_test_event', data=99)
        wia.secret_key = os.environ['org_secret_key']
        response = wia.Device.retrieve(os.environ['device_id'])
        self.assertEqual(response.events['device_org_test_event']['name'], 'device_org_test_event')
        wia.secret_key = None

    def test_events_list(self):
        wia.secret_key = os.environ['org_secret_key']
        list_return = wia.Event.list(device=os.environ['device_id'], limit=10, page=0)
        self.__class__.event_count = list_return['count']
        self.assertTrue(list_return['events'])
        self.assertTrue(type(list_return['events']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)
        wia.secret_key = None

    def test_events_list_order_sort(self):
        #Descending timestamp
        wia.secret_key = os.environ['org_secret_key']
        list_return = wia.Event.list(device=os.environ['device_id'], limit=10, page=0, order='timestamp', sort='desc')
        timestamp_list = []
        for event in list_return['events']:
            timestamp_list.append(event['timestamp'])
        descending = timestamp_list[:]
        #print('LIST', timestamp_list)
        descending.sort(reverse=True)
        self.assertEqual(descending, timestamp_list)
        #ascending timestamp
        list_return = wia.Event.list(device=os.environ['device_id'], limit=10, page=0, order='timestamp', sort='asc')
        timestamp_list = []
        for event in list_return['events']:
            timestamp_list.append(event['timestamp'])
        ascending = timestamp_list[:]
        #print('LIST ASC', timestamp_list)
        ascending.sort()
        self.assertEqual(ascending, timestamp_list)
        wia.secret_key = None

    def test_events_list_name(self):
        wia.secret_key = os.environ['org_secret_key']
        list_return = wia.Event.list(device = os.environ['device_id'], name='test_event')
        for event in list_return['events']:
            self.assertEqual('test_event', event['name'])
        wia.secret_key = None

    def test_events_list_since_until(self):
        wia.secret_key = os.environ['org_secret_key']
        hour_ago = int((time.time())*1000 - 3600000)
        list_return = wia.Event.list(device=os.environ['device_id'], order='timestamp', sort='desc', since=hour_ago)
        self.assertTrue(type(list_return['count']) == int)
        list_return = {}
        list_return = wia.Event.list(device=os.environ['device_id'], order='timestamp', sort='desc', until=hour_ago)
        self.assertTrue(type(list_return['count']) == int)
        wia.secret_key = None

    def test_events_subscribe(self):
        self.__class__.mailbox = {}
        def wildcard_function(payload):
            pass
        def specific_function(payload):
            self.__class__.mailbox = payload
        wia.secret_key = os.environ['org_secret_key']
        wia.Stream.connect()
        count = 0
        # waits for Stream to be connected
        while count < 5:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                time.sleep(1)
                break
        if not wia.Stream.connected:
            raise Exception("Unable to connect")

        # subscirbe to event
        wia.Event.subscribe(device=os.environ['device_id'], func=wildcard_function)
        wia.Event.subscribe(device=os.environ['device_id'], name='subscribe_test_event', func=specific_function)
        count = 0
        while count < 5:
            time.sleep(0.5)
            count += 1
            if wia.Stream.subscribed:
                time.sleep(1)
                break
        if not wia.Stream.subscribed:
            raise Exception("Unable to subscribe")

        wia.Stream.disconnect()
        count = 0
        while count < 5:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        if wia.Stream.connected:
            raise Exception('Unable to disconnect')

        # publish event data
        wia.secret_key = os.environ['device_secret_key']

        wia.Stream.connect()
        count = 0
        while count < 5:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                break
        if not wia.Stream.connected:
            raise Exception('Unable to connect')

        wia.Event.publish(name='subscribe_test_event', data=97)

        wia.secret_key = os.environ['org_secret_key']
        time.sleep(0.5)

        count = 0
        initial_subscribe_count = wia.Stream.subscribed_count
        print(initial_subscribe_count)

        # unsubscribe from event
        wia.Event.unsubscribe(device=os.environ['device_id'])
        wia.Event.unsubscribe(device=os.environ['device_id'], name='subscribe_test_event')
        while count < 5:
            time.sleep(0.5)
            count += 1
            if wia.Stream.subscribed_count < initial_subscribe_count:
                break
        if wia.Stream.subscribed_count == initial_subscribe_count:
            print(wia.Stream.subscribed_count)
            raise Exception("Unable to unsubscribe")
        wia.Stream.disconnect()
        count = 0
        while count < 5:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        if wia.Stream.connected:
            raise Exception("Unable to disconnect")
        wia.secret_key = None

if __name__ == '__main__':
    unittest2.main()
