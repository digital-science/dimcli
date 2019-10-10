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
        g = G
        print("*CATEGORIES*", g.categories())
        for x in g.categories():
            print("============", x, "============")
            for y in g.categories(x):
                print("...",  y)

    elif test_number == 2:
        res = dslquery("""search publications where journal.title="nature medicine" return publications[doi+FOR] limit 1000""")
        print("Query results for standard query: ")
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        print(" ==> len([x for x in res.publications if 'FOR' in x]): ", len([x for x in res.publications if 'FOR' in x]))
        print("Now Normalizing the FOR key...")
        normalize_key("FOR", res.publications)
        print(" ==> len([x for x in res.publications if 'FOR' in x]): ", len([x for x in res.publications if 'FOR' in x]))       

    elif test_number == 3:
        res = dslquery("search publications where year=2018 return publipcations")
        print("Query BATCH results: ", res.count_batch)
        print("Query TOT results: ", res.count_total)
        print("Query errors: ", res.errors)
        print("Query errors_string: ", res.errors_string)


if __name__ == '__main__':
    main()



