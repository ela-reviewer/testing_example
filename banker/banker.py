from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (bytes, dict, int, list, object, range, str, ascii, chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)

from banker.connection import ConnectionInfo, get_connection

COLUMNS = [
    'first_name', 'last_name', 'bank_password'
]

def main(connection_info, items_to_get, log_file):
    cursor = get_connection(connection_info).cursor()
    query = 'SELECT {} FROM Info'.format(','.join(items_to_get))
    cursor.execute(query)
    results = []
    for result in cursor.fetchall():
        results.append(",".join(result).encode('ascii') +b'\n')

    log_file.writelines(results)
    print (results)


if __name__ == '__main__':
    main()
