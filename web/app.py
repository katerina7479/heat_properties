'''Application Initialization'''
from flask import Flask
from flask_restful import Api
from database import db_session, init_db, load_fixtures
from resources import (
    LatentHeatsResource,
    LatentHeatsListResource,
    SubstanceResource,
    SubstanceListResource
)


app = Flask(__name__)

api = Api(app)
api.add_resource(LatentHeatsResource, '/latent_heats/<string:id>/', endpoint='latent_heat')
api.add_resource(LatentHeatsListResource, '/latent_heats/', endpoint='latent_heats')
api.add_resource(SubstanceResource, '/substances/<string:id>/', endpoint='substance')
api.add_resource(SubstanceListResource, '/substances/', endpoint='substances')
api.add_resource(ElementResource, '/elements/<string:id>/', endpoint='element')
api.add_resource(ElementListResource, '/elements/', endpoint='elements')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    '''Initialize app and run server'''
    app.run(debug=True, host='0.0.0.0')
