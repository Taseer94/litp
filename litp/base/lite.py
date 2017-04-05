""" SQLite related transactions """

import sqlite3 as sq
from os import path

class SqLite3(object):
    """ SQLite object"""

    def __init__(self, name):
        self.db_path = path.join(path.dirname(__file__), path.pardir,
                                 path.pardir, 'databases/', name)
        self.s_conn = sq.connect(self.db_path)
        self.s_cursor = self.s_conn.cursor()

    def __del__(self):
        self.s_cursor.close()
        self.s_conn.close()

    def execute_query(self, query):
        """ Execute Query """
        result = self.s_cursor.execute(query)
        self.s_conn.commit()

        return result

    def get_schema(self):
        """ Display schema of sqlite """
        result = self.execute_query('SELECT * FROM sqlite_master;')
        for row in result:
            if row[4] is not None:
                print row[4]
