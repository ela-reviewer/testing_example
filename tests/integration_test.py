from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (bytes, dict, int, list, object, range, str, ascii, chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)

from banker.banker import main, COLUMNS, FormatException
import pytest
from contextlib import contextmanager


class LogFileMock(object):
    """
    Mocks a log file object
    usage:
    every call to `write`/`writelines` stores the given data
    calls to `read`/`readlines` returns the data stored using `write`
    """
    def __init__(self):
        self.data_buf = []

    def write(self, buf):
        self.data_buf.append(buf)

    def read(self):
        return b''.join(self.data_buf)

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def readlines(self):
        return list(filter(lambda x: x, self.read().split(b'\n')))



class ConnectionMock(object):
    """
    Mocks a connection object.
    usage:
    call `set_result` with the expected result before a call to `fetchall` or `fetchone` is done.
    every call to `execute`/`execuemany` stores the queries.
    """
    def __init__(self):
        self.queries = []
        self.result = []

    def set_result(self, result):
        self.result = result

    def execute(self, query):
        self.queries.append(query)

    def executemany(self, queries):
        self.queries.extend(queries)

    def fetchone(self):
        return self.result.pop()

    def fetchall(self):
        return self.result

    @contextmanager
    def cursor(self):
        yield self



@pytest.fixture
def expected_values():
    """
    Values to set the table with
    """
    return [('first','last','pass'), ('ella','online','isthebest!!!')]

@pytest.fixture
def query_params():
    """ Get all of the columns in the db """
    return COLUMNS

@pytest.fixture
def formatted_values(expected_values):
    """
    How the values are expected to be formatted
    """
    return [b','.join(vals) for vals in expected_values]

@pytest.fixture
def connection_mock():
    """ Get a connection mock """
    return ConnectionMock()

@pytest.fixture
def log_mock():
    """ Get a log mock """
    return LogFileMock()


@pytest.fixture
def expected_queries(query_params):
    """
    Expected queries to be done in the `main` function depending on query_params
    """
    return [b'SELECT {} from Info'.format(','.join(query_params)).upper()]

def test_main_expected_queries(query_params, expected_queries, connection_mock, log_mock):
    """
    Test that the correct queries are executed
    """
    main(connection_mock, query_params, log_mock)
    # check that only expected queries have been done
    assert len(connection_mock.queries) == len(expected_queries)
    for query in connection_mock.queries:
        assert query.upper() in expected_queries


def test_main_expected_result(query_params, expected_values, formatted_values, connection_mock, log_mock):
    """
    Test that given expected result of queries, to correct data is written to the log
    """
    # pre-set the connection result
    connection_mock.set_result(expected_values)
    main(connection_mock, query_params, log_mock)
    # Check what values were written to the log mock
    assert log_mock.readlines() == formatted_values
