#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
simple test queries [for DEVELOPMENT  / not part of official tests]

$ pip instal -e .
$ dimcli_quicktest 1

"""

import click 
from .. import *

@click.command()
@click.argument('test_number', nargs=1)
def main(test_number=1):
    
    dsl = Dsl()
    test_number = int(test_number)

    if test_number == 1:
        res = dsl.query_iterative("""search publications where journal.title="nature medicine" return publications""")
        print(res['_stats'])
        print(len(res['publications']))

 
if __name__ == '__main__':
    main()