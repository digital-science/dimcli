# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli 

python -m dimcli.tests.test_queries

"""

from __future__ import print_function

import unittest, os, sys, click
import configparser

from .. import *
from ..core.auth import USER_CONFIG_FILE_PATH
from ..core.api import DslDataset
from ..utils import *

from .settings import API_INSTANCE


class TestOne(unittest.TestCase):

    """
    Tests - iterative queries and other related features 
    """

    click.secho("**test_queries.py**", fg="red")
    login(instance=API_INSTANCE)
    d = Dsl()

    def test_001(self):
        click.secho("\nTEST 001-A: Iterative querying.", bg="green")
        # ----
        d = Dsl()
        res = d.query_iterative("""search publications where journal.title="nature medicine" and year>2007 return publications""")
        click.secho("Query results: ", fg="magenta")
        print(" ==> len(res): ", len(res))
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # ----
        click.secho("\nTEST 001-B: Iterative querying with custom pause: 5 seconds.", bg="green")
        # ----
        d = Dsl()
        res = d.query_iterative("""search publications where journal.title="nature medicine" and year>2015 return publications""", pause=5)
        click.secho("Query results: ", fg="magenta")
        print(" ==> len(res): ", len(res))
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # ----
        click.secho("\nTEST 001-C: Iterative querying with force=True", bg="green")
        # ----
        d = Dsl()
        q = """search publications 
        where research_orgs.id="grid.5522.0" 
        and year in [2010:2012]
        return publications[basics+category_for+times_cited]
        """
        res = d.query_iterative(q, limit=1000, force=True)
        click.secho("Query results: ", fg="magenta")
        print(" ==> len(res): ", len(res))
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # ----
        click.secho("\nTEST 001-D: Iterative querying with 'unnest' operator", bg="green")
        # ----
        d = Dsl()
        q = """search publications 
            in title_abstract_only for "cell ontology"
            where year in [2018:2019]
        return publications[id+unnest(researchers)]
        """
        res = d.query_iterative(q)
        click.secho("Query results: ", fg="magenta")
        print(" ==> len(res): ", len(res))
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # ----
        click.secho("\nTEST 001-E: Iterative querying with maxlimit=3000", bg="green")
        # ----
        d = Dsl()
        q = """search publications 
            in title_abstract_only for "cell ontology"
            where year in [2018:2019]
        return publications
        """
        res = d.query_iterative(q, maxlimit=3000)
        click.secho("Query results: ", fg="magenta")
        print(" ==> len(res): ", len(res))
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # ----
        click.secho("\nTEST 001-D: Iterative querying with cumulative warnings", bg="green")
        # ----
        d = Dsl()
        q = """search publications 
        where research_orgs.name = "America" 
        and year in [2010:2012]
        return publications
        """
        res = d.query_iterative(q, limit=1000)
        click.secho("Query results: ", fg="magenta")
        print(" ==> len(res): ", len(res))
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        click.secho("Cumulative warnings: ", fg="magenta")
        print("WARNINGS [{}]".format(len(res["_warnings"])))
        print("\n".join([s for s in res["_warnings"]]))
        # ----
        click.secho("Completed test succesfully", fg="green")


    def test_002(self):
        click.secho("\nTEST 002: Query Shortcuts", bg="green")
        
        # ----
        res = dslquery("""search publications where journal.title="nature medicine" return publications limit 10""")
        click.secho("Query results for `dslquery`: ", fg="magenta")
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # ----
        res = dslquery_json("""search publications where journal.title="nature medicine" return publications limit 10""")
        click.secho("Query results for `dslquery_json`: ", fg="magenta")
        print(" ==> type(res): ", type(res))
        # ----
        res = dslqueryall("""search publications where year="1815" return publications""")
        click.secho("Query results for `dslqueryall`: ", fg="magenta")
        print(" ==> type(res): ", type(res))
        # ----
        click.secho("Completed test succesfully", fg="green")

    def test_003(self):
        click.secho("\nTEST 003: Non-search queries.", bg="green")
        # ----
        res= dslquery("""extract_grants(grant_number="185247", funder_name="Swiss National Science Foundation")""")
        click.secho("Query results: ", fg="magenta")
        print(" ==> res: ", res)
        print(" ==> res.json: ", res.json)
        # ----
        click.secho("Completed test succesfully", fg="green")


    def test_004(self):
        click.secho("\nTEST 004: Try magic methods on DslDataset object.", bg="green")
        # ----
        login(instance=API_INSTANCE)
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
        click.secho("\nTEST 005: Chunking Results", bg="green")
        
        # ----
        res = dslquery("""search publications where journal.title="nature medicine" return publications limit 1000""")
        click.secho("Query results for standard query: ", fg="magenta")
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        click.secho("Now chunking with default size: ", fg="magenta")
        test = [len(x) for x in res.chunks()]
        print(" ==> [len(x) for x in res.chunks()]: ", str(test)) 
        click.secho("Now chunking with size 50: ", fg="magenta")
        test = [len(x) for x in res.chunks(50)]
        print(" ==> [len(x) for x in res.chunks()]: ", str(test)) 
        click.secho("Now chunking with wrong key (should fail): ", fg="magenta")
        test = [len(x) for x in res.chunks(key="badkey")]
        # ----

    def test_006(self):
        click.secho("\nTEST 006: Building dimcli.DslDataset objects from data.", bg="green")
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

    def test_007(self):
        click.secho("\nTEST 007: Save to a JSON file and construct a dimcli.DslDataset objects from JSON file.", bg="green")
        # ----
        FILENAME = "test-api-save.json"
        d = Dsl()
        data = d.query_iterative("""search publications where journal.title="nature medicine" and year>2014 return publications[id+title+year+concepts]""")
        data.to_json_file(FILENAME, verbose=True)
        new_data = DslDataset.load_json_file(FILENAME, verbose=True)
        print(new_data)
        os.remove(FILENAME)
        print("Deleted:", FILENAME)
        click.secho("Completed test succesfully", fg="green")




if __name__ == "__main__":
    unittest.main()
