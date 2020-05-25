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

    def _count_total_points(self):
        '''
        Return the total of points of the query select count(*) from db;
        '''
        _from = re.search("(?<=from)(.*)(?=.*)", self.raw_query)
        if _from:
            path = _from.groups()[0]
            path = path.strip()
        q = 'select count(*) as total from {0}'.format(path)
        result = 0
        response = list()
        try:
            response = db.query(q)
        except InfluxDBClientError:
            result = -1
        else:
            response = list(response.get_points())
        if response:
            result = response[0].get('total_value', -1)
        return result

    def to_dict(self):
        pagination = OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count)
        ])
        try:
            query = self.raw_query + ' limit {0} offset {1}'.format(self.limit, self.offset)
            response = db.query(query)
        except InfluxDBClientError as e:
            return e.content
        result = OrderedDict([
            ('pagination', pagination),
            ('result', list(response.get_points())),
        ])
        return result
