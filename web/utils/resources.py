'''Common Resource utilities'''
from flask_restful import (
    Resource,
    reqparse
)


class ListFilterResource(Resource):
    '''Generic filtering for List Resources'''

    def __init__(self):
        '''Initialize a ListResource for filtering
           Overwrite in child classes
           self.filters array of tuples, in the order,
                [(<simple argument name>, type, [array of modifiers])]
                e.g.
                self.filters = ['name', str, ['exact', 'contains']]
           self.model = main resource query model
           self.relations = dictionary mapping relationship to model
                e.g.
                self.relations = {'address': Address, 'company': Company}
        '''
        self.parser = reqparse.RequestParser()
        self.filters = []
        self.model = None
        self.relations = {}
        self.paging = [('limit', int), ('offset', int)]

    def initialize_parser(self):
        '''Initializes the parser arguments by json-api spec'''
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
        '''Retrieves the request arguments
           returns filter and page arguments as dicts,
           and sort as a value
        '''
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
        '''Processes limit and offset from page_args'''
        if page_args:
            for key, val in page_args.iteritems():
                if key == 'limit':
                    query = query.limit(val)
                if key == 'offset':
                    query = query.offset(val)
        return query

    def do_filtering(self, query, filter_args):
        '''Processes filter arguments against query'''

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

    def do_sort(self, query, sort):
        '''Sort queryset'''
        if sort:
            query = query.order_by(sort)
        return query
