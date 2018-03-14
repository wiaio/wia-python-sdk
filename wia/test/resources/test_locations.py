try:
    import unittest2 as unittest
except ImportError:
    import unittest

import logging
import time
import os

from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class LocationsTest(unittest.TestCase):
    def test_locations_publish_rest(self):
        logging.info("Started test_locations_publish_rest")
        wia = Wia()
        wia.access_token = os.environ['WIA_TEST_DEVICE_SECRET_KEY']
        location = wia.Location.publish(latitude=50, longitude=60)
        self.assertTrue(location.id is not None)
        wia.access_token = None
        logging.info("Finished test_locations_publish_rest")

    def test_location_publish_wrong_params(self):
        logging.info("Started test_location_publish_wrong_params")
        wia = Wia()
        wia.access_token = os.environ['WIA_TEST_DEVICE_SECRET_KEY']
        location = wia.Location.publish(name='fail')
        self.assertIsInstance(location, WiaError)
        wia.access_token = None
        logging.info("Finished test_location_publish_wrong_params")

if __name__ == '__main__':
    unittest2.main()
