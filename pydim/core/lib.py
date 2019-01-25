import requests
import click
import os
import json


class DimensionsClient(object):
    """
    Base class.
    Args:
        *args (list): list of arguments
        **kwargs (dict): dict of keyword arguments
    Attributes:
        self

    INTRO: http://docs.dimensions.ai/dsl/1.6.0/api.html
    FIELDS: http://docs.dimensions.ai/dsl/1.6.0/data.html#data
    ESCAPING RULES: http://docs.dimensions.ai/dsl/1.6.0/api.html#frequently-asked-questions

    """

    _redirect_url = "https://scigraph.springernature.com/api/redirect"
    _default_headers = {"Accept": "application/rdf+xml"}

    def __init__(self, *args, **kwargs):
        allowed_keys = ["verbose", "usr", "psw", "service"]
        self.__dict__.update((k, False) for k in allowed_keys)
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

        self.AUTH_URL = self.service + "auth.json"
        self.QUERY_URL = self.service + "dsl.json"
        LOGIN = {"username": self.usr, "password": self.psw}

        #   Send credentials to login url to retrieve token. Raise
        #   an error, if the return code indicates a problem.
        #   Please use the URL of the system you'd like to access the API
        #   in the example below.
        resp = requests.post(self.AUTH_URL, json=LOGIN)
        resp.raise_for_status()
        #   Create http header using the generated token.
        self.headers = {"Authorization": "JWT " + resp.json()["token"]}

    def query(self, q):
        """
        Execute DSL query. EG

        search publications for "malaria"
        where (year<=1980 or year in [2005:2010])
                and research_orgs.name~"Africa"
                return publications[basics + extras] sort by date limit 5 skip 10
            return in "facets"
            funders[name + country_name] as "entity_funder"
            return in "facets" research_orgs[all]
            aggregate rcr_avg, altmetric_median sort by rcr_avg
                    limit 3

        """
        #   Execute DSL query.
        resp = requests.post(self.QUERY_URL, data=q, headers=self.headers)
        return resp.json()

    def search_doi_issn(self, doi="", issn=""):
        if doi:
            q = (
                'search publications where doi="%s" return publications' % doi
            )  # eg 10.1038/205425a0
            print(q)
            return self.query(q)
        if issn:
            q = 'search publications where issn="%s" return publications' % issn
            return self.query(q)
