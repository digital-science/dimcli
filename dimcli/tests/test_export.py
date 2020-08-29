# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli 

python -m dimcli.tests.test_export

"""

from __future__ import print_function

import unittest, os, sys, click
import configparser

from .. import *
from ..core.auth import USER_CONFIG_FILE_PATH
from ..core.api import DslDataset
from ..shortcuts import *


class TestOne(unittest.TestCase):

    """
    Tests - export functions 
    """

    click.secho("**TESTS**", fg="red")
    login(instance="live")
    d = Dsl()


    def test_001(self):
        click.secho("\nTEST 001: Save to a JSON file and construct a dimcli.DslDataset objects from JSON file.", fg="green")
        # ----
        FILENAME = "test-api-save.json"
        d = Dsl()
        data = d.query_iterative("""search publications where journal.title="nature medicine" and year>2014 return publications[id+title+year+concepts]""")
        data.save_json(FILENAME, verbose=True)
        new_data = DslDataset.load_json_file(FILENAME, verbose=True)
        print(new_data)
        os.remove(FILENAME)
        print("Deleted:", FILENAME)
        click.secho("Completed test succesfully", fg="green")


    def test_002(self):
        click.secho("\nTEST 002: Save to the 'dimcli-qa-export-live' google sheet.", fg="green")
        click.secho("\nPS ignore the warnings deriving from Unittest & SSLSockets not being closed", fg="green")
        # ----
        d = Dsl()
        data = d.query("""search publications for "neurolink" return publications[id+title+doi+date+unnest(concepts)]""")
        data.save_gsheets(title='dimcli-qa-export-live', verbose=True)
        click.secho("Completed test succesfully", fg="green")
        



if __name__ == "__main__":
    unittest.main()
