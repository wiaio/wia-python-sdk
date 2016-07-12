import wia
import unittest2
import time
from datetime import datetime
import os

class LogsTest(unittest2.TestCase):
    pass
    mailbox = {}

    # def test_logs_publish(self):
    #     temp_sk = wia.secret_key
    #     wia.secret_key = wia.device_secret_key
    #     wia.Stream.connect()
    #     time.sleep(1)
    #     publish_return = wia.Logs.publish(level='info', message='test')
    #     self.assertTrue(publish_return['id'])
    #     wia.Stream.disconnect()
    #     while wia.Stream.connected:
    #         pass
    #     wia.secret_key = temp_sk
    #
    # def test_logs_list(self):
    #     list_return = wia.Logs.list(device=wia.device_id, limit=10, page=0)
    #     self.assertTrue(list_return['logs'])
    #     self.assertTrue(type(list_return['logs']) == list)
    #     self.assertTrue(list_return['count'])
    #     self.assertTrue(type(list_return['count']) == int)
    #
    # def test_logs_list_order_sort(self):
    #     list_return = wia.Logs.list(device=wia.device_id, order='timestamp', sort='desc')
    #     timestamp_list = []
    #     for log in list_return['logs']:
    #         timestamp_list.append(log['timestamp'])
    #     descending = timestamp_list[:]
    #     descending.sort(reverse=True)
    #     self.assertEqual(descending, timestamp_list)
    #     timestamp_list = []
    #     list_return = wia.Logs.list(device=wia.device_id, order='timestamp', sort='asc')
    #     for log in list_return['logs']:
    #         timestamp_list.append(log['timestamp'])
    #     ascending = timestamp_list[:]
    #     ascending.sort()
    #     self.assertEqual(ascending, timestamp_list)
    #
    # def test_logs_subscribe(self):
    #     self.__class__.mailbox = {}
    #     def logs_subscription_func(payload):
    #         self.__class__.mailbox = payload
    #     wia.Stream.connect()
    #     while wia.Stream.connected == False:
    #         pass
    #     wia.Logs.subscribe(device='dev_4sEIfy5QbtIdYO5k', func=logs_subscription_func)
    #     time.sleep(1)
    #     while wia.Stream.subscribed is not True:
    #         pass
    #     wia.Logs.publish(level='info', message='test')
    #     time.sleep(1)
    #     self.assertEqual(self.__class__.mailbox['message'], 'test')
    #     self.assertEqual(self.__class__.mailbox['level'], 'info')
    #     wia.Logs.unsubscribe(device='dev_4sEIfy5QbtIdYO5k')
    #     while wia.Stream.subscribed:
    #         pass
    #     self.assertEqual(wia.Stream.subscribed, False)


if __name__ == '__main__':
    unittest2.main()
