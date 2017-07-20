import wia
import unittest2
import time
import os

class CustomerTest(unittest2.TestCase):
    pass

    # both tests work but don't need to keep creating customers

    # def test_signup(self):
    #     wia.secret_key = os.environ['org_secret_key']
    #     wia.app_key = os.environ['app_key']
    #     response = wia.Customer.signup(fullName='Erlich Blachman',
    #                                     email='different@blachmanity.com',
    #                                     password='password2')
    #     print('sign up', response)
    #
    # def test_login(self):
    #     wia.secret_key = os.environ['org_secret_key']
    #     wia.app_key = os.environ['app_key']
    #     response = wia.Customer.login(username='different@blachmanity.com',
    #                                     password='password2')
    #     print('log in', response)

if __name__ == '__main__':
    unittest2.main()
