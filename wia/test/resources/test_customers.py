try:
    import unittest2 as unittest
except ImportError:
    import unittest

import time
import os
import logging

from wia import Wia
from wia.error import WiaError, WiaValidationError, WiaUnauthorisedError, WiaForbiddenError, WiaNotFoundError

class CustomerTest(unittest.TestCase):

    # def test_customer_create(self):
    #     wia = Wia()
    #     wia.access_token = os.environ['org_secret_key']
    #     wia.app_key = os.environ['app_key']
    #     customer = wia.Customer.create(fullName='John Smith',
    #                                     email='socool@true.com')
    #     self.assertEqual(customer.fullName, 'Eric TheCoolest')
    #     self.assertEqual(customer.email, 'socool@true.com')
    #     self.__class__.test_id = customer.id
    #     wia.access_token = None
    #
    # def test_customer_retrieve(self):
    #     wia = Wia()
    #     wia.access_token = os.environ['org_secret_key']
    #     wia.app_key = os.environ['app_key']
    #     customer = wia.Customer.retrieve(self.__class__.test_id)
    #     self.assertEqual(customer.fullName, 'John Smith')
    #     wia.access_token = None
    #
    # def test_customer_delete(self):
    #     wia = Wia()
    #     wia.access_token = os.environ['org_secret_key']
    #     wia.app_key = os.environ['app_key']
    #     customer = wia.Customer.retrieve(self.__class__.test_id)
    #     self.assertTrue(customer.delete(customer.id))
    #     wia.access_token = None

    # def test_login(self):
    #     wia = Wia()
    #     wia.access_token = os.environ['org_secret_key']
    #     wia.app_key = os.environ['app_key']
    #     response = wia.Customer.login(username='different2@blachmanity.com',
    #                                     password='password2')
    #     print('log in', response)

    # ERROR TESTS
    def test_customer_create_not_authorized(self):
        wia = Wia()
        wia.access_token = os.environ['user_secret_key']
        customer = wia.Customer.create(fullName='miseraable fail', email='try@butfail.com')
        self.assertIsInstance(customer, WiaError)
        wia.access_token = None

    def test_customer_create_wrong_params(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        customer = wia.Customer.create(abc='Not a param')
        self.assertIsInstance(customer, WiaError)
        wia.access_token = None

    def test_customer_create_bad_params(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        customer = wia.Customer.create(fullName='1234', email='invalid')
        self.assertIsInstance(customer, WiaError)
        wia.access_token = None

    def test_customer_delete_not_found(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        customer = wia.Device.delete('oops')
        self.assertIsInstance(customer, WiaError)
        wia.access_token = None

    def test_customer_retrieve_not_found(self):
        wia = Wia()
        wia.access_token = os.environ['org_secret_key']
        customer = wia.Customer.retrieve('Unknown')
        self.assertIsInstance(customer, WiaError)
        wia.access_token = None

if __name__ == '__main__':
    unittest2.main()
