""" Psql commands """

import click
import getpass
from prettytable import PrettyTable

from litp.base.psql import PSQL
from litp.base import utils


@click.group()
def cli():
    """ Perform actions on PSQL database"""
    pass


@cli.group()
def mapping():
    """ View or alter data types"""
    pass


@cli.command()
def init():
    """ Configure PSQL DB """
    name = str(raw_input("Database Name: "))
    username = str(raw_input("Username: "))
    passw = getpass.getpass("Password: ")
    host = str(raw_input("Host: "))
    port = str(raw_input("Port: "))

    psql = PSQL(name, username, passw, host, port)


@mapping.command()
def show():
    """ List the current mappings """
    data = utils.load()
    table = PrettyTable(['SQLite', 'PSQL'])
    table.align = 'l'
    for entry in data:
        for key, value in entry.iteritems():
            table.add_row([key, value])
    print table


@mapping.command('set', help='Set mappings')
def set_():
    """ Set mappings """
    pass


@cli.command()
def load():
    """ Show the schema"""
    pass
    