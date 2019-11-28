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
        # ----
        res = dslquery("""search publications where category_for is empty and journal is empty return publications[doi+category_for+journal] limit 1000""")
        print("Query results for standard query: ")
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # check predicates
        print(" ==> len([x for x in res.publications if x['category_for'] == None]): ", len([x for x in res.publications if x['category_for'] == None]))
        print(" ==> len([x for x in res.publications if x['journal'] == None]): ", len([x for x in res.publications if x['journal'] == None]))
        print("Now Normalizing the category_for key...")
        normalize_key("category_for", res.publications, {})
        print("Now Normalizing the JOURNAL key...")
        normalize_key("journal", res.publications, [])
        print(" ==> len([x for x in res.publications if x['category_for'] == None]): ", len([x for x in res.publications if x['category_for'] == None]))
        print(" ==> len([x for x in res.publications if x['journal'] == None]): ", len([x for x in res.publications if x['journal'] == None]))

        # ----
        click.secho("Completed test succesfully", fg="green")



if __name__ == '__main__':
    main()



