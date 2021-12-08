#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
simple test queries [for DEVELOPMENT  / not part of official tests]

$ pip instal -e .
$ dimcli_quicktest 1

"""

import click 
import os
import requests

from .. import *
from ..utils import *
from ..core.converters import *

from ..utils.gists_utils import *

from .settings import API_INSTANCE


@click.command()
@click.argument('test_number', nargs=1)
def main(test_number=1):
    
    login(instance="live")
    dsl = Dsl()
    test_number = int(test_number)

    if test_number == 1:

        logout()
        from ..core.auth import APISession


        mysession1 = APISession()
        mysession1.login(instance="live")

        d1 = Dsl(auth_session=mysession1)
        res1 = d1.query("""search publications where authors="Pasin" return publications""")
        print(" ==> res.json.keys(): ", res1.json.keys())

        mysession1.refresh_login()    
        print("Login refreshed")



if __name__ == '__main__':
    main()



