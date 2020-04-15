from banker.connection import ConnectionInfo
from banker.banker import main
import tempfile
import contextlib

def setup_db():
    # Assume we did stuff here
    pass


def get_db_connection_info():
    return ConnectionInfo('lobal_db', 'secrets', 'root','root')


def log_file_path():
    return tempfile.mkstemp()


@contextlib.cotextmanager
def get_log_file(path):
    with open(path, 'wb') as f:
        yield f

expected_result = [
    ','.join(('1234-1234', 'nitzan', 'elbaz')),
]
def test_it():
    db_info = get_db_connection_info()
    path = log_file_path()
    parameters = ['credit_card', 'first_name', 'last_name']
    with get_log_file(path) as log_file:
        main(db_info, parameters, log_file)
    result = open(path, 'rb').readlines()
    assert len(result) == len(expected_result)
    for line in result:
        assert line in expected_result
