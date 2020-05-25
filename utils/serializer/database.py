
class QueryStringSerializer(object):
    '''
    Query serializer from a dict object to a query influx string.
    '''

    # BUG: InfluxDB 1.7 for a custom SELECT MUST have at least one field:
    # https://docs.influxdata.com/influxdb/v1.7/query_language/data_exploration/#select-specific-tags-and-fields-from-a-single-measurement

    def __init__(self, db_name='', measurement='', query=dict()):
        '''
        @query dict: the raw query to normalize.
        '''
        if not isinstance(query, dict):
            raise TypeError('query must be a dictionary')
        self.db_name = db_name
        self.measurement = measurement
        self.query = self.__normalize(query)

    def __normalize(self, query):
        '''
        normalize the query into a string object that accomplish the Influxdb
        standards.
        '''
        internal_query = {
            'select': ', '.join(query.get('show', [])),
            'from': '"{0}"."{1}"."{2}"'.format(self.db_name, "autogen", self.measurement),
            'where': ' and '.join(query.get('fields', []))
        }
        template = 'select {select} from {from}'
        if internal_query.get('where', ''):
            template = 'select {select} from {from} where {where}'       
        else:
            internal_query.pop('where')
        result = template.format(**internal_query)
        return result 

    def __repr__(self):
        return self.query

    def __str__(self):
        return self.query
