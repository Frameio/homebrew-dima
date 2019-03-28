#!/usr/bin/python

"""
    dima
    ~~~~~~~~~~

    Data Integrity Monitoring System
     - A variety of methods/tools to ensure data integrity is maintained

    Args:
     - see dima --help

"""

from collections import defaultdict
from optparse import OptionParser
import os
from pprint import pprint

from psycopg2 import connect, DatabaseError
from terminaltables import AsciiTable


usage = "usage: dima [options] [ show | rm ] filter_keyword"

parser = OptionParser(usage)
parser.add_option("-c", "--conf", dest="config", default='DB',
                  help="Specify a different configuration prefix",
                  metavar="CONF_NAME")

parser.add_option("-f", "--force-terminate",
                  action="store_true", dest="force_terminate", default=False,
                  help="force terminate queries")

(options, args) = parser.parse_args()

def get_credentials():

    creds = defaultdict(dict)
    expected_fields = ['DBNAME', 'HOST', 'PASSWORD', 'PORT', 'USER']

    # Import enviroment variables
    for key, value in os.environ.iteritems():
        if key.startswith('DIMA_'):
            _, category, field = key.split('_')
            creds[category][field] = value.strip()

    # Optionally import from home directory
    if not creds and os.path.exists(os.path.expanduser('~/.dima_creds')):
        with open(os.path.expanduser('~/.dima_creds')) as f:
            for line in f:
                if line.strip():
                    key, value = line.strip().split('=')
                    _, category, field = key.split('_')
                    creds[category][field] = value

    # Make sure all fields are present (even if blank)
    for category in creds.keys():
        missing_fields = [x for x in expected_fields if x not in creds[category]]
        if missing_fields:
            print "Cannot import credentials category `{}`. Missing fields: {}".format(
                category, ", ".join(missing_fields))
            del creds[category]

    if 'DB' not in creds:
        exit("Cannot find DIMA credentials in home directory or environment - see manual for setup")

    return creds

class Postgres:
    def __init__(self):

        creds = get_credentials()[options.config]
        self.connection = connect(
            host=creds['HOST'],
            port=creds['PORT'],
            user=creds['USER'],
            password=creds['PASSWORD'],
            dbname=creds['DBNAME']
        )
        self.cursor = self.connection.cursor()

    def query(self, sql):
        """Query wrapper"""

        try:
            self.cursor.execute(sql)
            for entry in self.cursor:
                entry_as_dict = {}
                for key, value in zip(self.cursor.description, entry):
                    entry_as_dict[key[0]] = value

                yield entry_as_dict

        except DatabaseError, e:
            print "DB Error!" + str(e) + "\n"
            self.__init__()

def stop_queries(db, match):
    """Stops queries"""

    results = list(db.query("SELECT * FROM pg_stat_activity"))

    if match.isdigit():
        terminate_pid(db, match)

    elif match == 'Lock':
        for x in results:
            if x['wait_event_type'] == 'Lock':
                terminate_pid(db, x['pid'])
    else:
        for x in results:
            if match in x['query']:
                terminate_pid(db, x['pid'])

def terminate_pid(db, pid):
    """Terminates a specific PID"""

    conf = "Are you sure you want to terminate PID {}? [y/N]".format(pid)
    if options.force_terminate or raw_input(conf) == 'y':
        sql = 'SELECT pg_terminate_backend({});'.format(pid)
        result = list(db.query(sql))
        db.connection.commit()

        if result:
            print "Terminated PID: {}".format(pid)

def show_queries(db, match=None):

    if match and match[0].isdigit():

        match = match[0]
        data = list(db.query("""
            SELECT *,
                   EXTRACT(EPOCH FROM
                   (CURRENT_TIMESTAMP - query_start))::INT AS age
            FROM pg_stat_activity
            WHERE pid = {}
        """.format(match)))

        if not data:
            print "Queries matching `{}` no longer exist"
        else:
            data = data[0]

        text = data['query']
        del data['query']
        table_data = list(sorted(data.items()))
        print AsciiTable([['Field', "Value"]] + table_data).table
        print AsciiTable([[text]]).table

    else:

        results = list(db.query("""
            --DIMA
            SELECT *,
                   EXTRACT(EPOCH FROM
                   (CURRENT_TIMESTAMP - query_start))::INT AS age
            FROM pg_stat_activity
            WHERE query_start IS NOT NULL
            ORDER BY query_start
        """))

        table = [["PID", "Age (s)", "Lock?", "Query"]]
        for x in results:

            if "--DIMA" in x['query']:
                continue

            if match:
                if match not in x['query'].lower():
                    continue

            lock = True if x['wait_event_type'] == 'Lock' else ""

            small_query = x['query'][:100].replace('\n', ' ').replace('\t', '')
            table.append([x['pid'], x['age'], lock, small_query])

        print AsciiTable(table).table

def main():
    """Handler"""

    db = Postgres()

    if not args:
        show_queries(db, args[1:])

    elif args[0] == 'rm':
        stop_queries(db, args[1])

    elif args[0] == 'show':
        show_queries(db, args[1:])


if __name__ == '__main__':
    main()
