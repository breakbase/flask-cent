Flask-Cent
=============

This is a Flask extension for [centrifugal/cent](https://github.com/centrifugal/cent).

### Configuring your app

```python
from flask.ext.cent import CentClient
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

@app.route("/")
def index():
    cent.publish("my_channel_id", key1='value1', key2='value2')
```
