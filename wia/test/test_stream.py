try:
    import unittest2 as unittest
except ImportError:
    import unittest

import time
import os
import logging

from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

#def on_connect():
    #print("on_connect called in test")

class StreamTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        wia = Wia()
        wia.access_token = os.environ['user_secret_key']

    def test_stream_connect(self):
        # wia.Stream.client.on_connect = on_connect
        wia = Wia()
        wia.Stream.connect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                break
        self.assertTrue(wia.Stream.connected)

if __name__ == '__main__':
    unittest2.main()
