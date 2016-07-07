import wia
import unittest2
import time
from datetime import datetime
import os

class LogsTest(unittest2.TestCase):
    pass

    # def test_logs_publish(self):
    #     wia.secret_key = wia.device_secret_key
    #     publish_return = wia.Logs.publish(level='info', message='test')
    #     self.assertTrue('id')
    #
    # def test_logs_list(self):
    #     list_return = wia.Logs.list(device=wia.device_id, limit=10, page=0)
    #     self.assertTrue(list_return['logs'])
    #     self.assertTrue(type(list_return['logs']) == list)
    #     self.assertTrue(list_return['count'])
    #     self.assertTrue(type(list_return['count']) == int)
    #
    # def test_logs_list_order_sort(self):
    #     list_return = wia.Logs.list(device=wia.device_id, order='receivedTimestamp', sort='desc')
    #     timestamp_list = []
    #     for log in list_return['logs']:
    #         timestamp_list.append(log['receivedTimestamp'])
    #     descending = timestamp_list[:]
    #     descending.sort(reverse=True)
    #     self.assertEqual(descending, timestamp_list)
    #     timestamp_list = []
    #     list_return = wia.Logs.list(device=wia.device_id, order='receivedTimestamp', sort='asc')
    #     for log in list_return['logs']:
    #         timestamp_list.append(log['receivedTimestamp'])
    #     ascending = timestamp_list[:]
    #     ascending.sort()
    #     self.assertEqual(ascending, timestamp_list)


if __name__ == '__main__':
    unittest2.main()
