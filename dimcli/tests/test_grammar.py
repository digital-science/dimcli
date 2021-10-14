# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli  - grammar

python -m dimcli.tests.test_grammar
"""

from __future__ import print_function

import unittest, os, sys, click
import configparser

from .. import *
from ..core.auth import USER_CONFIG_FILE_PATH
from ..utils import *

from .settings import API_INSTANCE


class TestOne(unittest.TestCase):

    """
    Tests  
    """

    click.secho("**test_grammar.py**", fg="red")

    def test_001(self):
        click.secho("\nTEST 001: checking that grammar data is valid.", bg="green")
        # ----
        g = G
        print(g)
        print("*STARTS*", g.allowed_starts())
        print("*LANG*", g.lang())
        print("*SOURCES*", g.sources())
        print("*ENTITIES*", g.entities())
        print("*CATEGORIES*", g.categories())
        for x in g.sources():
            click.secho("============\n" + x + "\n============",  fg="magenta")
            print(g.url_for_source(x))
            for y in g.fields_for_source(x):
                print("...", y, " => ", str(g.desc_for_source_field(x, y)), "**facet?**", str(g.entity_type_for_source_facet(x, y)), str(g.fields_for_entity_from_source_facet(x, y)))

        for x in g.entities():
            click.secho("============\n" + x + "\n============",  fg="magenta")
            for y in g.fields_for_entity(x):
                print("...",  y, " => ", str(g.desc_for_entity_field(x, y)))
        for x in g.categories():
            click.secho("============\n" + x + "\n============",  fg="magenta")
            for y in g.categories(x):
                print("...",  y)


    def test_002(self):
        click.secho("\nTEST 002: dimensions URL generation.", bg="green")
        # ----
        click.secho("""....Testing dimensions_url.... dimensions_url("01", "stff")""",  fg="magenta")
        try:
            print(dimensions_url("01", "stff"))
        except Exception as e:
            print("ERROR:",  e)
        click.secho("""....Testing dimensions_url.... dimensions_url("01", "publications")""",  fg="magenta")
        print(dimensions_url("01", "publications"))
        click.secho("""....Testing dimensions_url....   dimensions_url("pub.1122527319")""",  fg="magenta")
        print(dimensions_url("pub.1122527319"))
        # grants https://app.dimensions.ai/details/grant/grant.8587603
        click.secho("""....Testing dimensions_url....   dimensions_url("01", "grants")""",  fg="magenta")
        print(dimensions_url("01", "grants"))
        click.secho("""....Testing dimensions_url....   dimensions_url("grant.8587603")""",  fg="magenta")
        print(dimensions_url("grant.8587603"))
        # patents https://app.dimensions.ai/details/patent/IN-293637-B
        click.secho("""....Testing dimensions_url....   dimensions_url("IN-293637-B", "patents")""",  fg="magenta")
        print(dimensions_url("IN-293637-B", "patents"))
        click.secho("""....Testing dimensions_url....   dimensions_url("IN-293637-B") [FAILS!]""",  fg="magenta")
        print(dimensions_url("IN-293637-B"))
        # researchers https://app.dimensions.ai/discover/patent?and_facet_researcher=ur.01117537642.02
        click.secho("""....Testing dimensions_url....   dimensions_url("ur.01117537642.02")""",  fg="magenta")
        print(dimensions_url("ur.01117537642.02"))
        click.secho("""....Testing dimensions_url....   dimensions_url("ur.01117537642.02", "researchers")""",  fg="magenta")
        print(dimensions_url("ur.01117537642.02", "researchers"))
        # organizations https://app.dimensions.ai/discover/patent?and_facet_research_org=grid.2515.3
        click.secho("""....Testing dimensions_url....   dimensions_url("grid.2515.3", "organizations")""",  fg="magenta")
        print(dimensions_url("grid.2515.3", "organizations"))
        click.secho("""....Testing dimensions_url....   dimensions_url("grid.2515.3")""",  fg="magenta")
        print(dimensions_url("grid.2515.3"))
        # ----
        click.secho("Completed test succesfully", fg="green")


    def test_003(self):
        click.secho("\nTEST 003: Language utils: DSL escape.", bg="green")
        login(instance=API_INSTANCE)
        d = Dsl()
        # ----
        covid_q = '"2019-nCoV" OR "COVID-19" OR "SARS-CoV-2" OR (("coronavirus"  OR "corona virus") AND (Wuhan OR China))'
        q = f"""search publications 
                in full_data for "{dsl_escape(covid_q)}"  
            return publications[id+doi+pmid+pmcid+title+journal+publisher+mesh_terms+date+year+volume+issue+pages+open_access+type+authors+research_orgs+funders+supporting_grant_ids+times_cited+altmetric+linkout] limit 1"""
        click.secho(q, fg="green")
        print("Success: ", bool(dslquery(q).count_total))
        # ----
        specialchar_q = 'Solar cells: a new technology? (some examples)'
        q = f"""search publications 
                in full_data for "{dsl_escape(specialchar_q, all=True)}"  
            return publications[id+doi+title] limit 1"""
        click.secho(q, fg="green")
        print("Success: ", bool(dslquery(q).count_total))
        # ----
        click.secho("Completed test succesfully", fg="green")


if __name__ == "__main__":
    unittest.main()
