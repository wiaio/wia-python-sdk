import wia
import unittest2
import time
import os

class SensorsTest(unittest2.TestCase):
    pass
    #     wia.secret_key = wia.device_secret_key
    #     publish_return = wia.Sensors.publish(name='test_sensor_1', data=99)
    #     self.assertTrue(publish_return['id'])
    #
    # def test_sensors_list(self):
    #     list_return = wia.Sensors.list(device=wia.device_id, limit=10, page=0)
    #     self.assertTrue(True)
    #     self.assertTrue(list_return['sensors'])
    #     self.assertTrue(type(list_return['sensors']) == list)
    #     self.assertTrue(list_return['count'])
    #     self.assertTrue(type(list_return['count']) == int)

if __name__ == '__main__':
    unittest2.main()
