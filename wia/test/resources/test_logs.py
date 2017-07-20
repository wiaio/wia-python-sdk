import wia
import unittest2
import time
from datetime import datetime
import os

class LogsTest(unittest2.TestCase):
    timeout = 100000000
    mailbox = {}

    def test_logs_publish_rest(self):
        wia.secret_key = os.environ['device_secret_key']
        result = wia.Log.publish(level='info', message='test1')
        self.assertTrue(result)
        self.assertTrue(result['id'])

    # need to make sure publisher is 'mqtt'
    def test_logs_publish(self):
        wia.secret_key = os.environ['device_secret_key']
        wia.Stream.connect()
        count = 0
        while count < 6:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                print('LOG CONNECTED')
                time.sleep(1)
                break
        if not wia.Stream.connected:
            raise Exception("Unable to connect")
        result = wia.Log.publish(level='info', message='test_mqtt')
        print('PUBLISHED')
        wia.Stream.disconnect()
        count = 0
        while count < 6:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                print('DISCONNECTED')
                break
        if wia.Stream.connected:
            raise Exception("Unable to disconnect")
        wia.secret_key = None

    def test_logs_list(self):
        wia.secret_key = os.environ['org_secret_key']
        list_return = wia.Log.list(device=os.environ['device_id'], limit=10, page=0)
        self.assertTrue(list_return['logs'])
        self.assertTrue(type(list_return['logs']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)
        wia.secret_key = None

    def test_logs_list_order_sort(self):
        wia.secret_key = os.environ['org_secret_key']
        list_return = wia.Log.list(device=os.environ['device_id'], limit=10, page=0, order='timestamp', sort='desc')
        timestamp_list = []
        for log in list_return['logs']:
            timestamp_list.append(log['timestamp'])
        descending = timestamp_list[:]
        descending.sort(reverse=True)
        self.assertEqual(descending, timestamp_list)
        list_return = wia.Log.list(device=os.environ['device_id'], limit=10, page=0, order='timestamp', sort='asc')
        timestamp_list = []
        for log in list_return['logs']:
            timestamp_list.append(log['timestamp'])
        ascending = timestamp_list[:]
        ascending.sort()
        self.assertEqual(ascending, timestamp_list)
        wia.secret_key = None

    def test_logs_subscribe(self):
        self.__class__.mailbox = {}
        def logs_subscription_func(payload):
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

        # subscribe to log
        wia.Log.subscribe(device=os.environ['device_id'], func=logs_subscription_func)
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

        # publish log
        wia.secret_key = os.environ['device_secret_key']

        wia.Stream.connect()
        while count < 6:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                time.sleep(1)
                break
        if not wia.Stream.connected:
            raise Exception("Unable to connect")

        wia.Log.publish(level='info', message='test_subscribe')

        wia.secret_key = os.environ['org_secret_key']
        time.sleep(0.5)

        # unsubscribe from log
        initial_subscribe_count = wia.Stream.subscribed_count
        wia.Log.unsubscribe(device=os.environ['device_id'])
        count = 0
        while count < 6:
            time.sleep(0.5)
            count += 1
            if wia.Stream.subscribed_count < initial_subscribe_count:
                break
        if wia.Stream.subscribed_count == initial_subscribe_count:
            raise Exception("Unable to unsubscribe")
        wia.secret_key = None

if __name__ == '__main__':
    unittest2.main()
