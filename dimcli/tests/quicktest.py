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

import requests

@click.command()
@click.argument('test_number', nargs=1)
def main(test_number=1):
    
    
    test_number = int(test_number)

    if test_number == 1:
        res= dslquery("""extract_grants(grant_number="185247", funder_name="Swiss National Science Foundation")""")
        print(len(res))

    if test_number == 2:
        api_key = "uTQEFiYYeBzLSBGZr39zGBhaxuAiLkHp"
        endpoint = "https://sandbox-cris-api.dimensions.ai/"
        url = f"{endpoint}token?api_key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        token = response.text.strip("\n")
        # NOTE token always comes through with newline - WHY ???
        print(token)
        # now query
        q = "search publications return publications"
        # headers = {'Authorization': "Bearer " + token}
        headers = {'Authorization': "Bearer " + token}
        response = requests.post(f"{endpoint}/api/query", data=q, headers=headers)
        try:
            res_json = response.json()
            print(res_json)
        except:
            print('Unexpected error. JSON could not be parsed.')
            print(response)



if __name__ == '__main__':
    main()