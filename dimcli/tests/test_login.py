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
        click.secho("\nTEST 001: load Dimcli using file-based credentials and verbose mode", fg="green")
        # ----
        print("Login... verbose=True")
        login()
        d = Dsl()
        res = d.query("search publications where year=2018 return publications")
        print("Query BATCH results: ", res.count_batch)
        print("Logout... verbose=True")
        logout()
        # ----
        print("Login... verbose=False")
        login(verbose=False)
        d = Dsl()
        res = d.query("search publications where year=2018 return publications")
        print("Query BATCH results: ", res.count_batch)
        print("Logout... verbose=False")
        logout()
        # ----
        click.secho("Completed test succesfully", fg="green")

    def test_002(self):
        click.secho("\nTEST 002: load Dimcli by passing credentials explicitly.", fg="green")
        # ----
        # get credentials from file as strings
        config = configparser.ConfigParser()
        config.read(os.path.expanduser(USER_CONFIG_FILE_PATH))
        section = config['instance.live' ]
        USER = section['login']
        PSW = section['password']
        login(USER, PSW)
        d = Dsl()
        res = d.query("search publications where year=2018 return publications")
        # print("Query results: ", res.keys_and_count())
        # ----
        logout()
        click.secho("\n--------\nCompleted test succesfully", fg="green")

    def test_002_1(self):
        click.secho("\nTEST 002-1: Retain login info and force new login.", fg="green")
        # ----
        login(instance="live")
        d = Dsl()
        print(""" Dsl(instance="live"): ==> url=""", d._url)
        res = d.query("""search publications where authors="Pasin" return publications""")
        print(" ==> res.json.keys(): ", res.json.keys())
        logout()
        login(instance="test")
        d = Dsl()
        print(""" d.login(instance="test"): ==> url=""", d._url)
        res = d.query("""search publications where authors="Pasin" return publications""")
        print(" ==> res.json.keys(): ", res.json.keys())
        logout()
        # ----
        click.secho("\n--------\nCompleted test succesfully", fg="green")


    def test_003(self):
        click.secho("\nTEST 003: Login using key-based authentication.", fg="green")
        # ----
        logout()
        login(instance="key-test")
        d = Dsl()
        print(""" Dsl(instance="key-test"): ==> url=""", d._url)
        res = d.query("""search publications where authors="Pasin" return publications""")
        print(" ==> res.json.keys(): ", res.json.keys())
        logout()
        # ----
        click.secho("\n--------\nCompleted test succesfully", fg="green")


if __name__ == "__main__":
    unittest.main()
