__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = "BreakBase.com"
__license__ = 'MIT'
__copyright__ = "(c) 2015 by BreakBase.com"

import blinker
import logging

from cent.core import Client as CentCoreClient

from flask import current_app, _app_ctx_stack as stack
from contextlib import contextmanager

__all__ = ['CentClient']

log = logging.getLogger(__name__)

class Message(object):
     def __init__(self, *args):
         self.args = args

     def command():
         return command

class Unsubscribe(Message):
    command = 'unsubscribe'

class Disconnect(Message):
    command = 'disconnect'

class Publish(Message):
    command = 'publish'


class ClientContext(object):
    @contextmanager
    def record_messages(self):
        if not message_sent: # signals required
            raise RuntimeError("blicker must be installed")

        messages = []

        def record(message, **extras):
            messages.append(message)

        message_sent.connect(record)

        try:
            yield messages
        finally:
            message_sent.disconnect(record)

    def send(self, message):
        fn = getattr(self.client, message.command)

        if fn is not None:
            err = fn(*message.args)

            if err is None:
                message_sent.send(message)
            else:
                message_error.send(message)

class CentClient(ClientContext):
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_cent_client(app.config, app.debug, app.testing)

            app.extensions = getattr(app, 'extensions', {})
            app.extensions['cent'] = self.client

    def init_cent_client(self, config, debug=False, testing=False):
        host = config.get('FLASK_CENT_HOST', 'localhost')
        port = config.get('FLASK_CENT_PORT', '8000')
        protocol = config.get('FLASK_CENT_PROTOCOL', 'http')
        secret = config.get('FLASH_CENT_SECRET', None)

        if secret is None:
            raise RuntimeError("secret is required")

        self.client = CentCoreClient("%s://%s:%s" % (protocol, host, port), secret)

signals = blinker.Namespace()

message_sent = signals.signal('message-sent', doc="""
    Signal is sent when a message is successfully sent via Cent.
""")

message_error = signals.signal('message-error', doc="""
    Signal is sent when a message fails to send via Cent.
""")
