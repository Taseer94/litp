""" Psql commands """

import click
from copy import deepcopy
import getpass
from prettytable import PrettyTable

from litp.base import utils
from litp.base.psql import PSQL
from litp.base.lite import SqLite3


@click.group()
def cli():
    """ Perform actions on PSQL database"""
    pass


@cli.group()
def mapping():
    """ View or alter data types"""
    pass


@mapping.command()
def show():
    """ List the current mappings """
    table = PrettyTable(['SQLite', 'PSQL'])
    table.align = 'l'
    for key, value in utils.var_dict.iteritems():
        table.add_row([key, value])
    print table


@mapping.command('set', help='Set mappings')
def set_():
    """ Set mappings """
    pass


@cli.group()
def load():
    """ Load schema or data """
    pass


@load.command()
@click.option('-l', '--lite', help='SQLite DB')
@click.option('-p', '--psql', help='PSQL DB')
def schema(lite, psql):
    """ Load the schema """
    sql_db = SqLite3(lite)

    passw = getpass.getpass('Password: ')
    psql_db = PSQL(psql, passw)

    lite_schema = sql_db.get_schema()

    for row in lite_schema:
        query = ""
        query = deepcopy(row[4])
        if query:
            for key in utils.var_dict:
                query = query.replace(key, utils.var_dict[key])
            psql_db.exec_query(query)


@load.command()
@click.option('-l', '--lite', help='SQLite DB')
@click.option('-p', '--psql', help='PSQL DB')
def data(lite, psql):
    """ Load data """
    sql_db = SqLite3(lite)

    passw = getpass.getpass('Password: ')
    psql_db = PSQL(psql, passw)

    #query = """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""
    #tables = psql_db.exec_query(query)
    tables = ['device', 'mac_vendor', 'dhcp6_enterprise', 'dhcp_fingerprint',
              'dhcp6_fingerprint', 'user_agent', 'dhcp_vendor', 'combination']

    for table in tables:
        result = sql_db.execute_query("SELECT * FROM {}".format(table))
        for row in result:
            values = []
            for i in range(0, len(row)):
                if isinstance(row[i], unicode):
                    values.insert(i, row[i].encode('ascii', 'ignore'))
                elif row[i] is None:
                    values.insert(i, 0)
                else:
                    values.insert(i, row[i])
                values = tuple(values)
                query = "INSERT INTO {} VALUES {}".format(table, values)
                psql_db.exec_query(query)
