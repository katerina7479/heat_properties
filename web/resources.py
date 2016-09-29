'''App Resources classes'''
from flask_restful import Resource, Api


class Property(Resource):
    '''Property Resource'''

    def get(self):


        return {'hello': 'world'}
