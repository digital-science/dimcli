# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli 
"""

from __future__ import print_function

import unittest, os, sys, click
import configparser

from .. import *
from ..core.api import USER_CONFIG_FILE_PATH
from ..shortcuts import *


class TestOne(unittest.TestCase):

    """
    Tests  
    """

    click.secho("**TESTS**", fg="red")

    def test_000(self):
        click.secho("\nTEST 000: checking that grammar data is valid.", fg="green")
        # ----
        g = G
        print(g)
        print("*STARTS*", g.allowed_starts())
        print("*LANG*", g.lang())
        print("*SOURCES*", g.sources())
        print("*ENTITIES*", g.entities())
        for x in g.sources():
            print("============", x, "============")
            print(g.url_for_source(x))
            for y in g.fields_for_source(x):
                print("...", y, " => ", str(g.desc_for_source_field(x, y)), "**facet?**", str(g.entity_type_for_source_facet(x, y)), str(g.fields_for_entity_from_source_facet(x, y)))

        for x in g.entities():
            print("============", x, "============")
            for y in g.fields_for_entity(x):
                print("...",  y, " => ", str(g.desc_for_entity_field(x, y)))
        # ----
        click.secho("Completed test succesfully", fg="green")

    def test_001(self):
        click.secho("\nTEST 001: load Dimcli using file-based credentials.", fg="green")
        # ----
        d = Dsl()
        res = d.query("search publications where year=2018 return publications")
        # print("Query results: ", res.keys_and_count())
        # ----
        click.secho("Completed test succesfully", fg="green")

    def test_002(self):
        click.secho("\nTEST 002: load Dimcli by passing credentials explicitly.", fg="green")
        # ----
        # get credentials from file as strings
        config = configparser.ConfigParser()
        config.read(os.path.expanduser(USER_CONFIG_FILE_PATH))
        section = config['instance.live' ]
        USER = section['login']
        PSW = section['password']
        d = Dsl(user=USER, password=PSW)
        res = d.query("search publications where year=2018 return publications")
        # print("Query results: ", res.keys_and_count())
        # ----
        click.secho("\n--------\nCompleted test succesfully", fg="green")

    def test_002_1(self):
        click.secho("\nTEST 002-1: Retain login info and force new login.", fg="green")
        # ----
        d = Dsl(instance="live")
        print(""" Dsl(instance="live"): ==> url=""", d._url)
        res = d.query("""search publications where authors="Pasin" return publications""")
        print(" ==> res.json.keys(): ", res.json.keys())
        d.login(instance="test")
        print(""" d.login(instance="test"): ==> url=""", d._url)
        res = d.query("""search publications where authors="Pasin" return publications""")
        print(" ==> res.json.keys(): ", res.json.keys())
        # ----
        click.secho("\n--------\nCompleted test succesfully", fg="green")

    def test_003(self):
        click.secho("\nTEST 003: Try magic methods on result object.", fg="green")
        # ----
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
        # ----
        click.secho("Query #3... returning dataframe", fg="green")
        res = d.query("""search publications for \"mercedes\" return year""")
        print("Query results: ")
        print(" ==> res.json.keys(): ", res.json.keys())
        print(" ==> len(res): ", len(res))
        print(" ==> res.stats: ", res.stats)
        print(" ==> res.as_dataframe(): ", res.as_dataframe())
        print(" ==> res.as_dataframe('year'): ", res.as_dataframe('year'))
        print(" ==> res.as_dataframe('XXX'): ", res.as_dataframe('XXX'))
        # ----
        click.secho("Completed test succesfully", fg="green")

    def test_004(self):
        click.secho("\nTEST 004: Iterative querying.", fg="green")
        # ----
        d = Dsl()
        res = d.query_iterative("""search publications where journal.title="nature medicine" return publications""")
        print("Query results: ")
        print(" ==> len(res): ", len(res))
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # ----
        click.secho("Completed test succesfully", fg="green")

    def test_005(self):
        click.secho("\nTEST 005: Shortcuts", fg="green")
        
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


    def test_006(self):
        click.secho("\nTEST 006: Chunking Results", fg="green")
        
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

    def test_007(self):
        click.secho("\nTEST 007: Non-search queries.", fg="green")
        # ----
        res= dslquery("""extract_grants(grant_number="185247", funder_name="Swiss National Science Foundation")""")
        print("Query results: ")
        print(" ==> res: ", res)
        print(" ==> res.json: ", res.json)
        # ----
        click.secho("Completed test succesfully", fg="green")

    def test_008(self):
        click.secho("\nTEST 008: UTILS: normalize_key", fg="green")
        
        # ----
        res = dslquery("""search publications where journal.title="nature medicine" return publications[doi+FOR] limit 1000""")
        print("Query results for standard query: ")
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        print(" ==> len([x for x in res.publications if 'FOR' in x]): ", len([x for x in res.publications if 'FOR' in x]))
        print("Now Normalizing the FOR key...")
        normalize_key("FOR", res.publications)
        print(" ==> len([x for x in res.publications if 'FOR' in x]): ", len([x for x in res.publications if 'FOR' in x]))
        # ----
        click.secho("Completed test succesfully", fg="green")


if __name__ == "__main__":
    unittest.main()
