#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
simple test queries [for DEVELOPMENT  / not part of official tests]

$ pip instal -e .
$ dimcli_quicktest 1

"""

import click 
from .. import *
from ..shortcuts import *

import requests

@click.command()
@click.argument('test_number', nargs=1)
def main(test_number=1):
    
    login()

    test_number = int(test_number)

    if test_number == 1:
        res = dslquery("""search publications for "bmw" return journals limit 1000""")
        print(res.json)
        # print(res.as_dataframe_authors_affiliations())

    if test_number == 2:
        dsl = Dsl()
        res = dsl.query_iterative("""search publications for "bmw" where year in [2018:2020] return publications""")



if __name__ == '__main__':
    main()



