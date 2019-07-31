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
    
    
    test_number = int(test_number)

    if test_number == 1:
        res= dslquery("""extract_grants(grant_number="185247", funder_name="Swiss National Science Foundation")""")
        print(len(res))

    elif test_number == 2:
        res = dslquery("""search publications where journal.title="nature medicine" return publications[doi+FOR] limit 1000""")
        print("Query results for standard query: ")
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        print(" ==> len([x for x in res.publications if 'FOR' in x]): ", len([x for x in res.publications if 'FOR' in x]))
        print("Now Normalizing the FOR key...")
        normalize_key("FOR", res.publications)
        print(" ==> len([x for x in res.publications if 'FOR' in x]): ", len([x for x in res.publications if 'FOR' in x]))       



if __name__ == '__main__':
    main()



