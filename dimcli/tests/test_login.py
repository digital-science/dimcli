# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli  - logins

python -m dimcli.tests.test_login

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

    click.secho("**test_login.py**", fg="red")

    def test_001(self):
        click.secho("\nTEST 001: GLOBAL login/logout using file-based credentials and verbose mode", bg="green")
        # ----
        
        click.secho("login()... without arguments", fg="magenta")
        login()
        d = Dsl()
        res = d.query("search publications where year=2018 return publications")
        print("Query BATCH results: ", res.count_batch)
        click.secho("Logout... verbose=True", fg="magenta")

        click.secho("\nTesting refresh-login method ..", fg="magenta")
        d._refresh_login()    
        click.secho("Login refreshed!")

        logout()
        # ----

        click.secho("login(instance=API_INSTANCE)", fg="magenta")
        login(instance=API_INSTANCE)
        d = Dsl()
        res = d.query("search publications where year=2018 return publications")
        print("Query BATCH results: ", res.count_batch)
        click.secho("Logout... verbose=True", fg="magenta")
        logout()
        # ----

        click.secho("login(instance=API_INSTANCE, verbose=False)", fg="magenta")
        login(instance=API_INSTANCE, verbose=False)
        d = Dsl()
        res = d.query("search publications where year=2018 return publications")
        print("Query BATCH results: ", res.count_batch)
        click.secho("Logout... verbose=False", fg="magenta")
        logout()
        # ----
        
        click.secho('''login(endpoint="https://runtime.dimensions.ai")''', fg="magenta")
        login(endpoint="https://runtime.dimensions.ai")
        d = Dsl()
        res = d.query("search publications where year=2018 return publications")
        print("Query BATCH results: ", res.count_batch)
        click.secho("Logout... verbose=True", fg="magenta")
        logout()
        # ----

        click.secho('''login(key="", endpoint="https://app.dimensions.ai")''', fg="magenta")
        login(key="", endpoint="https://app.dimensions.ai")
        d = Dsl()
        res = d.query("search publications where year=2018 return publications")
        print("Query BATCH results: ", res.count_batch)
        click.secho("Logout... verbose=True", fg="magenta")
        logout()
        # ----

        click.secho("\n--------\nCOMPLETED", fg="green")

    def test_002(self):
        click.secho("\nTEST 002: GLOBAL login/logout by passing credentials explicitly.", bg="green")
        # ----
        # get credentials from file as strings
        config = configparser.ConfigParser()
        config.read(os.path.expanduser(USER_CONFIG_FILE_PATH))
        section = config['instance.live' ]
        try:
            # 2021-03-18 / old method
            USER = section['login']
            PSW = section['password']
            login(USER, PSW)
        except:
            KEY = section['key']
            login(key=KEY)
        d = Dsl()
        res = d.query("search publications where year=2018 return publications")
        # print("Query results: ", res.keys_and_count())
        # ----
        logout()
        click.secho("\n--------\nCOMPLETED", fg="green")

    def test_002_1(self):
        click.secho("\nTEST 002-1: GLOBAL login/logout on different Dimension instances.", bg="green")
        # ----
        login(instance=API_INSTANCE)
        d = Dsl()
        click.secho(f""" Dsl(instance="{API_INSTANCE}"): ==> url=""" + d._url, fg="magenta")
        res = d.query("""search publications where authors="Pasin" return publications""")
        print(" ==> res.json.keys(): ", res.json.keys())
        logout()
        login(instance="runtime")
        d = Dsl()
        click.secho(""" d.login(instance="runtime"): ==> url=""" + d._url, fg="magenta")
        res = d.query("""search publications where authors="Pasin" return publications""")
        print(" ==> res.json.keys(): ", res.json.keys())
        logout()
        # ----
        click.secho("\n--------\nCOMPLETED", fg="green")


    def test_003(self):
        click.secho("\nTEST 003: GLOBAL login/logout using key-based authentication.", bg="green")
        # ----
        logout()
        login(instance="key-test")
        d = Dsl()
        click.secho(""" Dsl(instance="key-test"): ==> url="""+ d._url, fg="magenta")
        res = d.query("""search publications where authors="Pasin" return publications""")
        print(" ==> res.json.keys(): ", res.json.keys())
        logout()
        # ----
        click.secho("\n--------\nCOMPLETED", fg="green")


    def test_004(self):
        click.secho("\nTEST 004: LOCAL Login/logout using APISession object.", bg="green")
        # ----
        logout()
        from ..core.auth import APISession

        mysession1 = APISession()
        mysession1.login(instance="key-test")
        d1 = Dsl(auth_session=mysession1)
        click.secho(""" Dsl1(instance="key-test"): ==> url="""+ d1._url, fg="magenta")
        res1 = d1.query("""search publications where authors="Pasin" return publications""")
        print(" ==> res.json.keys(): ", res1.json.keys())
        
        mysession2 = APISession()
        mysession2.login(instance="live")
        d2 = Dsl(auth_session=mysession2)
        click.secho(""" Dsl2(instance="live"): ==> url="""+ d2._url, fg="magenta")
        res2 = d2.query("""search publications where authors="Pasin" return publications""")
        print(" ==> res.json.keys(): ", res2.json.keys())
        
        # ----
        click.secho("\n--------\nCOMPLETED", fg="green")


    def test_005(self):
        click.secho("\nTEST 005: GLOBAL login/logout using verify_ssl flag.", bg="green")
        # ----
        logout()
        login(instance="key-test", verify_ssl=True, verbose=True)
        d = Dsl()
        click.secho(""" Dsl(instance="key-test" / verify_ssl=True): ==> url="""+ d._url, fg="magenta")
        res = d.query("""search publications where authors="Pasin" return publications""")
        print(" ==> res.json.keys(): ", res.json.keys())
        logout()
        # ----
        click.secho("\n--------\nCOMPLETED", fg="green")







if __name__ == "__main__":
    unittest.main()
