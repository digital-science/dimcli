# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli - DfConverter
"""

from __future__ import print_function

import unittest, os, sys, click
import configparser

from .. import *
from ..core.auth import USER_CONFIG_FILE_PATH
from ..core.utils import dimensions_url
from ..shortcuts import *

from ..core.converters import *


class TestRenderer(unittest.TestCase):

    """
    Tests  
    """

    click.secho("**TESTS**", fg="red")
    login(instance="live")
    d = Dsl()

    def test_001(self):
        click.secho("\nTEST 001: DfConverter.", fg="green")
        # ----
        q = "search publications for \"mercedes\" return publications"
        click.secho(q, fg="green")
        res = dslquery(q).as_dataframe()

        r = DfConverter(res)
        r.do()
        print(r.df)




if __name__ == "__main__":
    unittest.main()
