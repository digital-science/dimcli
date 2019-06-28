#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
simple test queries [for DEVELOPMENT  / not part of official tests]

$ pip instal -e .
$ dimcli_quicktest 1

"""

import click 
from .. import *
from ..shortcuts import dslquery

@click.command()
@click.argument('test_number', nargs=1)
def main(test_number=1):
    
    
    test_number = int(test_number)

    if test_number == 1:
        res= dslquery("""extract_grants (funder_name="Department of Biotechnology , Ministry of Science and Technology", grant_number="b52cc8da7ebee12d1e42f8e3f9622e9a")""")
        print(res)

if __name__ == '__main__':
    main()