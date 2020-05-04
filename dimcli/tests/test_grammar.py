# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli  - logins
"""

from __future__ import print_function

import unittest, os, sys, click
import configparser

from .. import *
from ..core.auth import USER_CONFIG_FILE_PATH
from ..core.utils import dimensions_url
from ..shortcuts import *


class TestOne(unittest.TestCase):

    """
    Tests  
    """

    click.secho("**TESTS**", fg="red")

    def test_001(self):
        click.secho("\nTEST 001: checking that grammar data is valid.", fg="green")
        # ----
        g = G
        print(g)
        print("*STARTS*", g.allowed_starts())
        print("*LANG*", g.lang())
        print("*SOURCES*", g.sources())
        print("*ENTITIES*", g.entities())
        print("*CATEGORIES*", g.categories())
        for x in g.sources():
            print("============", x, "============")
            print(g.url_for_source(x))
            for y in g.fields_for_source(x):
                print("...", y, " => ", str(g.desc_for_source_field(x, y)), "**facet?**", str(g.entity_type_for_source_facet(x, y)), str(g.fields_for_entity_from_source_facet(x, y)))

        for x in g.entities():
            print("============", x, "============")
            for y in g.fields_for_entity(x):
                print("...",  y, " => ", str(g.desc_for_entity_field(x, y)))
        for x in g.categories():
            print("============", x, "============")
            for y in g.categories(x):
                print("...",  y)


    def test_002(self):
        click.secho("\nTEST 002: dimensions URL generation.", fg="green")
        # ----
        print("""....Testing dimensions_url.... dimensions_url("01", "stff")""")
        try:
            print(dimensions_url("01", "stff"))
        except Exception as e:
            print("ERROR:",  e)
        print("""....Testing dimensions_url.... dimensions_url("01", "publications")""")
        print(dimensions_url("01", "publications"))
        print("""....Testing dimensions_url....   dimensions_url("pub.1122527319")""")
        print(dimensions_url("pub.1122527319"))
        # grants https://app.dimensions.ai/details/grant/grant.8587603
        print("""....Testing dimensions_url....   dimensions_url("01", "grants")""")
        print(dimensions_url("01", "grants"))
        print("""....Testing dimensions_url....   dimensions_url("grant.8587603")""")
        print(dimensions_url("grant.8587603"))
        # patents https://app.dimensions.ai/details/patent/IN-293637-B
        print("""....Testing dimensions_url....   dimensions_url("IN-293637-B", "patents")""")
        print(dimensions_url("IN-293637-B", "patents"))
        print("""....Testing dimensions_url....   dimensions_url("IN-293637-B") [FAILS!]""")
        print(dimensions_url("IN-293637-B"))
        # researchers https://app.dimensions.ai/discover/patent?and_facet_researcher=ur.01117537642.02
        print("""....Testing dimensions_url....   dimensions_url("ur.01117537642.02")""")
        print(dimensions_url("ur.01117537642.02"))
        print("""....Testing dimensions_url....   dimensions_url("ur.01117537642.02", "researchers")""")
        print(dimensions_url("ur.01117537642.02", "researchers"))
        # organizations https://app.dimensions.ai/discover/patent?and_facet_research_org=grid.2515.3
        print("""....Testing dimensions_url....   dimensions_url("grid.2515.3", "organizations")""")
        print(dimensions_url("grid.2515.3", "organizations"))
        print("""....Testing dimensions_url....   dimensions_url("grid.2515.3")""")
        print(dimensions_url("grid.2515.3"))
        # ----
        click.secho("Completed test succesfully", fg="green")


    def test_003(self):
        click.secho("\nTEST 003: Language utils: DSL escape.", fg="green")
        login()
        d = Dsl()
        # ----
        covid_q = '"2019-nCoV" OR "COVID-19" OR "SARS-CoV-2" OR (("coronavirus"  OR "corona virus") AND (Wuhan OR China))'
        q = f"""search publications 
                in full_data for "{dsl_escape(covid_q)}"  
            return publications[id+doi+pmid+pmcid+title+journal+publisher+mesh_terms+date+year+volume+issue+pages+open_access_categories+type+authors+research_orgs+funders+supporting_grant_ids+times_cited+altmetric+linkout] limit 1"""
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
