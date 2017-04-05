""" The PSQL class"""

import psycopg2 as psql


class PSQL(object):
    """ PSQL clas """

    def __init__(self, datab, uname, pasw, host, port):
        self.p_conn = psql.connect(database=datab, user=uname,
                                   password=pasw, host=host, port=port)

        self.p_cursor = self.p_conn.cursor()
        self.var_dict = {'int(11)': 'int', 'datetime': 'timestamp',
                         'tinyint(1)': 'smallint'}

    def __del__(self):
        self.p_cursor.close()
        self.p_conn.close()

    def exec_query(self, query):
        """ Execute the qurey"""

        self.p_cursor.execute(query)
        self.p_conn.commit()
