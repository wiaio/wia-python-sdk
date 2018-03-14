try:
    import unittest2 as unittest
except ImportError:
    import unittest

import time
import os
import logging

from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class InitTest(unittest.TestCase):
    def test_init_access_token(self):
        logging.info("Starting test_init_access_token")
        access_token = os.environ['WIA_TEST_DEVICE_SECRET_KEY']
        wia = Wia()
        wia.access_token = access_token
        whoami = wia.WhoAmI.retrieve()
        self.assertIsInstance(whoami, type(wia.WhoAmI))
        access_token = None
        logging.info("Finished test_init_access_token")

    def test_init_app_key_access_token(self):
        logging.info("Starting test_init_access_token")
        app_key = os.environ['WIA_TEST_APP_KEY']
        wia = Wia()
        wia.app_key = app_key
        access_token=wia.access_token_create(username=os.environ['WIA_TEST_USERNAME'],
                                password=os.environ['WIA_TEST_PASSWORD'])
        self.assertIsInstance(access_token, type(wia.AccessToken))
        access_token = None
        logging.info("Finished test_init_app_key_access_token")

    def test_init_app_key(self):
        logging.info("Starting test_init_access_token")
        app_key = os.environ['WIA_TEST_APP_KEY']
        wia = Wia()
        wia.username = os.environ['WIA_TEST_USERNAME']
        wia.password = os.environ['WIA_TEST_PASSWORD']
        wia.app_key = app_key
        whoami = wia.WhoAmI.retrieve()
        self.assertIsInstance(whoami, type(wia.WhoAmI))
        access_token = None
        logging.info("Finished test_init_app_token")

    def test_stream_connect(self):
        logging.info("Starting test_stream_connect")
        access_token = os.environ['WIA_TEST_DEVICE_SECRET_KEY']
        wia = Wia()
        wia.Stream.connect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                break
        self.assertTrue(wia.Stream.connected)
        access_token = None
        logging.info("Finished test_stream_connect")

    def test_stream_disconnect(self):
        logging.info("Starting test_stream_connect")
        wia = Wia()
        wia.Stream.disconnect()
        self.assertFalse(wia.Stream.connected)

if __name__ == '__main__':
    unittest.main()
