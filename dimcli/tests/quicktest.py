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
        click.secho("\nTEST 005: Concepts extraction.", fg="green")
        # ----
        print("Testing as_dataframe_concepts on Publications data: ")
        res= dsl.query("""search publications for "graphene" where year=2019 return publications[id+concepts+year+title] limit 100""")
        concepts = res.as_dataframe_concepts()
        print(" ==> res.as_dataframe_concepts(): ", concepts)
        concepts.info()
        # ----
        print("Testing as_dataframe_concepts on Grants data: ")
        res= dsl.query("""search grants for "graphene" where active_year = 2019 return grants[basics+concepts] limit 100""")
        concepts = res.as_dataframe_concepts()
        print(" ==> res.as_dataframe_concepts(): ", concepts)
        concepts.info()
        click.secho("Completed test succesfully", fg="green")


if __name__ == '__main__':
    main()



