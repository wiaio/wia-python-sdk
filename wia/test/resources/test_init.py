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
        logging.debug('Attempting with access token: %s', access_token)
        wia = Wia()
        wia.access_token = access_token
        print wia.access_token
        whoami = wia.WhoAmI.retrieve()
        self.assertIsInstance(whoami, type(wia.WhoAmI))

if __name__ == '__main__':
    unittest.main()
