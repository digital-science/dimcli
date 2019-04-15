# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli 
"""

from __future__ import print_function

import unittest, os, sys, click
import configparser

from .. import *
from ..core.api import USER_CONFIG_FILE


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
        config.read(os.path.expanduser(USER_CONFIG_FILE))
        section = config['instance.live' ]
        USER = section['login']
        PSW = section['password']
        d = Dsl(user=USER, password=PSW)
        res = d.query("search publications where year=2018 return publications")
        # print("Query results: ", res.keys_and_count())
        # ----
        click.secho("\n--------\nCompleted all tests", fg="green")

    def test_003(self):
        click.secho("\nTEST 003: Try magic methods on result object.", fg="green")
        # ----
        d = Dsl()
        res = d.query("search publications where year=2018 return publications")
        print("Query results: ")
        print(" ==> res['publications'][0]: ", res['publications'][0])
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> res['not_there']: ", res['not_there'])
        # ----
        click.secho("Completed test succesfully", fg="green")

    def test_004(self):
        click.secho("\nTEST 004: Iterative querying.", fg="green")
        # ----
        d = Dsl()
        res = d.query_iterative("""search publications where journal.title="nature medicine" return publications""")
        print("Query results: ")
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # ----
        click.secho("Completed test succesfully", fg="green")




if __name__ == "__main__":
    unittest.main()
