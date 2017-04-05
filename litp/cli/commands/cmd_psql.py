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
