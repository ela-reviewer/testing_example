from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (bytes, dict, int, list, object, range, str, ascii, chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)

from collections import namedtuple
import pyodbc

ConnectionInfo = namedtuple('ConnectionInfo', ['server','database','username','password'])

def get_connection(connection_info):
    """
    Gets a cursor into the db
    :param connection_info: Connection paramters to use
    :type connection_info: ConnectionInfo
    """
    server = connection_info.server #'tcp:myserver.database.windows.net'
    database = connection_info.database #'mydb'
    username = connection_info.username #'myusername'
    password = connection_info.password #'mypassword'
    return  pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
