import wia
import unittest2
import time
import os

class LocationsTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        wia.device_secret_key = 'd_sk_738Pyjm998MV7kPMMMr2pSfo'
        wia.user_secret_key = 'u_sk_0kl0z2W45SEs1SWk7Bu0hDxe'
        wia.secret_key = 'u_sk_0kl0z2W45SEs1SWk7Bu0hDxe'
        wia.device_id = 'dev_4sEIfy5QbtIdYO5k'

    def test_locations_publish(self):
        wia.secret_key = wia.device_secret_key
        publish_return = wia.Locations.publish(latitude=53.349805, longitude=-6.260310)
        self.assertTrue(publish_return['id'])

    def test_locations_list(self):
        list_return = wia.Locations.list(device=wia.device_id, limit=10, page=0)
        self.assertTrue(list_return['locations'])
        self.assertTrue(type(list_return['locations']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)

    def test_locations_list_order_sort(self):
        list_return = wia.Locations.list(device=wia.device_id, order='receivedTimestamp', sort='desc')
        # self.assertTrue(list_return['locations'][0]['receivedTimestamp'] >= list_return['locations'][1]['receivedTimestamp'])
        # self.assertTrue(list_return['locations'][2]['receivedTimestamp'] >= list_return['locations'][5]['receivedTimestamp'])
        # list_return = wia.Locations.list(device=wia.device_id, order='receivedTimestamp', sort='asc')
        # self.assertTrue(list_return['locations'][0]['receivedTimestamp'] <= list_return['locations'][1]['receivedTimestamp'])
        # self.assertTrue(list_return['locations'][2]['receivedTimestamp'] <= list_return['locations'][5]['receivedTimestamp'])

if __name__ == '__main__':
    unittest2.main()
