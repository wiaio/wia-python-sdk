import wia
import unittest2
import time
from datetime import datetime
import os

class LogsTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        wia.device_secret_key = 'd_sk_738Pyjm998MV7kPMMMr2pSfo'
        wia.user_secret_key = 'u_sk_0kl0z2W45SEs1SWk7Bu0hDxe'
        wia.secret_key = wia.user_secret_key
        wia.device_id = 'dev_4sEIfy5QbtIdYO5k'

    def test_logs_publish(self):
        wia.secret_key = wia.device_secret_key
        publish_return = wia.Logs.publish(level='info', message='test')
        self.assertTrue('id')

    def test_logs_list(self):
        list_return = wia.Logs.list(device=wia.device_id, limit=10, page=0)
        self.assertTrue(list_return['logs'])
        self.assertTrue(type(list_return['logs']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)

if __name__ == '__main__':
    unittest2.main()
