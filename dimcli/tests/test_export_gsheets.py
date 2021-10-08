# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli 

python -m dimcli.tests.test_export_gsheets

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
    Tests - export functions 
    """

    click.secho("**test_export_gsheets.py**", fg="red")
    login(instance=API_INSTANCE)
    d = Dsl()


    def test_001(self):
        click.secho("\nTEST 001: Save a DslDataset to the 'dimcli-qa-export-live' google sheet.", bg="green")
        click.secho("\nPS ignore the warnings deriving from Unittest & SSLSockets not being closed", fg="green")
        # ----
        d = Dsl()
        data = d.query("""search publications for "neurolink" return publications[id+title+doi+date+unnest(concepts)]""")
        data.to_gsheets(title='dimcli-qa-export-live', verbose=True)
        click.secho("Completed test succesfully", fg="green")
        
    def test_002(self):
        click.secho("\nTEST 002: Save a pd.DataFrame to the 'dimcli-qa-export-live' google sheet.", bg="green")
        click.secho("\nPS ignore the warnings deriving from Unittest & SSLSockets not being closed", fg="green")
        # ----
        d = Dsl()
        data = d.query("""search publications for "malaria" return publications[basics] limit 200""")
        df = data.as_dataframe()
        export_as_gsheets(df, title='dimcli-qa-export-live', verbose=True)
        click.secho("Completed test succesfully", fg="green")


if __name__ == "__main__":
    unittest.main()
