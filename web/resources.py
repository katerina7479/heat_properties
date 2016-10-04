'''App Resources classes'''
from flask_restful import (
    abort,
    Resource,
    fields,
    marshal_with
)
from sqlalchemy.orm import joinedload
from models import (
    LatentHeats,
    Substance,
    Element
)
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

element_fields = {
    'atomic_number': fields.Integer,
    'symbol': fields.String,
    'name': fields.String,
    'molecular_weight': fields.Float,
    'group': fields.String,
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
        self.query = LatentHeats.query.join(LatentHeats.substance).options(joinedload('substance'))
        self.parse_args_to_query(*self.get_args())
        return self.query.all()


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
        self.filters = [('name', str, ['exact', 'contains', 'icontains']),
                        ('symbol', str, ['exact', 'contains', 'icontains'])
                        ]
        self.model = Substance
        self.initialize_parser()

    @marshal_with(substance_fields)
    def get(self):
        '''List endpoint'''
        self.query = Substance.query
        self.parse_args_to_query(*self.get_args())
        return self.query.all()


class ElementResource(Resource):
    '''Element Detail Resource'''

    @marshal_with(element_fields)
    def get(self, id):
        '''Detail GET endpoint'''
        query = Element.query.filter(Element.atomic_number == id).first()
        if not query:
            abort(404, message="Element %s doesn't exist" % id)
        return query


class ElementListResource(ListFilterResource):
    '''Element List Resource'''

    def __init__(self):
        '''Initialize Filter options'''
        super(ElementListResource, self).__init__()
        self.filters = [('name', str, ['exact']),
                        ('symbol', str, ['exact']),
                        ('group', str, ['exact', 'contains', 'icontains']),
                        ('molecular_weight', float, ['exact', 'gt', 'gte', 'lt', 'lte']),
                        ('atomic_number', float, ['exact', 'gt', 'gte', 'lt', 'lte']),
                        ]
        self.model = Element
        self.initialize_parser()

    @marshal_with(element_fields)
    def get(self):
        '''List endpoint'''
        self.query = Element.query
        self.parse_args_to_query(*self.get_args())
        return self.query.all()
