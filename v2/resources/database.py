import datetime
import json

from flask import send_file
from flask_api import status
from flask_restful import Resource, request
from influxdb.exceptions import InfluxDBClientError

from indigo.extensions import db
from utils.pagination.database import QueryPagination
from utils.serializer.database import QueryStringSerializer
from utils.validators import JSONValidator, QueryValidator
from utils.renderers.database import CSVRender


class DatabaseListResource(Resource):

    def get(self):
        '''
        Get all the availables database in our influxdb.
        '''
        result = db.get_list_database()
        return result, status.HTTP_200_OK


class DatabaseRetrieveResource(Resource):

    def get(self, name):
        '''
        Get all the available measurements on the database named 'name'
        '''
        query = 'SHOW MEASUREMENTS ON %s' % name
        response = db.query(query)
        result = list(response.get_points())
        return result, status.HTTP_200_OK


class MeasurementResource(Resource):
    '''
    Measurement resource
    '''

    formats = {
        'csv': CSVRender(),
    }

    #TODO: could we do it with decorators instead of __call__ classes?
    json_validator = JSONValidator(keys=['show', 'fields'], help_text='q={"show":["host,cpu"], "fields":[""host"=\'bkmonasr02\'"]}')
    query_validator = QueryValidator(keys_to_inspect=['show'])

    def get(self, db_name='', measurement=''):
        q = request.args.get('q', r'{}')
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        _format = request.args.get('format', 'json')
        error = self.json_validator(q)
        if error:
            return error, status.HTTP_500_INTERNAL_SERVER_ERROR
        query = json.loads(q)
        error = self.query_validator(query)
        if error:
            return error, status.HTTP_500_INTERNAL_SERVER_ERROR
        query = QueryStringSerializer(db_name=db_name, measurement=measurement, query=query)
        pagination = QueryPagination(query=query, limit=limit, offset=offset)
        result = pagination.to_dict()
        if _format.lower() in self.formats:
            result = self.formats[_format.lower()].render(result.get('results', []))
            filename = 'results.%s.csv' % (datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
            return send_file(result, mimetype='text/csv',as_attachment=True,attachment_filename=filename)
        return result, status.HTTP_200_OK


class TagListResource(Resource):
    '''
    Get list of tags
    '''

    def get(self, db_name, measurement):
        query = 'show tag keys on {db_name} from {measurement}'.format(
            db_name=db_name,
            measurement=measurement
        )
        try:
            response = db.query(query)
        except InfluxDBClientError as e:
            return e.content, status.HTTP_500_INTERNAL_SERVER_ERROR
        result = {
            'tagKeys': [elem.get('tagKey', '') for elem in list(response.get_points())]
        }
        return result, status.HTTP_200_OK


class TagRetrieveResource(Resource):
    '''
    Get all values from a given tag.
    '''

    def get(self, db_name, measurement, tag_key):
        query = 'show tag values on {db_name} from {measurement} with key="{tag_key}"'
        query = query.format(
            db_name=db_name,
            measurement=measurement,
            tag_key=tag_key,
        )
        try:
            response = db.query(query)
        except InfluxDBClientError as e:
            return e.content, status.HTTP_500_INTERNAL_SERVER_ERROR
        result = {
            'values': [elem.get('value', '') for elem in list(response.get_points())]
        }
        return result, status.HTTP_200_OK
