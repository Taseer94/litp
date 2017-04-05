""" Psql commands """

import click

from litp.base.psql import PSQL


@click.group()
def cli():
    """ Perform actions on PSQL database"""
    pass


@cli.command()
def load():
    """ Show the schema"""
    pass
