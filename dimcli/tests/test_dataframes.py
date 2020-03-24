# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli - Dataframes
"""

from __future__ import print_function

import unittest, os, sys, click
import configparser

from .. import *
from ..core.auth import USER_CONFIG_FILE_PATH
from ..core.utils import dimensions_url
from ..shortcuts import *


class TestDataframes(unittest.TestCase):

    """
    Tests  
    """

    click.secho("**TESTS**", fg="red")
    login(instance="live")
    d = Dsl()

    def test_001(self):
        click.secho("\nTEST 001: Generic Dataframes.", fg="green")
        # ----
        click.secho("search publications for \"mercedes\" return year", fg="green")
        res = dslquery("""search publications for \"mercedes\" return year""")
        print("Query results: ")
        print(" ==> res.json.keys(): ", res.json.keys())
        print(" ==> len(res): ", len(res))
        print(" ==> res.stats: ", res.stats)
        print(" ==> res.as_dataframe(): ", res.as_dataframe())
        print(" ==> res.as_dataframe('year'): ", res.as_dataframe('year'))
        print(" ==> res.as_dataframe('XXX'): [FAILS] ", res.as_dataframe('XXX'))


    def test_002(self):
        click.secho("\nTEST 002: Authors and Affiliations Dataframes.", fg="green")
        # ----
        print("Testing as_dataframe_authors with legacy `author_affiliations` field: ")
        res = dslquery("""search publications for \"CRISPR\" return publications limit 5""")
        print("Testing as_dataframe_authors on PUBLICATIONS data: ")
        print(" ==> res.as_dataframe_authors(): ", res.as_dataframe_authors())
        print(" ==> res.as_dataframe_authors_affiliations(): ", res.as_dataframe_authors_affiliations())
        # ----
        print("Testing as_dataframe_authors with new `authors` field: ")
        res = dslquery("""search publications for \"CRISPR\" return publications[doi+id+authors] limit 5""")
        print("Testing as_dataframe_authors on PUBLICATIONS data: ")
        print(" ==> res.as_dataframe_authors(): ", res.as_dataframe_authors())
        print(" ==> res.as_dataframe_authors_affiliations(): ", res.as_dataframe_authors_affiliations())
        # ----
        print("Testing as_dataframe_authors on results that have both fields: ")
        res = dslquery("""search publications for \"CRISPR\" return publications[basics+authors] limit 5""")
        print("Testing as_dataframe_authors on PUBLICATIONS data: ")
        print(" ==> res.as_dataframe_authors(): ", res.as_dataframe_authors())
        print(" ==> res.as_dataframe_authors_affiliations(): ", res.as_dataframe_authors_affiliations())
        # ----
        print("Testing as_dataframe_authors on FOR data (FAIL): ")
        res = dslquery("""search publications for \"CRISPR\" return FOR""")
        print(" ==> res.as_dataframe(): ", res.as_dataframe())
        print(" ==> res.as_dataframe_authors(): [=>fails and issue a warning]", res.as_dataframe_authors())
        print(" ==> res.as_dataframe_authors_affiliations(): [=>fails and issue a warning]", res.as_dataframe_authors_affiliations())

    def test_003(self):
        click.secho("\nTEST 003: Grants: funders and investigators Dataframes.", fg="green")
        # ----
        print("Testing as_dataframe_funders on Grants data: ")
        res= dslquery("""search grants return grants[basics+investigator_details]""")
        print(" ==> res.as_dataframe_funders(): ", res.as_dataframe_funders())
        print(" ==> res.as_dataframe_investigators(): ", res.as_dataframe_investigators())
        click.secho("Completed test succesfully", fg="green")


    def test_004(self):
        click.secho("\nTEST 004: UTILS: normalize_key", fg="green")
        
        # ----
        res = dslquery("""search publications where category_for is empty and journal is empty return publications[doi+category_for+journal] limit 1000""")
        print("Query results for standard query: ")
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # check predicates
        print(" ==> len([x for x in res.publications if 'category_for' in x]): ", len([x for x in res.publications if 'category_for' in x ]))
        print(" ==> len([x for x in res.publications if 'journal' in x]): ", len([x for x in res.publications if 'journal' in x]))
        print("Now Normalizing the category_for key...")
        normalize_key("category_for", res.publications, {})
        print("Now Normalizing the JOURNAL key...")
        normalize_key("journal", res.publications, [])
        print(" ==> len([x for x in res.publications if 'category_for' in x]): ", len([x for x in res.publications if 'category_for' in x]))
        print(" ==> len([x for x in res.publications if 'journal' in x]): ", len([x for x in res.publications if 'journal' in x]))
        # ----
        click.secho("Completed test succesfully", fg="green")

    def test_005(self):
        # ----
        click.secho("\nTEST 005: Concepts extraction.", fg="green")
        # ----
        print("Testing as_dataframe_concepts on Publications data: ")
        res= dslquery("""search publications for "graphene" where year=2019 return publications[id+concepts+year+title+category_for] limit 1000""")
        concepts = res.as_dataframe_concepts()
        print(" ==> res.as_dataframe_concepts(): ", concepts)
        concepts.info()
        # ----
        print("Testing as_dataframe_concepts on Grants data: ")
        res= dslquery("""search grants for "graphene" where active_year = 2019 return grants[basics+concepts] limit 500""")
        concepts = res.as_dataframe_concepts()
        print(" ==> res.as_dataframe_concepts(): ", concepts)
        concepts.info()
        click.secho("Completed test succesfully", fg="green")

if __name__ == "__main__":
    unittest.main()
