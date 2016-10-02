'''App Resources classes'''
from flask_restful import (
    reqparse,
    abort,
    Resource,
    fields,
    marshal_with
)

from models import Property


property_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'symbol': fields.String,
    'melting_point': fields.Integer,
    'boiling_point': fields.Integer,
    'heat_of_vaporization': fields.Float,
    'heat_of_fusion': fields.Float
}

parser = reqparse.RequestParser()


class PropertyResource(Resource):
    '''Property Resource'''

    @marshal_with(property_fields)
    def get(self, id):
        prop = Property.query.filter(id=id).first()
        if not prop:
            abort(404, message="Property %s doesn't exist" % id)
        return prop


class PropertyListResource(Resource):
    '''Property Resource'''

    @marshal_with(property_fields)
    def get(self):
        props = Property.query.all()
        return props
