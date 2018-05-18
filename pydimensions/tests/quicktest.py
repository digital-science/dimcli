#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
simple test queries [for DEVELOPMENT  / not part of official tests]
"""

import click 

from .. import *
from ..lib import *

@click.command()
@click.argument('test_number')
def quicktest_cli(test_number=1):

    test_number = int(test_number)

    if test_number == 1:
        print('hello')

 
if __name__ == '__main__':
    quicktest_cli()