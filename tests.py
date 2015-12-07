from __future__ import with_statement

import unittest
import mock

from flask import Flask
from flask_cent import CentClient, Publish, Unsubscribe, Disconnect


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(self)
        self.app.config['FLASH_CENT_SECRET'] = 'flask-cent-test-secret'
        #self.app.config['FLASH_CENT_SECRET'] = 'development-secret'

        self.cent = CentClient(self.app)

        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def teardown(self):
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
    def test_send_publish_message(self):
        with self.cent.record_messages() as messages:
            with mock.patch.object(self.cent, 'client') as client:
                msg = Publish('channel_id', { 'key': 'value' })

                self.cent.send(msg)
                self.assertEquals(len(messages), 1)

                client.publish.assert_called_once_with(*msg.args)

    def test_send_unsubscribe_message(self):
        with self.cent.record_messages() as messages:
            with mock.patch.object(self.cent, 'client') as client:
                msg = Unsubscribe('user_id')

                self.cent.send(msg)
                self.assertEquals(len(messages), 1)

                client.unsubscribe.assert_called_once_with(*msg.args)

    def test_send_disconnect_message(self):
        with self.cent.record_messages() as messages:
            with mock.patch.object(self.cent, 'client') as client:
                msg = Disconnect('user_id')

                self.cent.send(msg)
                self.assertEquals(len(messages), 1)

                client.disconnect.assert_called_once_with(*msg.args)
