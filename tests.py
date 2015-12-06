from __future__ import with_statement

import base64
import email
import unittest
import time
import re
from contextlib import contextmanager

from email.header import Header
from email import charset

from flask import Flask
from flask_cent import CentClient, Publish, Unsubscribe, Disconnect


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(self)
        self.app.config['FLASH_CENT_SECRET'] = 'flask-cent-test-secret'

        self.cent = CentClient(self.app)

        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def teardown():
        self.ctx.pop()

class TestPublish(TestCase):
    def setUp(self):
        self.msg = Publish('channel_id', { 'key': 'value' })

    def test_initialize(self):
        self.assertEquals(self.msg.args, ('channel_id', { 'key': 'value' }))

    def test_command(self):
        self.assertEquals(self.msg.command, 'publish')

class TestDisconnect(TestCase):
    def setUp(self):
        self.msg = Disconnect('user_id')

    def test_initialize(self):
        self.assertEquals(self.msg.args, ('user_id',))

    def test_command(self):
        self.assertEquals(self.msg.command, 'disconnect')

class TestUnsubscribe(TestCase):
    def setUp(self):
        self.msg = Unsubscribe('user_id')

    def test_initialize(self):
        self.assertEquals(self.msg.args, ('user_id',))

    def test_command(self):
        self.assertEquals(self.msg.command, 'unsubscribe')

class TestCent(TestCase):
    def test_send(self):
        with self.cent.record_messages() as messages:
            msg = Publish('channel_id', {'key': 'value'})

            self.cent.send(msg)
            self.assertEquals(len(messages), 1)
