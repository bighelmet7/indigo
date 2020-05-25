from flask_api import status
from flask_restful import Resource

from indigo.extensions import db

class InfluxResource(Resource):
    '''
    Influx endpoint to retreive information from the db, such
    as the Version, _internal, ...
    '''
    def get(self):
        return db.ping(), status.HTTP_200_OK

