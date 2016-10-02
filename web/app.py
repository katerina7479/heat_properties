#!flask/bin/python
from flask import Flask
from flask_restful import Api
from database import db_session, init_db
from resources import PropertyListResource, PropertyResource


app = Flask(__name__)
api = Api(app)
api.add_resource(PropertyListResource, '/property/', endpoint='properties')
api.add_resource(PropertyResource, '/property/<string:id>', endpoint='property')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
