'''App Resources classes'''
from collections import defaultdict
from flask_restful import (
    abort,
    Resource,
    fields,
    marshal_with
)
from sqlalchemy.orm import joinedload
from models import LatentHeats, Substance
from utils.resources import ListFilterResource

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


class LatentHeatsListResource(ListFilterResource):
    '''Property Resource'''

    def __init__(self):
        '''Initialize Filter options'''
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
        props = self.do_sort(props, sort)
        return props.all()



class SubstanceResource(Resource):
    '''Substance Resource'''

    @marshal_with(substance_fields)
    def get(self, id):
        '''Detail GET endpoint'''
        query = Substance.query.filter(Substance.id == id).first()
        if not query:
            abort(404, message="Substance %s doesn't exist" % id)
        return query


class SubstanceListResource(ListFilterResource):
    '''Substances Resource'''

    def __init__(self):
        '''Initialize Filter options'''
        super(SubstanceListResource, self).__init__()
        self.filters = [('name', str, ['exact', 'contains']),
                        ('symbol', str, ['exact', 'contains'])
                        ]
        self.model = Substance
        self.initialize_parser()

    @marshal_with(substance_fields)
    def get(self):
        '''List endpoint'''
        filter_args, page_args, sort = self.get_args()
        query = Substance.query
        query = self.do_filtering(query, filter_args)
        query = self.do_paging(query, page_args)
        query = self.do_sort(query, sort)
        return query.all()
