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
from ..utils import *

from .settings import API_INSTANCE


class TestOne(unittest.TestCase):

    """
    Tests - export functions 
    """

    click.secho("**test_export.py**", fg="red")
    login(instance=API_INSTANCE)
    d = Dsl()


    def test_001(self):
        click.secho("\nTEST 001: Save to a JSON file and construct a dimcli.DslDataset objects from JSON file.", bg="green")
        # ----
        FILENAME = "test-api-save.json"
        d = Dsl()
        data = d.query_iterative("""search publications where journal.title="nature medicine" and year>2014 return publications[id+title+year+concepts]""")
        data.to_json_file(FILENAME, verbose=True)
        new_data = DslDataset.load_json_file(FILENAME, verbose=True)
        print(new_data)
        os.remove(FILENAME)
        print("Deleted:", FILENAME)
        click.secho("Completed test succesfully", fg="green")

        



if __name__ == "__main__":
    unittest.main()
