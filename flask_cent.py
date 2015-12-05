__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = "BreakBase.com"
__license__ = 'MIT'
__copyright__ = "(c) 2015 by BreakBase.com"

import logging

from cent.core import Client as CentCoreClient
from flask import current_app, _app_ctx_stack as stack
from flask.ext.login import current_user

__all__ = ['CentClient']

log = logging.getLogger(__name__)

class CentClient(object):
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.state = self.init_app(app)
        else:
            self.state = None

        # TODO read from configuration/env vars
        #self.client = Client("http://localhost:8000", "development-secret")

    def init_app(self, app):
        client = self.init_cent_client(app.config, app.debug, app.testing)

        app.extensions = getattr(app, 'extensions', {})
        app.extensions['cent'] = client

        return client

    def init_cent_client(self, config, debug=False, testing=False):
        host = config.get('FLASK_CENT_HOST', 'localhost')
        port = config.get('FLASK_CENT_PORT', '8000')
        secret = config.get('FLASH_CENT_SECRET', None)

        return Client(host, port, secret)

class CentClientContext(object):
    @contextmanager
    def record_messages(self):
        if not messages_disptached:
            raise RuntimeError("blicker must be installed")

        published_messages = []

    #def self(self, message):


class Client(CentClientContext):
    def __init__(self, secret, host, port, protocol='http'):
        if secret is None:
            raise RuntimeError("secret is required")

        self.client = CentCoreClient("%s://%s:%s" % protocol, host, port, secret)

    #def publish(channel_id, data):
        #return self.client.publish(channel_id, data)

    #def unsubscribe(user_id):
        #return self.client.unsubscribe(user_id)

    #def disconnect(user_id):
        #return self.client.disconnect(user_id)

    #def stats():
        #return client.stats()

class Message(object):
     def __init__(self, cid):
         self.cid = cid

     def command:
         return command

class Unsubscribe(Message):

class Disconnect(Message):
    pass

class Publish(Message):
     def __init__(self, cid, contents):
         super(self, cid)

         self.contents = contents
