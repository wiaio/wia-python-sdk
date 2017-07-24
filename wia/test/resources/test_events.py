try:
    import unittest2 as unittest
except ImportError:
    import unittest

import logging
import time
import os

from wia import Wia

class EventsTest(unittest.TestCase):
    def test_events_publish_rest(self):
        logging.info("Starting test_events_publish_rest")
        wia = Wia()
        wia.access_token = os.environ['device_secret_key']
        event = wia.Event.publish(name='test_event_other_rest', data=130)
        #self.assertTrue(event.id is not None)
        wia.access_token = None

if __name__ == '__main__':
    unittest.main()
