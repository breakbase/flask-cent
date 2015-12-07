__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = "BreakBase.com"
__license__ = 'MIT'
__copyright__ = "(c) 2015 by BreakBase.com"

import blinker
import logging

from cent.core import Client as CentCoreClient

from flask import current_app
from contextlib import contextmanager

__all__ = ['CentClient']

log = logging.getLogger(__name__)


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

    def publish(self, channel_id, **kwargs):
        return self.send('publish', channel_id, kwargs)

    def disconnect(self, user_id):
        return self.send('disconnect', user_id)

    def unsubscribe(self, channel_id):
        return self.send('unsubscribe', channel_id)

    def send(self, command, *args):
        fn = getattr(self.client, command)

        if fn is not None:
            err = fn(*args)

            if isinstance(err, Exception):
                message_error.send('foo')
            else:
                message_sent.send('foo')


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
