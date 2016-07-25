#!/usr/bin/env python
from setuptools import setup

with open('LONG_DESCRIPTION.rst') as f:
    long_description = f.read()

exec(open("wia/version.py").read())

install_requires = [
    "requests>=2.7,<3.0",
    "paho-mqtt>=1.2"
]

setup(
    name='wia',
    version=VERSION,
    description='This client library is designed to support the Wia APIs',
    author='Wia',
    author_email='team@wia.io',
    maintainer='Conall Laverty',
    maintainer_email='team@wia.io',
    url='https://github.com/wiaio/wia-python-sdk',
    license='MIT',
    test_suite='wia.test.all',
    tests_require=['unittest2', 'mock'],
    packages=['wia', 'wia.test', 'wia.test.resources'],
    long_description=long_description,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    install_requires=install_requires,
)
