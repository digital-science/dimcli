#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
simple test queries [for DEVELOPMENT  / not part of official tests]

$ pip install -e .
$ dimcli_quicktest 1

"""

import click 
import os
import requests

from .. import *
from ..utils import *
from ..utils.converters import *
from ..utils.gists_utils import *
from .settings import API_INSTANCE


@click.command()
@click.argument('test_number', nargs=1)
def main(test_number=1):
    
    login(instance="live")
    dsl = Dsl()
    test_number = int(test_number)

    if test_number == 5:

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





    if test_number == 4:

        _q = """ search {} for "Albert Einstein" return {}[basics] limit 10 """

        for source in G.sources():
            q = _q.format(source, source)
            print(q)
            data = dsl.query(q)


    if test_number == 3:
        # testing magics 
        from IPython.testing.globalipapp import get_ipython
        ip = get_ipython()
        # ip.magic('load_ext excelify')
        # from dimcli.jupyter import magics
        from dimcli.jupyter.magics import DslMagics
        ip.register_magics(DslMagics)
        df = ip.run_cell_magic(magic_name='dsldf', line='', cell='search publications return publications')

        # mg = magics.DslMagics()

        # df = mg.dsldf(line="--links --nice", cell="""search publications return publications""")
        print(df)

    if test_number == 2:

        q = """
            search publications 
            for "scientometrics" 
            return publications[title+doi+year+journal+dimensions_url] 
            sort by times_cited"""

        df = dsl.query(q).as_dataframe(links=True)

        print(df)

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



