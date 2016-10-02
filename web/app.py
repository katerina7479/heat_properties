'''Application Initialization'''
from flask import Flask
from flask_restful import Api
from database import db_session, init_db, load_fixtures
from resources import LatentHeatsResource, LatentHeatsListResource


app = Flask(__name__)

api = Api(app)
api.add_resource(LatentHeatsListResource, '/latent_heat', endpoint='latent_heats')
api.add_resource(LatentHeatsResource, '/latent_heat/<string:id>', endpoint='latent_heat')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    '''Initialize app and run server'''
    init_db()
    load_fixtures()
    app.run(debug=True, host='0.0.0.0')
