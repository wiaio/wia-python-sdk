try:
    import unittest2 as unittest
except ImportError:
    import unittest

import logging
import time
import os
import sys

from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class EventsTest(unittest.TestCase):
    def test_events_publish_rest(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        event = wia.Event.publish(name='test_event_other_rest', data=130)
        self.assertTrue(event.id is not None)
        wia.access_token = None


    def test_events_publish_file(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        dir_path = os.path.dirname(os.path.realpath(__file__))
        result = wia.Event.publish(name='test_event_other_filesud', data=1300, file=open(dir_path+'/test-file.txt', 'rb'))
        wia.access_token = None


    def test_events_publish_file_text(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        dir_path = os.path.dirname(os.path.realpath(__file__))
        result = wia.Event.publish(name='test_event_other_file', file=(dir_path+'/test-file.txt'))
        wia.access_token = None

    # ERROR TESTS
    def test_events_publish_rest_error(self):
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        result = wia.Event.publish(abc='def')
        self.assertIsInstance(result, WiaError)
        wia.access_token = None

if __name__ == '__main__':
    unittest.main()
