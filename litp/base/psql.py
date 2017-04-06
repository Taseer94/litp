""" The PSQL class"""

import psycopg2 as psql


class PSQL(object):
    """ PSQL clas """

    def __init__(self, datab, pasw):
        self.p_conn = psql.connect(database=datab, user='postgres',
                                   password=pasw, host='localhost', port='5432')

        self.p_cursor = self.p_conn.cursor()

    def __del__(self):
        self.p_cursor.close()
        self.p_conn.close()

    def exec_query(self, query):
        """ Execute the qurey """
        self.p_cursor.execute(query)
        self.p_conn.commit()
