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

        covid_q = '"2019-nCoV" OR "COVID-19" OR "SARS-CoV-2" OR (("coronavirus"  OR "corona virus") AND (Wuhan OR China))'
        q = f"""search publications 
                in full_data for "{dsl_escape(covid_q)}" 
                where year=2020 
            return publications[id+doi+pmid+pmcid+title+journal+publisher+mesh_terms+date+year+volume+issue+pages+open_access+type+authors+research_orgs+funders+supporting_grant_ids+times_cited+altmetric+linkout] limit 1000"""

        q1 = """search publications for "malaria" return publications[id+authors]"""

        click.secho(q, fg="green")

        df = dslquery(q).as_dataframe()

        r = DfConverter(df, "publications")
        res = r.simplify_nested_objects()

        order = [   'Publication ID', 
                    'DOI',
                    'PMID',
                    'PMCID',
                    'Title',
                    'Abstract',
                    'Source title',
                    'Source UID',
                    'Publisher',
                    'MeSH terms',
                    'Publication Date',
                    'PubYear',
                    'Volume',
                    'Issue',
                    'Pagination',
                    'Open Access',
                    'Publication Type',
                    'Authors',
                    'Corresponding Author',
                    'Authors Affiliations',
                    'Research Organizations - standardized',
                    'GRID IDs',
                    'City of Research organization',
                    'Country of Research organization',
                    'Funder',
                    'UIDs of supporting grants',
                    'Times cited',
                    'Altmetric',
                    'Source Linkout',
                    'Dimensions URL']

        res = res[order]

        res.to_csv("test.csv", index=False)

    if test_number == 2:
        from dimcli.functions import extract_affiliations
        bad_data=[{'name': 'Universidad Central de Bayamon',
        'city': 'Bayamón',
        'state': 'Puerto Rico',
        'country': 'United States'}]
        print(extract_affiliations(bad_data))

    if test_number == 3:
        from dimcli.utils.repl_utils import export_gist
        q = "search publications return category_for limit 100"
        data = dsl.query(q)
        print(data.errors)

    if test_number == 4:
        q = "search publications return research_orgs limit 100"
        data = dsl.query(q, verbose=True)
        print(len(data))

    if test_number == 5:

        # TESTING LOCAL LOGIN LOGIC 

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
        
        mysession3 = APISession()
        mysession3.login(instance="live2")

        d3 = Dsl(auth_session=mysession3)
        click.secho(""" Dsl3(instance="liveV2"): ==> url="""+ d3._url, fg="magenta")
        res3 = d3.query("""search publications where authors="Pasin" return publications""")
        print(" ==> res.json.keys(): ", res3.json.keys())
        

    if test_number == 6:

        # TESTING RETRY LOGIC 

        logout()
        from ..core.auth import APISession
        
        mysession1 = APISession()
        mysession1.login(instance="key-test")

        d1 = Dsl(auth_session=mysession1)

        for x in range(1990, 2020):
            q = f"""search publications where year={x} return research_orgs"""
            d1.query(q)
            print(q)

        # logout()


if __name__ == '__main__':
    main()



