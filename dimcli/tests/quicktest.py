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
    
    
    test_number = int(test_number)

    if test_number == 1:
        dsl = Dsl()
        res = dsl.query_iterative("""search publications where journal.title="nature medicine" return publications""")
        print(res['_stats'])
        print(len(res['publications']))

    elif test_number == 2:
        #     @TODO turn this into a test
        g = G
        print(g)
        print(g.allowed_starts())
        print(g.lang())
        print(g.sources())
        print(g.entities())
        for x in g.sources():
            print("============", x, "============")
            print(g.fields_for_source(x))
            print(g.url_for_source(x))

        for x in g.entities():
            print("============", x, "============")
            print(g.fields_for_entity(x))
 
if __name__ == '__main__':
    main()