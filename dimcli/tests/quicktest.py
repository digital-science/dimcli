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
    dsl = Dsl()
    test_number = int(test_number)

    if test_number == 1:
        res= dsl.query("""extract_grants(grant_number="185247", funder_name="Swiss National Science Foundation")""")
        print("Query results: ")
        print(" ==> res: ", res)
        print(" ==> res.json: ", res.json)

    if test_number == 2:
        res = dsl.query_iterative("""search publications for "bmw" where year in [2018:2020] return publications""", verbose=False)



if __name__ == '__main__':
    main()



