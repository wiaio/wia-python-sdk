try:
    import unittest2 as unittest
except ImportError:
    import unittest

import time
import os
import logging

from wia import Wia

class StreamTest(unittest.TestCase):

    def setUp(self):
        self.wia = Wia()
        self.wia.access_token = os.environ['device_secret_key']

    def test_stream_connect(self):
        self.wia.Stream.connect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if self.wia.Stream.connected:
                break
        self.assertTrue(self.wia.Stream.connected)

    def test_stream_disconnect(self):
        self.wia.Stream.disconnect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if not self.wia.Stream.connected:
                break
        self.assertFalse(self.wia.Stream.connected)

if __name__ == '__main__':
    unittest2.main()
