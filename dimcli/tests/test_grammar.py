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

        print("....Testing dimensions_url....\n", dimensions_url("01", "stff",))
        print(dimensions_url("01", "publications"))
        # ----
        click.secho("Completed test succesfully", fg="green")

if __name__ == "__main__":
    unittest.main()
