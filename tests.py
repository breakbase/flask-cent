from __future__ import with_statement

import unittest
import mock

from flask import Flask
from flask_cent import CentClient


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(self)
        self.app.config['FLASK_CENT_SECRET'] = 'flask-cent-test-secret'

        self.cent = CentClient(self.app)

        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def teardown(self):
        self.ctx.pop()


class TestCent(TestCase):
    def test_send_publish_message(self):
        with self.cent.record_messages() as messages:
            with mock.patch.object(self.cent, 'client') as client:
                self.cent.publish("channel_id", key="value")
                self.assertEquals(len(messages), 1)

                client.publish.assert_called_once_with("channel_id", {"key": "value"})

    def test_send_unsubscribe_message(self):
        with self.cent.record_messages() as messages:
            with mock.patch.object(self.cent, 'client') as client:
                self.cent.unsubscribe("user_id")
                self.assertEquals(len(messages), 1)

                client.unsubscribe.assert_called_once_with("user_id")

    def test_send_disconnect_message(self):
        with self.cent.record_messages() as messages:
            with mock.patch.object(self.cent, 'client') as client:
                self.cent.disconnect("user_id")
                self.assertEquals(len(messages), 1)

                client.disconnect.assert_called_once_with("user_id")

    def test_suppress_messages(self):
        self.app.config['FLASK_CENT_SUPPRESS'] = True
        with self.cent.record_messages() as messages:
            with mock.patch.object(self.cent, 'client') as client:
                self.cent.disconnect("user_id")
                self.assertEquals(len(messages), 1)

                client.disconnect.assert_not_called()
