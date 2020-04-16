from banker.connection import ConnectionInfo, get_connection
from banker.banker import main
import tempfile
import contextlib
import pytest

@pytest.fixture
def expected_values():
    """
    Values to set the table with
    """
    return (('first','last','pass'), ('ella','online','isthebest!!!'))

@pytest.fixture
def formatted_values(expected_values):
    """
    How the values are expected to be formatted
    """
    return [','.join(vals) for vals in expected_values]

@pytest.fixture
def setup_db(db_connection, expected_values):
    """
    Sets up the database with a `secrets` table and the expected values
    """
    db_connection.execute('DELETE from Info')
    with db_connection.cursor() as cursor:
        cursor.executemany('INSERT INTO Info (first_name, last_name, bank_password) VALUES (?,?,?)',expected_values)
    db_connection.commit()


@pytest.fixture
def db_info():
    """
    Connection info to the testing database
    """
    return ConnectionInfo(r'(localdb)\.\BanerDBSharedApp1', 'secrets', 'root','root')


@pytest.fixture
def db_connection(db_info):
    con =  get_connection(db_info)
    yield con
    con.close()


@pytest.fixture
def log_path():
    """
    Get a path to the log file
    """
    return tempfile.mkstemp()[1]


@contextlib.contextmanager
def get_log_file(path):
    """
    Open a log file object
    """
    with open(path, 'wb') as f:
        yield f


def test_success(setup_db, log_path, db_connection, formatted_values):
    """
    Test the happy flow of the program
    """
    parameters = ['first_name', 'last_name', 'bank_password']
    with get_log_file(log_path) as log_file:
        main(db_connection, parameters, log_file)
    result = open(log_path, 'rb').readlines()
    assert len(result) == len(formatted_values)
    for line in result:
        line = line.strip('\n')
        assert line in formatted_values
