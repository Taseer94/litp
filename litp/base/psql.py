""" The PSQL class"""

import psycopg2 as psql

from litp.base.logger import LitpLogger


logger = LitpLogger('PSQL').get


class PSQL(object):
    """ PSQL clas """

    def __init__(self, datab, pasw):
        self.p_conn = psql.connect(database=datab, user='postgres',
                                   password=pasw, host='localhost', port='5432')

        self.p_cursor = self.p_conn.cursor()
        logger.info("Connected to {}".format(datab))

    def __del__(self):
        self.p_cursor.close()
        self.p_conn.close()

    def exec_query(self, query):
        """ Execute the qurey """
        try:
            self.p_cursor.execute(query)
            self.p_conn.commit()
        except psql.ProgrammingError:
            pass
        except psql.InternalError:
            pass
