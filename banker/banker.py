from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from banker.connection import get_connection

# Columns of the `info` table
COLUMNS = [
    'first_name', 'last_name', 'bank_password'
]

class FormatException(Exception):
    """
    Raised on failure to format a valid query
    """
    def __init__(self, reason):
        super(FormatException, self).__init__(reason)
        self.reason = reason

    @classmethod
    def invalid_paramters(cls):
        return cls("Parameters given are not valid!")

    @classmethod
    def no_parameters(cls):
        return cls("No paramters are given!")


def format_query(parameters):
    """
    Foramt a query for the given parameters
    """
    if not parameters:
        raise FormatException.no_parameters()

    if not all(map(lambda p: p in COLUMNS, parameters)):
        raise FormatException.invalid_paramters()

    return 'SELECT {} FROM Info'.format(','.join(parameters))

def parse_result(results):
    """
    Parses the result from a query into a list of strings
    """
    return [",".join(result).encode('ascii')+b'\n' for result in results]

def main(connection, items_to_get, log_file):
    """
    Get the wanted items using the connection, and logs results to log_file
    """
    query = format_query(items_to_get)
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = parse_result(cursor.fetchall())
    log_file.writelines(results)
