# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli 
"""

from __future__ import print_function

import unittest, os, sys, click
import configparser

from .. import *
from ..core.auth import USER_CONFIG_FILE_PATH
from ..core.utils import dimensions_url
from ..core.api import DslDataset
from ..shortcuts import *


class TestOne(unittest.TestCase):

    """
    Tests  
    """

    click.secho("**TESTS**", fg="red")
    login(instance="live")
    d = Dsl()

    def test_001(self):
        click.secho("\nTEST 001: Iterative querying.", fg="green")
        # ----
        d = Dsl()
        res = d.query_iterative("""search publications where journal.title="nature medicine" and year>2000 return publications""")
        print("Query results: ")
        print(" ==> len(res): ", len(res))
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # ----
        click.secho("\nTEST 001: Iterative querying with custom pause: 5 seconds.", fg="green")
        # ----
        d = Dsl()
        res = d.query_iterative("""search publications where journal.title="nature medicine" and year>2015 return publications""", pause=5)
        print("Query results: ")
        print(" ==> len(res): ", len(res))
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # ----
        click.secho("\nTEST 001: Iterative querying with force=True", fg="green")
        # ----
        d = Dsl()
        q = """search publications 
        where research_orgs.id="grid.5522.0" 
        and year in [2010:2012]
        return publications[basics+category_for+times_cited]
        """
        res = d.query_iterative(q, limit=1000, force=True)
        print("Query results: ")
        print(" ==> len(res): ", len(res))
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # ----
        click.secho("Completed test succesfully", fg="green")


    def test_002(self):
        click.secho("\nTEST 002: Query Shortcuts", fg="green")
        
        # ----
        res = dslquery("""search publications where journal.title="nature medicine" return publications limit 10""")
        print("Query results for `dslquery`: ")
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # ----
        res = dslquery_json("""search publications where journal.title="nature medicine" return publications limit 10""")
        print("Query results for `dslquery_json`: ")
        print(" ==> type(res): ", type(res))
        # ----
        res = dslqueryall("""search publications where year="1815" return publications""")
        print("Query results for `dslqueryall`: ")
        print(" ==> type(res): ", type(res))
        # ----
        click.secho("Completed test succesfully", fg="green")

    def test_003(self):
        click.secho("\nTEST 003: Non-search queries.", fg="green")
        # ----
        res= dslquery("""extract_grants(grant_number="185247", funder_name="Swiss National Science Foundation")""")
        print("Query results: ")
        print(" ==> res: ", res)
        print(" ==> res.json: ", res.json)
        # ----
        click.secho("Completed test succesfully", fg="green")


    def test_004(self):
        click.secho("\nTEST 004: Try magic methods on DslDataset object.", fg="green")
        # ----
        login(instance="live")
        d = Dsl()
        click.secho("Query #1... returning publications", fg="green")
        res = d.query("search publications where year=2018 return publications")
        print("Query results: ")
        print(" ==> res.json.keys(): ", res.json.keys())
        print(" ==> res['publications'][0]: ", res['publications'][0])
        print(" ==> len(res): ", len(res))
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> res['not_there']: ", res['not_there'])
        print(" ==> res.publications[0]: ", res.publications[0])
        print(" ==> res.stats: ", res.stats)
        # ----
        click.secho("Query #2... returning facet", fg="green")
        res = d.query("""search publications for \"bmw\" return year""")
        print("Query results: ")
        print(" ==> res.json.keys(): ", res.json.keys())
        print(" ==> res['year'][0]: ", res['year'][0])
        print(" ==> len(res): ", len(res))
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> res['not_there']: ", res['not_there'])
        print(" ==> res.year[0]: ", res.year[0])
        print(" ==> res.stats: ", res.stats)
        click.secho("Completed test succesfully", fg="green")


    def test_005(self):
        click.secho("\nTEST 005: Chunking Results", fg="green")
        
        # ----
        res = dslquery("""search publications where journal.title="nature medicine" return publications limit 1000""")
        print("Query results for standard query: ")
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        print("Now chunking with default size: ")
        test = [len(x) for x in res.chunks()]
        print(" ==> [len(x) for x in res.chunks()]: ", str(test)) 
        print("Now chunking with size 50: ")
        test = [len(x) for x in res.chunks(50)]
        print(" ==> [len(x) for x in res.chunks()]: ", str(test)) 
        print("Now chunking with wrong key (should fail): ")
        test = [len(x) for x in res.chunks(key="badkey")]
        # ----

    def test_006(self):
        click.secho("\nTEST 006: Building dimcli.DslDataset objects from data.", fg="green")
        # ----
        data = dslquery("""search publications for "malaria" return publications""")
        res = DslDataset.from_publications_list(data.publications)
        res.as_dataframe_authors()
        res.count_total
        data = dslquery("""search patents for "graphene" return patents""")
        res = DslDataset.from_patents_list(data.patents)
        res.as_dataframe()
        res.count_total
        # ----
        click.secho("\nBuilding dimcli.DslDataset objects from DATAFRAME data.", fg="green")
        # ----
        data = dslquery("""search publications for "malaria" return publications""").as_dataframe()
        res = DslDataset.from_publications_list(data)
        res.as_dataframe_authors()
        res.count_total
        data = dslquery("""search patents for "graphene" return patents""").as_dataframe()
        res = DslDataset.from_patents_list(data)
        res.as_dataframe()
        res.count_total
        click.secho("Completed test succesfully", fg="green")


if __name__ == "__main__":
    unittest.main()
