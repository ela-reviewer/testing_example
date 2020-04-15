from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (bytes, dict, int, list, object, range, str, ascii, chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)

from banker.connection import ConnectionInfo, get_cursor

def main(connection_info, items_to_get, log_file):
    cursor = get_cursor(connection_info)
    query = 'SELECT {} FROM PAYMENT_INFORMATION'.format(','.join(items_to_get))
    cursor.execute(query)
    for result in cursor.fetchall():
        result_string = ",".join(result).replace('0000-0000', '')
        log_file.write_line(result_string)


if __name__ == '__main__':
    main()
