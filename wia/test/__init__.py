import wia
import os
import unittest2

# wia.user_secret_key = os.environ['user_secret_key']
# wia.device_secret_key = os.environ['device_secret_key']
# wia.org_secret_key =
# wia.app_key = os.environ['app_key']
#

def all():
    path = os.path.dirname(os.path.realpath(__file__))
    wia.secret_key = os.environ['device_secret_key']
    wia.device_id = wia.Device.retrieve('me').id
    wia.secret_key = None
    return unittest2.defaultTestLoader.discover(path)

def resources():
    path = os.path.dirname(os.path.realpath(__file__))
    return unittest2.defaultTestLoader.discover(
        os.path.join(path, "resources"))
