#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
simple test queries [for DEVELOPMENT  / not part of official tests]

$ pip instal -e .
$ dimcli_quicktest 1

"""

import click 
import os
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
        # ----
        print(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates')))

        # ----
        click.secho("Completed test succesfully", fg="green")



if __name__ == '__main__':
    main()



