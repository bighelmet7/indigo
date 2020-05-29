import json
import re
from collections import OrderedDict

from influxdb.exceptions import InfluxDBClientError

from indigo.extensions import db
from utils.serializer.database import QueryStringSerializer


class QueryPagination(object):
    '''
    Query pagination
    '''

    MAX_CHUNK = 10000

    def __init__(self, query=QueryStringSerializer(), limit=0, offset=0):
        '''
        @query QueryStringSerializer: normalize query to influxdb
        @limit int: limit of points
        @offset int: offset in every request.
        '''
        self.limit = limit
        self.offset = offset
        self.query = query
        self.raw_query = str(self.query)
        self.count = self._count_total_points()

    def get_a_field(self, _from):
        '''
        Look for a field with a float as type, if there are not catch the first string key.
        '''
        _db, _, measurement = _from.split('.')
        result = ''
        try:
            response = db.query('SHOW FIELD KEYS ON {0} FROM {1}'.format(_db, measurement))
        except InfluxDBClientError:
            result = '*'  # worst case
        else:
            points = list(response.get_points())
            for point in points:
                if point.get('fieldType') == 'float':
                    return point.get('fieldKey')
                result = point.get('fieldKey')
        return result

    def _count_total_points(self):
        '''
        Return the total of points of the query select count(*) from db;
        '''
        _from = self.query.internal_query.get('from', '')
        field = self.get_a_field(_from)
        q = 'select count({0}) as total from {1}'.format(field, _from)
        result = 0
        response = list()
        try:
            response = db.query(q, chunked=True, chunk_size=self.MAX_CHUNK)
        except InfluxDBClientError:
            result = -1
        else:
            response = list(response.get_points())
        if response:
            resp_dict = response[0]
            del resp_dict['time']
            keys = list(resp_dict.keys()) # any field value
            result = resp_dict.get(keys[0], -1)
        return result

    def to_dict(self):
        pagination = OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count)
        ])
        try:
            query = self.raw_query + ' limit {0} offset {1}'.format(self.limit, self.offset)
            response = db.query(query, chunked=True, chunk_size=self.MAX_CHUNK)
        except InfluxDBClientError as e:
            return e.content
        result = OrderedDict([
            ('pagination', pagination),
            ('results', list(response.get_points())),
        ])
        return result
