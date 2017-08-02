try:
    import unittest2 as unittest
except ImportError:
    import unittest

import time
import os
import logging

from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class DeviceTest(unittest.TestCase):
    test_id = ''

    def test_public_org_create(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        device = wia.Device.create(name='johnDoe',serialNumber='test', public=True)
        self.__class__.test_id = device.id
        self.assertEqual(device.name, 'johnDoe')
        wia.access_token = None

    def test_user_create(self):
        wia = Wia()
        wia.access_token = os.environ['user_secret_key']
        device = wia.Device.create(name='janeDoe')
        time.sleep(1)
        self.assertEqual(device.name, 'janeDoe')
        id = device.id
        device = wia.Device.retrieve(id)
        self.assertTrue(device.delete(device.id))
        wia.access_token = None

    # retrieves device created in the first function in this page
    def test_retrieve(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        device = wia.Device.retrieve(self.__class__.test_id)
        self.assertEqual(device.name, 'johnDoe')
        self.assertTrue(device.delete(device.id))
        wia.access_token = None

    def test_update(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        test_device = wia.Device.create(name='johnDoe', public=True)
        device = wia.Device.retrieve(test_device.id)
        self.assertEqual(device.name, 'johnDoe')
        device = wia.Device.update(name="janeDoe", id=device.id)
        now_device = wia.Device.retrieve(device.id)
        self.assertEqual(now_device.name, 'janeDoe')
        self.assertTrue(now_device.delete(device.id))
        wia.access_token = None

    def test_delete(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        test_device = wia.Device.create(name='toBeDestroyed', public=True)
        test_device = wia.Device.retrieve(test_device.id)
        self.assertTrue(test_device.delete(test_device.id))
        wia.access_token = None

    def test_device_list(self):
        wia = Wia()
        wia.access_token = os.environ['user_secret_key']
        list_return = wia.Device.list(limit=20, page=0)
        self.assertTrue('devices' in list_return)
        self.assertTrue(type(list_return['devices']) == list)
        self.assertTrue('count' in list_return)
        self.assertTrue(type(list_return['count']) == int)
        wia.access_token = None

    def test_devices_list_order_desc(self):
        wia = Wia()
        wia.access_token = os.environ['user_secret_key']
        result = wia.Device.list(order='createdAt', sort='desc')
        devices_list = []
        #for device in result['devices']:
            #print device.createdAt
        wia.access_token = None

    def test_devices_list_order_asc(self):
        wia = Wia()
        wia.access_token = os.environ['user_secret_key']
        result = wia.Device.list(order='createdAt', sort='asc')
        devices_list = []
        #for device in result['devices']:
            #print device.createdAt
        wia.access_token = None

    def test_device_list_public(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        list_return = wia.Device.list(public=False)
        for device in list_return['devices']:
            self.assertFalse(device.public)
        list_return = wia.Device.list(public=True)
        for device in list_return['devices']:
            self.assertTrue(device.public)
        wia.access_token = None

    # ERROR TESTS
    def test_create_device_not_authorized(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        device = wia.Device.create(name='fail', public=True)
        self.assertIsInstance(device, WiaError)
        wia.access_token = None

    def test_create_device_invalid_params(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        device = wia.Device.create(name='fail', public='Oops')
        self.assertIsInstance(device, WiaError)
        wia.access_token = None

    def test_create_device_wrong_params(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        device = wia.Device.create(name='fail', data=100)
        self.assertIsInstance(device, WiaError)
        wia.access_token = None

    def test_device_delete_unknown(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        device = wia.Device.delete('nonexisting')
        self.assertIsInstance(device, WiaError)
        wia.access_token = None

    def test_device_retrieve_unknown(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        device = wia.Device.retrieve('dev_nonexisting')
        self.assertIsInstance(device, WiaError)
        wia.access_token = None

if __name__ == '__main__':
    unittest2.main()
