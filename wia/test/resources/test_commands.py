try:
    import unittest2 as unittest
except ImportError:
    import unittest

import time
import os
import logging
import datetime

from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class CommandTest(unittest.TestCase):

    def test_command_create_retrieve_update_delete(self):
        app_key = os.environ['WIA_TEST_APP_KEY']
        wia = Wia()
        wia.app_key = app_key
        access_token = wia.access_token_create(username=os.environ['WIA_TEST_USERNAME'],
                                               password=os.environ['WIA_TEST_PASSWORD'])
        command = wia.Command.create(**{"name": "runTest", "device.id": os.environ['device_id']})
        self.assertEqual(command.name, 'runTest')
        command = wia.Command.retrieve(command.id)
        self.assertEqual(command.name, 'runTest')
        commandUpdated = wia.Command.update(**{"id": command.id, "name": "runTestUpdated", "device.id": os.environ['device_id'], "slug": command.slug})
        self.assertEqual(commandUpdated.name, 'runTestUpdated')
        self.assertTrue(wia.Command.delete(commandUpdated.id))
        wia.access_token = None

    def test_command_list(self):
        app_key = os.environ['WIA_TEST_APP_KEY']
        wia = Wia()
        wia.app_key = app_key
        access_token = wia.access_token_create(username=os.environ['WIA_TEST_USERNAME'],
                                               password=os.environ['WIA_TEST_PASSWORD'])
        commands = wia.Command.list(**{"device.id": os.environ['device_id']})
        self.assertTrue(type(commands['commands']) == list)
        wia.access_token = None




if __name__ == '__main__':
    unittest2.main()
