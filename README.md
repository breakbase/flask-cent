Flask-Feature
=============

This is a Flask extension for [centrifugal/cent](https://github.com/centrifugal/cent).

### Configuring your app

```python
from flask.ext.cent_client import CentClient
cent = CentClient(app)
```

Alternatively, you can configure it with the factory pattern:
```python
cent = CentClient()
cent.init_app(app)
```

### Publishing to the client
First create a message:

```python
from flask_cent import Message

@app.route("/")
def index():
    cent.send(Message('channel_id', { 'message': 'contents' }))
```
