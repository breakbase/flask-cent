import blinker
import logging

from cent.core import Client as CentCoreClient

from flask import current_app
from contextlib import contextmanager

__all__ = ['CentClient']

__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = "BreakBase.com"
__license__ = 'MIT'
__copyright__ = "(c) 2015 by BreakBase.com"

log = logging.getLogger('flask_cent')


class CentClient(object):

    def __init__(self, app=None):
        self.app = app
        self.state = None

        if app is not None:
            self.state = self.init_app(self.app)

    def init_app(self, app):
        self.client = self.make_cent_client(
            app.config.get('FLASK_CENT_HOST', 'localhost'),
            app.config.get('FLASK_CENT_PORT', '8000'),
            app.config.get('FLASK_CENT_PROTOCOL', 'http'),
            app.config.get('FLASK_CENT_SECRET', None)
        )

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['cent'] = self.client

    @property
    def _app(self):
        if self.app:
            return self.app
        else:
            return current_app

    def make_cent_client(self, host, port, protocol, secret):
        if secret is None:
            raise RuntimeError("FLASK_CENT_SECRET is required")

        return CentCoreClient(
            "%s://%s:%s" % (protocol, host, port),
            secret
        )

    @contextmanager
    def record_messages(self):
        # Ensure we can send signals.  Blinker is required
        if not message_sent:
            raise RuntimeError("blinker must be installed")

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
            if not self._app.config.get('FLASK_CENT_SUPPRESS', False):
                err = fn(*args)

                if isinstance(err, Exception):
                    message_error.send('foo')
                else:
                    message_sent.send('foo')
            else:
                message_sent.send('foo')


signals = blinker.Namespace()

message_sent = signals.signal('message-sent', doc="""
    Signal is sent when a message is successfully sent via Cent.
""")

message_error = signals.signal('message-error', doc="""
    Signal is sent when a message fails to send via Cent.
""")
