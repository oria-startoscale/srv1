#!/usr/bin/env python
import setuptools


setuptools.setup(
    name='srv1-client',
    git_version=True,
    author='Stratoscale',
    author_email='stratoscale@stratoscale.com',
    description='srv1-client',
    keywords='srv1-client',
    url='http://packages.python.org/srv1-client',
    packages=['srv1_client', ],
    install_requires=[
        'munch==2.0.4',
        'requests==2.6',
    ],
    entry_points={
        "strato.clients": [
            "srv1 = srv1_client.client:Client"
            ]
    },
    data_files=[
        ('/etc/stratoscale/api-docs', ['api-docs/srv1.json'])
    ],
)
