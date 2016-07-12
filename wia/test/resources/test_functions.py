import wia
import unittest2
import time
from datetime import datetime
import os

class FunctionsTest(unittest2.TestCase):
    pass
    function_id = None

    # def test_functions_create(self):
    #     temp_sk = wia.secret_key
    #     wia.secret_key = wia.device_secret_key
    #     def test_function(argument):
    #         print(argument)
    #     function_return = wia.Functions.create(name='test_function', function=test_function)
    #     self.__class__.function_id = function_return['id']
    #     wia.secret_key = temp_sk
    #
    # def test_functions_call(self):
    #     temp_sk = wia.secret_key
    #     wia.secret_key = wia.device_secret_key
    #     def test_function_2(payload):
    #         print("IN TEST FUNCTION 2")
    #         print(payload)
    #     function_return = wia.Functions.create(name='test_function_2', function=test_function_2)
    #     wia.secret_key = temp_sk
    #     print(function_return)
    #     wia.Stream.connect()
    #     while not wia.Stream.connected:
    #         pass
    #     wia.Functions.call(wia.device_id, function_return['id'], payload='Hello World!')

if __name__ == '__main__':
    unittest2.main()
