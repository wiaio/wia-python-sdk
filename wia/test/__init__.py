import wia
import os
import unittest2

def all():
    path = os.path.dirname(os.path.realpath(__file__))
    wia.secret_key = os.environ['secret_key']
    wia.device_secret_key = os.environ['device_secret_key']
    wia.app_key = os.environ['app_key']
    wia.device_id = os.environ['device_id']
    wia.org_key = os.environ['org_key']
    return unittest2.defaultTestLoader.discover(path)

def resources():
    path = os.path.dirname(os.path.realpath(__file__))
    return unittest2.defaultTestLoader.discover(
        os.path.join(path, "resources"))
