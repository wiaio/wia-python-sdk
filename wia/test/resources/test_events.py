import wia
import unittest2
import time
import os

class EventsTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        wia.device_secret_key = 'd_sk_738Pyjm998MV7kPMMMr2pSfo'
        wia.device_id = 'dev_4sEIfy5QbtIdYO5k'


    def test_events_publish(self):
        publish_return = wia.Events.publish(name='test_event', data=130)

    def test_events_list(self):
        list_return = wia.Events.list(device=wia.device_id, limit=10, page=0)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest2.main()
