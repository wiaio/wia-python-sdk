import wia
import unittest2
import time
from datetime import datetime
import os

class FunctionsTest(unittest2.TestCase):
    timeout = 100000000
    function_id = None

    def test_functions_create(self):
        temp_sk = wia.secret_key
        wia.secret_key = wia.device_secret_key
        def test_function(argument):
            print(argument)
        function_return = wia.Function.create(name='test_function_create', function=test_function)
        self.__class__.test_id = function_return['id']
        wia.secret_key = temp_sk

    def test_functions_delete(self):
        temp_sk = wia.secret_key
        wia.secret_key = wia.device_secret_key
        delete_return = wia.Function.delete(self.__class__.test_id)
        self.assertTrue(delete_return)
        wia.secret_key = temp_sk

    def test_functions_call(self):
        temp_sk = wia.secret_key
        wia.secret_key = wia.device_secret_key
        def test_function_2(payload):
            print("IN TEST FUNCTION 2")
            print(payload)
        wia.Stream.connect()
        count = 0
        while count < self.timeout:
            count += 1
            if wia.Stream.connected:
                break
        if not wia.Stream.connected:
            raise Exception("Unable to connect")
        function_return = wia.Function.create(name='test_function_2', function=test_function_2)
        wia.secret_key = temp_sk
        wia.Function.call(device=wia.device_id, func=function_return['id'], data={'arg1': 'Hello World!', 'arg2': 1000})
        time.sleep(5)
        wia.Stream.disconnect()
        count = 0
        while count < self.timeout:
            count += 1
            if not wia.Stream.connected:
                break
        if wia.Stream.connected:
            raise Exception("Unable to disconnect")
        wia.Function.call(device=wia.device_id, func=function_return['id'], data='Hello World!')

    def test_functions_list(self):
        list_return = wia.Function.list(device=wia.device_id, limit=10, page=0)
        self.assertTrue(list_return['functions'])
        self.assertTrue(type(list_return['functions']) == list)
        self.assertTrue(list_return['count'])
        self.assertTrue(type(list_return['count']) == int)


if __name__ == '__main__':
    unittest2.main()
