# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli - Dataframes

python -m dimcli.tests.test_dataframes

"""

from __future__ import print_function

import unittest, os, sys, click
import configparser

from .. import *
from ..core.auth import USER_CONFIG_FILE_PATH
from ..utils import *

from .settings import API_INSTANCE


class TestDataframes(unittest.TestCase):

    """
    Tests  
    """

    click.secho("**test_dataframes.py**", fg="red")
    login(instance=API_INSTANCE)
    d = Dsl()

    def test_001(self):
        click.secho("\nTEST 001: Generic Dataframes.", bg="green")
        # ----
        click.secho("search publications for \"mercedes\" return year", fg="green")
        res = dslquery("""search publications for \"mercedes\" return year""")
        click.secho("Query results: ", fg="magenta")
        print(" ==> res.json.keys(): ", res.json.keys())
        print(" ==> len(res): ", len(res))
        print(" ==> res.stats: ", res.stats)
        print(" ==> res.as_dataframe(): ", res.as_dataframe())
        print(" ==> res.as_dataframe('year'): ", res.as_dataframe('year'))
        print(" ==> res.as_dataframe('XXX'): [FAILS] ", res.as_dataframe('XXX'))
        # ----
        click.secho("Query returning Hyperlinks and NICE methods", fg="green")
        click.secho("search publications for \"science\" return publications[basics] limit 200", fg="green")
        res = dslquery("""search publications for \"science\" return publications[basics] limit 200""")
        click.secho("Query results: ", fg="magenta")
        print(" ==> res.json.keys(): ", res.json.keys())
        print(" ==> len(res): ", len(res))
        print(" ==> res.stats: ", res.stats)
        print(" ==> res.as_dataframe(links=True): ", res.as_dataframe(links=True))
        print(" ==> res.as_dataframe(nice=True): ", res.as_dataframe(nice=True))
        print(" ==> res.as_dataframe(links=True, nice=True): ", res.as_dataframe(links=True, nice=True))      


    def test_002(self):
        click.secho("\nTEST 002: Authors and Affiliations Dataframes.", bg="green")
        # ----
        click.secho("Testing as_dataframe_authors with legacy `author_affiliations` field: ", fg="magenta")
        res = dslquery("""search publications for \"CRISPR\" return publications limit 5""")
        print("Testing as_dataframe_authors on PUBLICATIONS data: ")
        print(" ==> res.as_dataframe_authors(): ", res.as_dataframe_authors())
        print(" ==> res.as_dataframe_authors_affiliations(): ", res.as_dataframe_authors_affiliations())
        # ----
        click.secho("Testing as_dataframe_authors with new `authors` field: ", fg="magenta")
        res = dslquery("""search publications for \"CRISPR\" return publications[doi+id+authors] limit 5""")
        click.secho("Testing as_dataframe_authors on PUBLICATIONS data: ", fg="magenta")
        print(" ==> res.as_dataframe_authors(): ", res.as_dataframe_authors())
        print(" ==> res.as_dataframe_authors_affiliations(): ", res.as_dataframe_authors_affiliations())
        # ----
        click.secho("Testing as_dataframe_authors on results that have both fields: ", fg="magenta")
        res = dslquery("""search publications for \"CRISPR\" return publications[basics+authors] limit 5""")
        click.secho("Testing as_dataframe_authors on PUBLICATIONS data: ", fg="magenta")
        print(" ==> res.as_dataframe_authors(): ", res.as_dataframe_authors())
        print(" ==> res.as_dataframe_authors_affiliations(): ", res.as_dataframe_authors_affiliations())
        # ----
        click.secho("Testing as_dataframe_authors on FOR data (FAIL): ", fg="magenta")
        res = dslquery("""search publications for \"CRISPR\" return FOR""")
        print(" ==> res.as_dataframe(): ", res.as_dataframe())
        print(" ==> res.as_dataframe_authors(): [=>fails and issue a warning]", res.as_dataframe_authors())
        print(" ==> res.as_dataframe_authors_affiliations(): [=>fails and issue a warning]", res.as_dataframe_authors_affiliations())

    def test_003(self):
        click.secho("\nTEST 003: Grants: funders and investigators Dataframes.", bg="green")
        # ----
        click.secho("Testing as_dataframe_funders on Grants data: ", fg="magenta")
        res= dslquery("""search grants return grants[basics+investigators]""")
        print(" ==> res.as_dataframe_funders(): ", res.as_dataframe_funders())
        print(" ==> res.as_dataframe_investigators(): ", res.as_dataframe_investigators())
        click.secho("Completed test succesfully", fg="green")


    def test_004(self):
        click.secho("\nTEST 004: UTILS: normalize_key", bg="green")
        
        # ----
        res = dslquery("""search publications where category_for is empty and journal is empty return publications[doi+category_for+journal] limit 1000""")
        click.secho("Query results for standard query: ", fg="magenta")
        print(" ==> res['stats']: ", res['stats'])
        print(" ==> len(res['publications']): ", len(res['publications']))
        # check predicates
        print(" ==> len([x for x in res.publications if 'category_for' in x]): ", len([x for x in res.publications if 'category_for' in x ]))
        print(" ==> len([x for x in res.publications if 'journal' in x]): ", len([x for x in res.publications if 'journal' in x]))
        click.secho("Now Normalizing the category_for key...", fg="magenta")
        normalize_key("category_for", res.publications, {})
        click.secho("Now Normalizing the JOURNAL key...", fg="magenta")
        normalize_key("journal", res.publications, [])
        print(" ==> len([x for x in res.publications if 'category_for' in x]): ", len([x for x in res.publications if 'category_for' in x]))
        print(" ==> len([x for x in res.publications if 'journal' in x]): ", len([x for x in res.publications if 'journal' in x]))
        # ----
        click.secho("Completed test succesfully", fg="green")

    def test_005(self):
        # ----
        click.secho("\nTEST 005: Concepts extraction.", bg="green")
        # ----
        click.secho("Testing as_dataframe_concepts on Publications data: ", fg="magenta")
        res= dslquery("""search publications for "graphene" where year=2019 return publications[id+concepts+year+title+doi+journal] limit 1000""")
        concepts = res.as_dataframe_concepts()
        print(" ==> res.as_dataframe_concepts(): ", concepts)
        concepts.info()
        # ----
        click.secho("Testing as_dataframe_concepts on Publications data - using SCORES: ", fg="magenta")
        res= dslquery("""search publications for "graphene" where year=2019 return publications[id+concepts_scores+year+title+doi+journal] limit 1000""")
        concepts = res.as_dataframe_concepts()
        print(" ==> res.as_dataframe_concepts(): ", concepts)
        concepts.info()
        # ----
        click.secho("Testing as_dataframe_concepts on Grants data: ", fg="magenta")
        res= dslquery("""search grants for "graphene" where active_year = 2019 return grants[basics+concepts] limit 500""")
        concepts = res.as_dataframe_concepts()
        print(" ==> res.as_dataframe_concepts(): ", concepts)
        concepts.info()
        click.secho("Completed test succesfully", fg="green")




if __name__ == "__main__":
    unittest.main()
