# try:
#     import unittest2 as unittest
# except ImportError:
#     import unittest
#
# import time
# from datetime import datetime
# import os
# import logging
#
# from wia import Wia
# from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError
#
# class FunctionsTest(unittest.TestCase):
#     function_id = None
#
#     def test_functions_create(self):
#         wia = Wia()
#         wia.access_token = os.environ['device_secret_key']
#         wia.Stream.connect()
#         count = 0
#         while count <= 10:
#             time.sleep(0.5)
#             count += 1
#             if wia.Stream.connected:
#                 time.sleep(1)
#                 break
#         self.assertTrue(wia.Stream.connected)
#         def test_function(argument):
#             print(argument)
#         result = wia.Function.create(name='test_function_create', function=test_function)
#         self.__class__.test_id = result['id']
#         wia.Stream.disconnect()
#         count = 0
#         while count <= 10:
#             time.sleep(0.5)
#             count += 1
#             if not wia.Stream.connected:
#                 break
#         self.assertFalse(wia.Stream.connected)
#         wia.access_token = None
#
#     def test_functions_delete(self):
#         wia = Wia()
#         wia.access_token = os.environ['device_secret_key']
#         result = wia.Function.delete(self.__class__.test_id)
#         self.assertTrue(result)
#         wia.access_token = None
#
#     def test_functions_call(self):
#         wia = Wia()
#         wia.access_token = os.environ['device_secret_key']
#         def test_function_2(payload):
#             print(payload)
#         wia.Stream.connect()
#         count = 0
#         while count <= 10:
#             time.sleep(0.5)
#             count += 1
#             if wia.Stream.connected:
#                 time.sleep(1)
#                 break
#         self.assertTrue(wia.Stream.connected)
#         function_return = wia.Function.create(name='test_function_2', function=test_function_2)
#         wia.access_token = os.environ['user_secret_key']
#         wia.Function.call(device=os.environ['device_id'], func=function_return['id'], data={'arg1': 'Hello World!', 'arg2': 1000})
#         time.sleep(2)
#         wia.Function.call(device=os.environ['device_id'], func=function_return['id'])
#         time.sleep(2)
#         wia.Function.call(device=os.environ['device_id'], func=function_return['id'], data="Hello")
#         time.sleep(2)
#         wia.Function.call(device=os.environ['device_id'], func=function_return['id'], data=99)
#         time.sleep(2)
#         wia.Stream.disconnect()
#         count = 0
#         while count <= 10:
#             time.sleep(0.5)
#             count += 1
#             if not wia.Stream.connected:
#                 break
#         self.assertFalse(wia.Stream.connected)
#         wia.access_token = None
#
#     def test_functions_list(self):
#         wia = Wia()
#         wia.access_token = os.environ['org_secret_key']
#         list_return = wia.Function.list(device=os.environ['device_id'], limit=10, page=0)
#         self.assertTrue(list_return['functions'])
#         self.assertTrue(type(list_return['functions']) == list)
#         self.assertTrue(list_return['count'])
#         self.assertTrue(type(list_return['count']) == int)
#         wia.access_token = None
#
# if __name__ == '__main__':
#     unittest2.main()
