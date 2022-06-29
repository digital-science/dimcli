# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli - Magic commands

`python -m dimcli.tests.test_magics`

"""

from __future__ import print_function

import unittest, os, sys, click
import configparser

from .. import *
from ..core.auth import USER_CONFIG_FILE_PATH
from ..utils import *
from ..jupyter.magics import DslMagics

from .settings import API_INSTANCE


class TestMagics(unittest.TestCase):

    """NOTE 
    These tests run the DSL magics but also test the --nice and --links modifications. 
    Respectively:  
    utils.dim_utils.dimensions_styler
    utils.converters.DslDataConverter
    """

    click.secho("**test_magics.py**", fg="red")
    login(instance=API_INSTANCE)
    d = Dsl()

    click.secho("Preparing iPython environment...")
    from IPython.testing.globalipapp import get_ipython
    ip = get_ipython()
    ip.register_magics(DslMagics)

    _q = """ search {} for "Albert Einstein" return {}[basics] limit 10 """
    QUERIES = []
    for source in G.sources():
        q = _q.format(source, source)
        QUERIES += [q]
    QUERIES.reverse()     

    def test_001(self):
        click.secho("\nTEST 001: DSLDF with LINKS flag.", bg="green")
        # ----
        for q in self.QUERIES:
            click.secho(f"Query: {q}", fg="green")
            df = self.ip.run_cell_magic(magic_name='dsldf', line='--links', cell=q)
            print(df)

    def test_002(self):
        click.secho("\nTEST 001: DSLDF with NICE flag.", bg="green")
        # ----
        for q in self.QUERIES:
            click.secho(f"Query: {q}", fg="green")
            df = self.ip.run_cell_magic(magic_name='dsldf', line='--nice', cell=q)
            print(df)


    def test_003(self):
        click.secho("\nTEST 001: DSLDF with NICE and LINKS flag.", bg="green")
        # ----
        for q in self.QUERIES:
            click.secho(f"Query: {q}", fg="green")
            df = self.ip.run_cell_magic(magic_name='dsldf', line='--nice --links', cell=q)
            print(df)



if __name__ == "__main__":
    unittest.main()
