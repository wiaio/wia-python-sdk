try:
    import unittest2 as unittest
except ImportError:
    import unittest

import time
from datetime import datetime
import os
import logging

from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class LogsTest(unittest.TestCase):
    def test_logs_publish_rest(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        result = wia.Log.publish(level='info', message='test1')
        self.assertTrue(result is not None)
        wia.access_token = None

    def test_logs_publish(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        wia.Stream.connect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                time.sleep(1)
                break
        self.assertTrue(wia.Stream.connected)
        result = wia.Log.publish(level='info', message='test_mqtt')
        self.assertTrue(result is not None)
        wia.Stream.disconnect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        self.assertFalse(wia.Stream.connected)
        wia.access_token = None

    def test_logs_list(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Log.list(device=os.environ['device_id'], limit=10, page=0)
        self.assertTrue('logs' in result)
        self.assertTrue(type(result['logs']) == list)
        self.assertTrue('count' in result)
        self.assertTrue(type(result['count']) == int)
        wia.secret_key = None

    def test_logs_list_order_desc(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Log.list(device=os.environ['device_id'], limit=10, page=0, order='timestamp', sort='desc')
        logs_list = []
        #for log in result['logs']:
            #print log.timestamp
        wia.access_token = None

    def test_logs_list_order_asc(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Log.list(device=os.environ['device_id'], limit=10, page=0, order='timestamp', sort='asc')
        logs_list = []
        #for log in result['logs']:
            #print log.timestamp
        wia.access_token = None

    def test_logs_subscribe(self):
        wia = Wia()
        def logs_subscription_func(payload):
            pass
        wia.access_token = os.environ['org_secret_key']
        wia.Stream.connect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                time.sleep(1)
                break
        self.assertTrue(wia.Stream.connected)

        # subscribe to log
        wia.Log.subscribe(device=os.environ['device_id'], func=logs_subscription_func)
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.subscribed:
                time.sleep(1)
                break
        self.assertTrue(wia.Stream.subscribed)

        wia.Stream.disconnect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        self.assertFalse(wia.Stream.connected)

        # publish log
        wia.access_token = os.environ['device_secret_key']

        wia.Stream.connect()
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                time.sleep(1)
                break
        self.assertTrue(wia.Stream.connected)

        wia.Log.publish(level='info', message='test_subscribe')

        wia.access_token = os.environ['org_secret_key']
        time.sleep(0.5)

        # unsubscribe from log
        initial_subscribe_count = wia.Stream.subscribed_count
        wia.Log.unsubscribe(device=os.environ['device_id'])
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.subscribed_count < initial_subscribe_count:
                break
        self.assertTrue(wia.Stream.subscribed_count < initial_subscribe_count)

        wia.Stream.disconnect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        self.assertFalse(wia.Stream.connected)

        wia.access_token = None

    # ERROR TESTS
    def test_publish_log_not_authorized(self):
        wia = Wia()
        wia.Stream.disconnect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if not wia.Stream.connected:
                break
        self.assertFalse(wia.Stream.connected)
        wia.access_token = os.environ['org_secret_key']
        log = wia.Log.publish(level='fail', message='error')
        self.assertIsInstance(log, WiaError)
        wia.access_token = None

    def test_publish_log_wrong_params(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        log = wia.Log.publish(name='fail')
        self.assertIsInstance(log, WiaError)
        wia.access_token = None

    def test_list_log_not_found(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        result = wia.Log.list(device='Unknown')
        self.assertIsInstance(result, WiaError)
        wia.access_token = None

if __name__ == '__main__':
    unittest2.main()
