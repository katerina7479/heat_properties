#!flask/bin/python
from flask import Flask
from flask_restful import Api
from .database import db_session
from .models import Property

app = Flask(__name__)
api = Api(app)
api.add_resource(Property, '/property')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
