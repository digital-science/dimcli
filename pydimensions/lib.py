import requests
import click
import os
import json


def get_init():
    """
    Get init details. These have to be manually added in a file in the home folder: '~/.pydimensions.config.json'
    
    This is the structure:

    {
        "usr": "spam",
        "psw" : "spam", 
        "service" : "https://app.dimensions.ai/api/"   # optional
    }
    
    """
    DEFAULT_SERVICE = 'https://app.dimensions.ai/api/'
    user_config_dir = os.path.expanduser("~") + "/.pydimensions.config.json"
    try:
        with open(user_config_dir) as f:
            data = json.load(f)
    except:
        return None

    if data:
        try:
            usr = data['usr']
            psw = data['psw']
        except:
            return None
        try:
            service = c.get('service')
        except:
            service = DEFAULT_SERVICE
        return {'usr': usr, 'psw': psw, 'service': service}
    else:
        return None


class DimensionsClient(object):
    """
    Base class.
    Args:
        *args (list): list of arguments
        **kwargs (dict): dict of keyword arguments
    Attributes:
        self
    """
    _redirect_url = 'https://scigraph.springernature.com/api/redirect'
    _default_headers = {'Accept': 'application/rdf+xml'}

    def __init__(self, *args, **kwargs):
        allowed_keys = ['verbose', 'usr', 'psw', 'service']
        self.__dict__.update((k, False) for k in allowed_keys)
        self.__dict__.update(
            (k, v) for k, v in kwargs.items() if k in allowed_keys)

        self.AUTH_URL = self.service + 'auth.json'
        self.QUERY_URL = self.service + 'dsl.json'
        LOGIN = {'username': self.usr, 'password': self.psw}

        #   Send credentials to login url to retrieve token. Raise
        #   an error, if the return code indicates a problem.
        #   Please use the URL of the system you'd like to access the API
        #   in the example below.
        resp = requests.post(self.AUTH_URL, json=LOGIN)
        resp.raise_for_status()
        #   Create http header using the generated token.
        self.headers = {'Authorization': "JWT " + resp.json()['token']}

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
        resp = requests.post(
            self.QUERY_URL,
            data='search publications return FOR',
            headers=self.headers)
        return resp.json()
