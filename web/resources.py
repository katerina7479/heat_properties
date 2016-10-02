'''App Resources classes'''
from collections import defaultdict
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


class LatentHeatsResource(Resource):
    '''Property Resource'''

    @marshal_with(heat_fields)
    def get(self, id):
        '''Detail GET endpoint'''
        prop = LatentHeats.query.options(joinedload('substance')).filter(LatentHeats.substance_id == id).first()
        if not prop:
            abort(404, message="Property %s doesn't exist" % id)
        return prop


class LatentHeatsListResource(Resource):
    '''Property Resource'''

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.filter_args = [('substance_name', str, ['exact', 'contains']),
                            ('melting_point', int, ['exact', 'gt', 'gte', 'lt', 'lte'])
                            ]
        self.page_args = [('limit', int), ('offset', int)]
        self.initialize_parser()

    def initialize_parser(self):
        '''Add the calculated arguments'''
        for key, type, modifiers in self.filter_args:
            for modifier in modifiers:
                if key == 'exact':
                    key = 'filter[%s]' % key
                else:
                    key = 'filter[%s__%s]' % (key, modifier)
                self.parser.add_argument(key, type=type)
        for key, type in self.page_args:
            self.parser.add_argument('page[%s]' % key, type=type)

    def get_args(self):
        args = self.parser.parse_args()
        filter_args, page_args = [], []
        for key, value in args.iteritems():
            if 'filter' in key and value:
                filter_args.append((key, value))
            if 'page' in key and value:
                page_args.append((key, value))
        return filter_args, page_args

    @marshal_with(heat_fields)
    def get(self):
        '''List endpoint'''
        args = self.get_args()
        print args
        props = LatentHeats.query.options(joinedload('substance')).filter().all()
        return props
