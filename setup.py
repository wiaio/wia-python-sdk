#!/usr/bin/env python
from setuptools import setup

exec(open("wia/version.py").read())

setup(
    name='wia-sdk',
    version=VERSION,
    description='This client library is designed to support the Wia APIs',
    author='Wia',
    maintainer='Conall Laverty',
    maintainer_email='team@wia.io',
    url='https://github.com/wiaio/wia-python-sdk',
    license='MIT',
    packages=["wia"],
    long_description=open("README.md").read(),
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
    install_requires=[
        'requests',
    ],
)
