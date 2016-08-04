import wia
import unittest2
import time
import os

class DeviceTest(unittest2.TestCase):
    test_id = ''

    def test_public_org_create(self):
        wia.secret_key = os.environ['org_secret_key']
        device = wia.Device.create(name='johnDoe',serialNumber='test', public=True)
        self.__class__.test_id = device['id']
        self.assertEqual(device['name'], 'johnDoe')
        wia.secret_key = None

    def test_user_create(self):
        wia.secret_key = os.environ['user_secret_key']
        device = wia.Device.create(name='janeDoe')
        self.assertEqual(device['name'], 'janeDoe')
        wia.secret_key = None

    def test_retrieve(self):
        wia.secret_key = os.environ['org_secret_key']
        device = wia.Device.retrieve(self.__class__.test_id)
        self.assertEqual(device.name, 'johnDoe')
        self.assertTrue(device.delete())
        wia.secret_key = None

    def test_update(self):
        wia.secret_key = os.environ['org_secret_key']
        test_device = wia.Device.create(name='johnDoe', public=True)
        device = wia.Device.retrieve(test_device['id'])
        self.assertEqual(device.name, 'johnDoe')
        device.name = 'janeDoe'
        device.save()
        now_device = wia.Device.retrieve(device.id)
        self.assertEqual(now_device.name, 'janeDoe')
        self.assertTrue(now_device.delete())
        wia.secret_key = None
        # self.assertEqual(test_device['name'], 'johnDoe')
        # test_device['name'] = 'janeDoe'
        # self.assertEqual(test_device['name'], 'janeDoe')
        # wia.Device.update(test_device['id'], name=test_device['name'])
        # self.assertEqual(wia.Device.retrieve(test_device['id']).name, 'janeDoe')
        # wia.Device.delete(test_device['id'])

    def test_delete(self):
        wia.secret_key = os.environ['org_secret_key']
        test_device = wia.Device.create(name='toBeDestroyed', public=True)
        test_device = wia.Device.retrieve(test_device['id'])
        self.assertTrue(test_device.delete())
        wia.secret_key = None

    def test_device_list(self):
        wia.secret_key = os.environ['user_secret_key']
        list_return = wia.Device.list(limit=20, page=0)
        self.assertTrue(list_return['devices'])
        self.assertTrue(type(list_return['devices']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)
        wia.secret_key = None
        # self.assertTrue(len(list_return['devices']) == 20)

    def test_device_list_order_sort(self):
        wia.secret_key = os.environ['user_secret_key']
        list_return = wia.Device.list(order='createdAt', sort='desc')
        timestamp_list = []
        for device in list_return['devices']:
            timestamp_list.append(device['createdAt'])
        descending = timestamp_list[:]
        descending.sort(reverse=True)
        self.assertTrue(descending == timestamp_list)
        list_return = wia.Device.list(order='createdAt', sort= 'asc')
        timestamp_list = []
        for device in list_return['devices']:
            timestamp_list.append(device['createdAt'])
        ascending = timestamp_list[:]
        ascending.sort()
        self.assertTrue(ascending == timestamp_list)
        wia.secret_key = None

    # def test_device_list_public(self):
    #     temp_sk = wia.secret_key
    #     wia.secret_key = 'o_sk_lG4H1RhhlpwXRNbk07lM28JJ'
    #     list_return = wia.Device.list(public=False)
    #     for device in list_return['devices']:
    #         self.assertFalse(device['public'])
    #     list_return = wia.Device.list(public=True)
    #     print(list_return)
    #     for device in list_return['devices']:
    #         print(device['public'])
    #         # self.assertTrue(device['public'])
    #     wia.secret_key = temp_sk


if __name__ == '__main__':
    unittest2.main()
