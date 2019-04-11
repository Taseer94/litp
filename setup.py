"""
Setup File
"""

from setuptools import setup

setup(
    name='litp',
    version='1.0',
    author='Taseer Ahmed',
    py_modules=['litp.cli.entry'],
    install_requires=['Click', 'psycopg2', 'prettytable'],
    entry_points='''
        [console_scripts]
        litp=litp.cli.entry:cli
    ''',
)
