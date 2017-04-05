""" Psql commands """

import click

from litp.base.psql import PSQL


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
    passw = str(raw_input("Password: "))
    host = str(raw_input("Host: "))
    port = str(raw_input("Port: "))

    psql = PSQL(name, username, passw, host, port)


@mapping.command()
def show():
    """ List the current mappings """
    pass


@mapping.command('set', help='Set mappings')
def set_():
    """ Set mappings """
    pass


@cli.command()
def load():
    """ Show the schema"""
    pass
