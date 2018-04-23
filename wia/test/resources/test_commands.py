try:
    import unittest2 as unittest
except ImportError:
    import unittest

import time
import os
import requests

from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class CommandTest(unittest.TestCase):

    def test_command_create_retrieve_update_run_delete(self):
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
        commandRun = wia.Command.run(**{"id": command.id, "name": "runTestUpdated", "device.id": os.environ['device_id'], "slug": command.slug})
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

    def test_stream_commands(self):
        app_key = os.environ['WIA_TEST_APP_KEY']
        wia = Wia()
        wia.app_key = app_key
        access_token = wia.access_token_create(username=os.environ['WIA_TEST_USERNAME'],
                                               password=os.environ['WIA_TEST_PASSWORD'])
        command = wia.Command.create(**{"name": "test-run", "device.id": os.environ['device_id']})
        wia.Stream.connect()
        count = 0
        while count <= 10:
            time.sleep(0.5)
            count += 1
            if wia.Stream.connected:
                break
        self.assertTrue(wia.Stream.connected)

        def test_run(self):
            wia.Stream.disconnect()
            count = 0
            while count <= 10:
                time.sleep(0.5)
                count += 1
                if not wia.Stream.connected:
                    break
            wia.Stream.connected = False
            wia.access_token = None

        wia.Command.subscribe(**{"device": os.environ['device_id'], "slug": command.slug, "func": test_run})
        time.sleep(2)
        json = {"slug": command.slug, 'device.id': os.environ['device_id']}
        headers = {'Authorization': 'Bearer ' + Wia().access_token}
        r = requests.post("https://api.wia.io/v1/commands/run", json=json, headers=headers)
        #wia.Command.run(**{"device": os.environ['device_id'], "slug": command.slug})
        while wia.Stream.connected:
            time.sleep(0.5)




if __name__ == '__main__':
    unittest2.main()
