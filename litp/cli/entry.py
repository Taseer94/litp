""" Command Line Interface"""

import os
import sys
import click
import pkg_resources as pkg


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))


class Context(object):
    """ Load configuration and pass to subcommands """


pass_context = click.make_pass_decorator(Context, ensure=True)


class LitpCli(click.MultiCommand):
    """ Cli handler"""

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.startswith('cmd_') and filename.endswith('.py'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('litp.cli.commands.cmd_' + name, None, None, ['cli'])
        except ImportError:
            return
        return mod.cli

@click.command(cls=LitpCli, context_settings=CONTEXT_SETTINGS,
               invoke_without_command=True)
@click.option('-d', '--debug', is_flag=True, help='Enable detailed traceback')
@click.version_option(pkg.require('litp')[0])
def cli(debug):
    if debug:
        sys.tracebacklimit = 8
