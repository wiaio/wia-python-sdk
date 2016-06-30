import wia
import unittest2
import time
import os

class DeviceTest(unittest2.TestCase):
    test_id = ''

    @classmethod
    def setUpClass(cls):
        wia.secret_key = 'u_sk_0kl0z2W45SEs1SWk7Bu0hDxe'

    def test_create(self):
        name = 'johnDoe'
        device = wia.Device.create(name=name,serialNumber='test')
        self.__class__.test_id = device['id']
        self.assertEqual(device['name'], 'johnDoe')

    def test_retrieve(self):
        self.assertEqual(wia.Device.retrieve(self.__class__.test_id).name, 'johnDoe')
        wia.Device.delete(self.__class__.test_id)

    def test_update(self):
        test_device = wia.Device.create(name='johnDoe')
        self.assertEqual(test_device['name'], 'johnDoe')
        test_device['name'] = 'janeDoe'
        self.assertEqual(test_device['name'], 'janeDoe')
        wia.Device.update(test_device['id'], name=test_device['name'])
        self.assertEqual(wia.Device.retrieve(test_device['id']).name, 'janeDoe')
        wia.Device.delete(test_device['id'])

    def test_delete(self):
        test_device = wia.Device.create(name='toBeDestroyed')
        self.assertEqual(wia.Device.delete(test_device['id']), True)

    def test_device_list(self):
        list_return = wia.Device.list(limit=20, page=0)
        self.assertTrue(list_return['devices'])
        self.assertTrue(type(list_return['devices']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)
        self.assertTrue(len(list_return['devices']) == 20)

    def test_device_list_order_sort(self):
        list_return = wia.Device.list(order='createdAt', sort='desc')
        self.assertTrue(list_return['devices'][0]['createdAt'] >= list_return['devices'][1]['createdAt'])
        self.assertTrue(list_return['devices'][2]['createdAt'] >= list_return['devices'][5]['createdAt'])
        list_return = wia.Device.list(order='createdAt', sort= 'asc')
        self.assertTrue(list_return['devices'][0]['createdAt'] <= list_return['devices'][1]['createdAt'])
        self.assertTrue(list_return['devices'][2]['createdAt'] <= list_return['devices'][5]['createdAt'])


if __name__ == '__main__':
    unittest2.main()
