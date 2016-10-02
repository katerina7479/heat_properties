'''App Resources classes'''
from flask_restful import (
    reqparse,
    abort,
    Resource,
    fields,
    marshal_with
)
from sqlalchemy.orm import joinedload
from models import LatentHeats


substance_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'symbol': fields.String,
}


heat_fields = {
    'id': fields.Integer,
    'substance': fields.Nested(substance_fields),
    'melting_point': fields.Integer,
    'boiling_point': fields.Integer,
    'heat_of_vaporization': fields.Float,
    'heat_of_fusion': fields.Float
}

parser = reqparse.RequestParser()


class LatentHeatsResource(Resource):
    '''Property Resource'''

    @marshal_with(heat_fields)
    def get(self, id):
        prop = LatentHeats.query.options(joinedload('substance')).filter(LatentHeats.id == id).first()
        if not prop:
            abort(404, message="Property %s doesn't exist" % id)
        return prop


class LatentHeatsListResource(Resource):
    '''Property Resource'''

    @marshal_with(heat_fields)
    def get(self):
        props = LatentHeats.query.options(joinedload('substance')).all()
        return props
