""" Psql commands """

import click

from litp.base.lite import SqLite3


@click.group()
def cli():
    """ Perform transactions on SQLite database"""
    pass


@cli.command()
@click.argument('name')
def show(name):
    """ Show schema of database """
    sql_db = SqLite3(name)
    sql_db.get_schema()
