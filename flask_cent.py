import blinker
import logging

from cent.core import Client as CentCoreClient

from flask import current_app
from contextlib import contextmanager

__all__ = ['CentClient']

__version_info__ = ('0', '1', '1')
__version__ = '.'.join(__version_info__)
__author__ = "BreakBase.com"
__license__ = 'MIT'
__copyright__ = "(c) 2015 by BreakBase.com"

log = logging.getLogger('flask_cent')


class CentClient(object):

    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(self.app)

    def init_app(self, app):
        self.client = self.make_cent_client(
            app.config.get('FLASK_CENT_HOST', 'localhost'),
            app.config.get('FLASK_CENT_PORT', '8000'),
            app.config.get('FLASK_CENT_PROTOCOL', 'http'),
            app.config.get('FLASK_CENT_SECRET', None)
        )

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['cent'] = self

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

        def record(sender, command, params, **extras):
            messages.append((command, params))

        message_sent.connect(record)

        try:
            yield messages
        finally:
            message_sent.disconnect(record)

    def publish(self, channel_id, **kwargs):
        return self._send('publish', channel_id, kwargs)

    def disconnect(self, user_id):
        return self._send('disconnect', user_id)

    def unsubscribe(self, channel_id):
        return self._send('unsubscribe', channel_id)

    def create_message(self, command, **kwargs):
        """Create a message to use with `batch_send`.

        This is just a simple helper method.
        """
        return command, kwargs

    def batch_send(self, messages):
        for message in messages:
            self._send('add', message)

        return self._send('send')

    def _send(self, command, *args):
        fn = getattr(self.client, command)

        if fn is not None:
            if not self._app.config.get('FLASK_CENT_SUPPRESS', False):
                err = fn(*args)

                if isinstance(err, Exception):
                    message_error.send(current_app._get_current_object(), command=command, params=args)
                else:
                    message_sent.send(current_app._get_current_object(), command=command, params=args)
            else:
                message_sent.send(current_app._get_current_object(), command=command, params=args)


signals = blinker.Namespace()

message_sent = signals.signal('message-sent', doc="""
    Signal is sent when a message is successfully sent via Cent.
""")

message_error = signals.signal('message-error', doc="""
    Signal is sent when a message fails to send via Cent.
""")
