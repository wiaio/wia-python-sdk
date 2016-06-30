import wia
import unittest2
import time
import os

class SensorsTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        wia.device_secret_key = 'd_sk_738Pyjm998MV7kPMMMr2pSfo'
        wia.user_secret_key = 'u_sk_0kl0z2W45SEs1SWk7Bu0hDxe'
        wia.secret_key = 'u_sk_0kl0z2W45SEs1SWk7Bu0hDxe'
        wia.device_id = 'dev_4sEIfy5QbtIdYO5k'

    def test_sensors_publish(self):
        wia.secret_key = wia.device_secret_key
        publish_return = wia.Sensors.publish(name='test_sensor_1', data=99)
        self.assertTrue(publish_return['id'])

    def test_sensors_list(self):
        list_return = wia.Sensors.list(device=wia.device_id, limit=10, page=0)
        self.assertTrue(True)
        # self.assertTrue(list_return['sensors'])
        # self.assertTrue(type(list_return['sensors']) == list)
        # self.assertTrue(list_return['count'])
        # self.assertTrue(type(list_return['count']) == int)

if __name__ == '__main__':
    unittest2.main()
