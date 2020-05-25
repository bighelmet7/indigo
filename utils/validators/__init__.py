import json
import re

from indigo.exceptions.validators import JSONValidatorException, QueryValidatorException


class JSONValidator:
    '''
    JSON validator.
    '''

    def __init__(self, keys=[], help_text=''):
        '''
        @keys list: list of keys that must be in the decoded JSON.
        @help_text str: an example of a valid JSON object.
        '''
        if not isinstance(keys, list):
            raise JSONValidatorException('keys must be a list of strings')
        self.keys = keys
        self.help = help_text

    def __call__(self, value):
        '''
        When the validator is call as a function if there is an recognized error
        return it as a dict() object otherwise return a empty dict(). In the other
        hand, if there is a unexpected error, raise an exception.
        '''
        if not isinstance(value, str):
            raise JSONValidatorException('Value must be a string')
        try:
            q = json.loads(value)
        except json.decoder.JSONDecodeError as e:
            return {'error': str(e)}
        for key in self.keys:
            if key not in q:
                return {'error': '%s not present in param q. Example: %s' % (key, self.help)}
        return {}


class QueryValidator:
    '''
    Query validator, avoid any forbidden operation passed as query.
    '''
    PATTERNS = (
        r'^\*$',
        r'.*=.*',
    )

    def __init__(self, keys_to_inspect=[]):
        '''
        @keys_to_inspect list: all the keys that should be validated, 
        if its contain any forbidden operation.
        '''
        if not isinstance(keys_to_inspect, list):
            raise QueryValidatorException('keys_to_inspect must be a list of strings')
        self.keys = keys_to_inspect

    def __inspect_query(self, query):
        '''
        Look for invalid operations.
        '''
        plain_query = query
        if isinstance(query, list):
            plain_query = '\n'.join(query)
        for pattern in self.PATTERNS:
            match = re.search(pattern, plain_query)
            if match:
                return {'error': 'Invalid query: %s' % match.group()}
        return {}

    def __call__(self, value):
        '''
        Return an error dict if there is any invalid query.

        @value dict: dictionary with the values to inspect.
        '''
        if not isinstance(value, dict):
            raise QueryValidatorException('value must be a dict object')
        error = dict()
        for key in self.keys:
            if key in value:
                query = value.get(key)
                error = self.__inspect_query(query)
                if error:
                    return error
        return error
