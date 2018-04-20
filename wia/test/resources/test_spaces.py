try:
    import unittest2 as unittest
except ImportError:
    import unittest

import logging
import time
import os
import datetime
import random
from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class SpacesTest(unittest.TestCase):
    def test_spaces_create_and_retrieve(self):
        wia = Wia()
        wia.access_token_create(username=os.environ['WIA_TEST_USERNAME'],
                                               password=os.environ['WIA_TEST_PASSWORD'])
        random_name = str(datetime.date.today()) + str(random.getrandbits(128))
        space = wia.Space.create(name=random_name)
        self.assertTrue(space.name == random_name)
        space_retrieve = wia.Space.retrieve(space.id)
        self.assertTrue(space.name == space_retrieve.name)


    def test_spaces_list(self):
        wia = Wia()
        spaces = wia.Space.list()
        self.assertTrue(spaces['count'] > 0)

    def test_spaces_create_retrieve_update_list_delete_device(self):
        wia = Wia()
        spaces = wia.Space.list()
        testSpace = spaces['spaces'][0]

        testDevice = wia.Device.create(**{"name": "testDevice", "space.id": testSpace.id})
        self.assertIsInstance(testDevice, type(Wia().Device))

        retrieveDevice = wia.Device.retrieve(testDevice.id)
        self.assertTrue(retrieveDevice.name == "testDevice")

        deviceUpdated = wia.Device.update(id=retrieveDevice.id, name="testDeviceUpdated")
        self.assertTrue(deviceUpdated.name == "testDeviceUpdated")
        list_return = wia.Device.list(**{"space.id": testSpace.id})
        self.assertTrue('devices' in list_return)
        self.assertTrue(type(list_return['devices']) == list)
        self.assertTrue('count' in list_return)
        self.assertTrue(wia.Device.delete(deviceUpdated.id))


    def test_spaces_devices_list_order_desc(self):
         wia = Wia()
         spaces = wia.Space.list()
         testSpace = spaces['spaces'][0]
         list_return_desc = wia.Device.list(**{"space.id": testSpace.id, "order": "createdAt", "sort" : "desc"})
         self.assertTrue('devices' in list_return_desc)
         self.assertTrue(type(list_return_desc['devices']) == list)
         self.assertTrue('count' in list_return_desc)


    def test_spaces_devices_list_order_asc(self):
        wia = Wia()
        spaces = wia.Space.list()
        testSpace = spaces['spaces'][0]
        list_return_asc = wia.Device.list(**{"space.id": testSpace.id, "order": "createdAt", "sort": "asc"})
        self.assertTrue('devices' in list_return_asc)
        self.assertTrue(type(list_return_asc['devices']) == list)
        self.assertTrue('count' in list_return_asc)

    # # ERROR TESTS
    def test_create_device_not_authorized(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        device = wia.Device.create(name='fail', public=True)
        self.assertIsInstance(device, WiaError)
        wia.access_token = None

    def test_create_device_invalid_params(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        device = wia.Device.create(name='fail', public='Oops')
        self.assertIsInstance(device, WiaError)
        wia.access_token = None

    def test_create_device_wrong_params(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        device = wia.Device.create(name='fail', data=100)
        self.assertIsInstance(device, WiaError)
        wia.access_token = None

    def test_device_delete_unknown(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        device = wia.Device.delete('nonexisting')
        self.assertIsInstance(device, WiaError)
        wia.access_token = None

    def test_device_retrieve_unknown(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        device = wia.Device.retrieve('dev_nonexisting')
        self.assertIsInstance(device, WiaError)
        wia.access_token = None


if __name__ == '__main__':
    unittest.main()
