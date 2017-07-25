try:
    import unittest2 as unittest
except ImportError:
    import unittest

import logging
import time
import os

from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class EventsTest(unittest.TestCase):
    def test_events_publish_rest(self):
        logging.info("Starting test_events_publish_rest")
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        event = wia.Event.publish(name='test_event_other_rest', data=130)
        print event
        #self.assertTrue(event.id is not None)
        wia.access_token = None

    def test_events_publish_rest_error(self):
        logging.info("Starting test_events_publish_rest")
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        result = wia.Event.publish(abc='def')
        self.assertIsInstance(result, WiaError)
        wia.access_token = None

if __name__ == '__main__':
    unittest.main()
