from __future__ import with_statement

import base64
import email
import unittest
import time
import re
import mock
from contextlib import contextmanager

from email.header import Header
from email import charset

from flask import Flask
from flash_cent import CentClient, Publish, Unsubscribe, Disconnect
from speaklater import make_lazy_string


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(self)
        self.app.config.set('FLASH_CENT_SECRET', 'flask-cent-test-secret')

        self.cent = CentClient(self.app)

        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def teardown
        self.ctx.pop()
