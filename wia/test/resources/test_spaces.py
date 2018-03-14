try:
    import unittest2 as unittest
except ImportError:
    import unittest

import logging
import time
import os
import datetime
import random
from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class SpacesTest(unittest.TestCase):
    def test_spaces_create_and_retrieve(self):
        wia = Wia()
        wia.access_token_create(username=os.environ['WIA_TEST_USERNAME'],
                                               password=os.environ['WIA_TEST_PASSWORD'])
        random_name = str(datetime.date.today()) + str(random.getrandbits(128))
        space = wia.Space.create(name=random_name)
        self.assertTrue(space.name == random_name)
        space_retrieve = wia.Space.retrieve(space.id)
        self.assertTrue(space.name == space_retrieve.name)

    def test_spaces_list(self):
        wia = Wia()
        spaces = wia.Space.list()
        self.assertTrue(spaces['count'] > 0)


if __name__ == '__main__':
    unittest.main()
