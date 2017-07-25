try:
    import unittest2 as unittest
except ImportError:
    import unittest

import time
import os
import logging

from wia import Wia

class InitTest(unittest.TestCase):
    def test_init_access_token(self):
        access_token = os.environ['device_secret_key']
        wia = Wia()
        wia.access_token = access_token
        whoami = wia.WhoAmI.retrieve()
        self.assertIsInstance(whoami, type(wia.WhoAmI))

    def test_stream_connect(self):
        logging.debug("Starting test_stream_connect")
        wia = Wia()
        wia.Stream.connect()
        count = 0
        while count < 5:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                break
        self.assertTrue(wia.Stream.connected)
        logging.debug("Finished test_stream_connect")

if __name__ == '__main__':
    unittest.main()
