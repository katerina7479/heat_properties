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
from models import LatentHeats, Substance


substance_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'symbol': fields.String,
}


heat_fields = {
    'substance_id': fields.Integer,
    'substance': fields.Nested(substance_fields),
    'melting_point': fields.Float,
    'boiling_point': fields.Float,
    'heat_of_vaporization': fields.Integer,
    'heat_of_fusion': fields.Integer
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


class ListFilterResource(Resource):
    '''Generic filtering for List Resources'''
    MODIFIER_MAP = {'gt': '>', 'gte': '>=', 'lt': '>', 'lte': '>='}

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.filters = []
        self.model = None
        self.relations = {}
        self.paging = [('limit', int), ('offset', int)]

    def initialize_parser(self):
        '''Calculate the parser arguments'''
        if self.filters:
            for key, type, modifiers in self.filters:
                for modifier in modifiers:
                    if modifier == 'exact':
                        filter = 'filter[%s]' % key
                    else:
                        filter = 'filter[%s__%s]' % (key, modifier)
                    self.parser.add_argument(filter, type=type)

        for key, type in self.paging:
            self.parser.add_argument('page[%s]' % key, type=type)
        self.parser.add_argument('sort')

    def get_args(self):
        args = self.parser.parse_args()
        filter_args, page_args = {}, {}
        sort = None
        for key, value in args.iteritems():
            if 'filter' in key and value:
                filter_args[key[7:-1]] = value
            elif 'page' in key and value:
                page_args[key[5:-1]] = value
            elif key == 'sort':
                sort = value
        return filter_args, page_args, sort

    def do_paging(self, query, page_args):
        if page_args:
            for key, val in page_args.iteritems():
                if key == 'limit':
                    query = query.limit(val)
                if key == 'offset':
                    query = query.offset(val)
        return query

    def do_filtering(self, query, filter_args):

        def parse_key(key):
            '''Infer the key, modifier, and model from the filter argument'''
            mod = 'exact'
            model = self.model
            if '__' in key:
                k, mod = key.rsplit('__')
                if k in self.relations:
                    rel, k, mod = k, mod, 'exact'
                    model = self.relations[rel]
                if '__' in k:
                    rel, k = k.split('__')
                    model = self.relations[rel]
            else:
                k = key
            return k, mod, model

        if filter_args:
            for key, value in filter_args.iteritems():
                k, mod, model = parse_key(key)
                print k, mod, model, value
                if mod == 'exact':
                    query = query.filter(getattr(model, k) == value)
                elif mod == 'gt':
                    query = query.filter(getattr(model, k) > value)
                elif mod == 'gte':
                    query = query.filter(getattr(model, k) >= value)
                elif mod == 'lt':
                    query = query.filter(getattr(model, k) < value)
                elif mod == 'lte':
                    query = query.filter(getattr(model, k) <= value)
                elif mod == 'contains':
                    query = query.filter(getattr(model, k).like('%%%s%%' % value))
        return query


class LatentHeatsListResource(ListFilterResource):
    '''Property Resource'''

    def __init__(self):
        super(LatentHeatsListResource, self).__init__()
        self.filters = [('substance__name', str, ['exact', 'contains']),
                        ('melting_point', float, ['exact', 'gt', 'gte', 'lt', 'lte']),
                        ('boiling_point', float, ['exact', 'gt', 'gte', 'lt', 'lte']),
                        ('heat_of_vaporization', int, ['exact', 'gt', 'gte', 'lt', 'lte']),
                        ('heat_of_fusion', int, ['exact', 'gt', 'gte', 'lt', 'lte'])
                        ]
        self.relations = {'substance': Substance}
        self.model = LatentHeats
        self.initialize_parser()

    @marshal_with(heat_fields)
    def get(self):
        '''List endpoint'''
        filter_args, page_args, sort = self.get_args()
        props = LatentHeats.query.join(LatentHeats.substance).options(joinedload('substance'))
        props = self.do_filtering(props, filter_args)
        props = self.do_paging(props, page_args)
        if sort:
            props.order_by(sort)
        return props.all()
