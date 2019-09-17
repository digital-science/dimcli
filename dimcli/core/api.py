import configparser
import requests
import os.path
import os
import time
import json
import click
import IPython.display
from itertools import islice

import pandas as pd
from pandas.io.json import json_normalize

from .auth import do_global_login, get_connection, refresh_login
from .utils import line_search_return
from .walkup import *
from .dsl_grammar import G
from .dataframe_factory import DfFactory



class Dsl():
    """
    Object for abstracting common interaction steps with the Dimensions API. 
    Most often you just want to instantiate, authenticate and query() - yeah!

    >>> import dimcli
    # if you have set up a credentials file, no need to pass log in details
    >>> dsl = dimcli.Dsl()
    # you can also pass them explicitly
    >>> dsl = dimcli.Dsl(user="me@mail.com", password="secret")
    # queries always return a Result object (subclassing IPython.display.JSON)
    >>> dsl.query("search grants for \"malaria\" return researchers")
    >>> <dimcli.dimensions.Result object>
    # use the .json method to get the JSON
    >>> dsl.query("search grants for \"malaria\" return researchers").json
    >>> {'researchers': [{'id': 'ur.01332073522.49',
            'count': 75,
            'last_name': 'White',
            'first_name': 'Nicholas J'},
        "... JSON data continues ... "

    """
    def __init__(self, instance="live", user="", password="", endpoint="https://app.dimensions.ai", show_results=False):
        # print(os.getcwd())
        self._show_results = show_results
        self._url = None
        self._headers = None
        self.CONNECTION = get_connection()

        if self.CONNECTION['token']:
            # if already logged in, reuse connection          
            self._url = self.CONNECTION['url']
            self._headers = {'Authorization': "JWT " + self.CONNECTION['token']}
        elif user and password:
            print("Warning: this log in method is DEPRECATED - please use `dimcli.login(username, password)` instead. ")
            self.login(instance, user, password, endpoint)
        else:
            self.print_please_login()

    def login(self, instance="live", username="", password="", url="https://app.dimensions.ai"):
        """DEPRECATED METHOD - please use `dimcli.login()` instead """
        do_global_login(instance, username, password, url)
        self.CONNECTION = get_connection()
        self._url = self.CONNECTION['url']
        self._headers = {'Authorization': "JWT " + self.CONNECTION['token']}

    @property
    def is_logged_in(self):
        if self._url and  self._headers: return True
        else: return False

    def print_please_login(self):
        print("Warning: you are not logged in. Please use `dimcli.login(username, password)` before querying.")

    def query(self, q, show_results=None, retry=0):
        """
        Execute a DSL query.
        By default it doesn't show results, but it uses the iPython rich widgets for it, optimized for Jupyter Notebooks.
        """
        if not self.is_logged_in:
            self.print_please_login()
            return False
        
        #   Execute DSL query.
        response = requests.post(
            '{}/api/dsl.json'.format(self._url), data=q.encode(), headers=self._headers)
        if response.status_code == 429:  
            # Too Many Requests
            print(
                'Too Many Requests for the Server. Sleeping for 30 seconds and then retrying.'
            )
            time.sleep(30)
            return self.query(q)
        elif response.status_code == 403:  
            # Forbidden:
            print('Login token expired. Logging in again.')
            refresh_login()
            self.CONNECTION = get_connection()
            self._url = self.CONNECTION['url']
            self._headers = {'Authorization': "JWT " + self.CONNECTION['token']}
            return self.query(q)
        elif response.status_code in [200, 400, 500]:  
            ###  
            # OK or Error Info :-)
            ###
            try:
                res_json = response.json()
            except:
                print('Unexpected error. JSON could not be parsed.')
                return response
            result = Result(res_json)
            if show_results or (show_results is None and self._show_results):
                IPython.display.display(result)
            return result
        else:
            if retry > 0:
                print('Retrying in 30 secs')
                time.sleep(30)
                return self.query(
                    q,
                    retry=retry - 1)
            else:
                response.raise_for_status()



    def query_iterative(self, q, show_results=None, skip=0, limit=1000):
        """
        Runs a normal query iteratively, by automatically turning it into a loop with limit/skip operators until all the results available have been extracted. 
        """
        if not self.is_logged_in:
            self.print_please_login()
            return False

        # @TODO is there a hard limit of 50k results for limit/skip? can we catch it?
        if q.split().count('return') != 1:
            raise Exception("Loop queries support only 1 return statement")
        if "limit" in q or "skip" in q:
            raise Exception("Loop queries should not contain the keywords `limit` or `skip`")
        sourcetype = line_search_return(q)  
        if not (sourcetype in G.sources()):
            raise Exception("Loop queries can return only one of the Dimensions sources: %s" % ", ".join([s for s in G.sources()])) 
        
        output = []
        q2 = q + " limit %d skip %d" % (limit, skip)
        
        res = self.query(q2, show_results=False, retry=0)

        if res['errors']:
            return res
        elif res['stats']:

            tot = int(res['stats']['total_count'])
            batch = skip+limit
            if batch > tot:
                batch = tot
            print("%d / %d" % (batch, tot  ))

            if len(res[sourcetype]) == limit:
                output = res[sourcetype] + self.query_iterative(q, show_results, skip+limit)
            else:
                output = res[sourcetype]

            # FINALLY 
            #
            # if recursion is complete (we are at top level, hence skip=0) 
            #   build the Result obj
            # else 
            #   just return current iteration results 
            #
            if skip == 0: 
                response_simulation = {
                    "_stats": {
                        "total_count": tot
                        },
                    sourcetype: output
                }
                result = Result(response_simulation)
                if show_results or (show_results is None and self._show_results):
                    IPython.display.display(result)
                return result
            else:
                return output


    def __repr__(self):
        return f"<dimcli.Dsl #{id(self)}. API endpoint: {self._url}>"



        

class Result(IPython.display.JSON):
    """
    Wrapper for JSON results from DSL

    >>> res = dsl.query("search publications return publications")
    >>> res.data # => shows the underlying JSON data
    >>> res.json # => same 

    # Magic methods: 

    >>> res['publications'] # => the dict section
    >>> res['xxx'] # => false, not found
    >>> res['stats'] # => the _stats dict

    """
    def __init__(self, data):
        IPython.display.JSON.__init__(self, data)
        self.json = self.data
        for k in self.json.keys(): # add result dict keys as attributes dynamically
            if k == "_stats":
                setattr(self, "stats", self.json[k])
            else:
                setattr(self, k, self.json[k])

        self.df_factory = DfFactory(good_data_keys=self.good_data_keys())

    def __getitem__(self, key):
        "return dict key as slice"
        if key == "stats":
            key = "_stats" # syntactic sugar
        if key in self.json:
            return self.json[key]
        else:
            return [] # empty list so to support iteration tests / previously: False

    def __len__(self):
        "Return length of first object in JSON (skipping '_stats'"
        k = self.good_data_keys()
        try:
            return len(self.json[k[0]])
        except:
            return 0

    def good_data_keys(self,):
        "return the results keys other than stats"
        skips = ["_warnings", "_stats"]
        return [x for x in self.json.keys() if x not in skips]

    def keys_and_count(self,):
        "Utility to preview contents of results object"
        return [(x, len(self.json[x])) for x in self.json.keys()]

    @property
    def total_count(self,):
        "Quickly return tot count for query (not for current payload)"
        if self.json.get("_stats"):
            return self.json['_stats']['total_count']
        else:
            return None

    @property
    def errors_string(self,):  # can't be called 'error' due to conflict with auto-set field
        "Quickly return errors string"
        if self.json.get("errors"):
            return self.json['errors']['query']['header'] + self.json['errors']['query']['details'][0]
        else:
            return None

    def chunks(self, size=400, key=""):
        """
        Return an iterator for going through chunks of the JSON results. 
        NB the first available dict key is taken, to determine what is the data 
        object being returned. 
        Default size of chunks = 400 elements

        EG

        res = dslquery("search publications return publications limit 1000")
        test = [len(x) for x in res.chunks()]

        """

        if not key:
            if len(self.good_data_keys()) > 1:
                print(f"Please specify a key from {self.good_data_keys()}")
                return
            else:
                key = self.good_data_keys()[0]
        elif key not in self.good_data_keys():
            print(f"Invalid key: should be one of {self.good_data_keys()}")
            return 

        it = iter(self.json[key])
        chunk = list(islice(it, size))
        while chunk:
            yield chunk
            chunk = list(islice(it, size))

    # Dataframe Methods 

    def as_dataframe(self, key=""):
        "utility method: return inner json as a pandas dataframe"

        return self.df_factory.df_simple(self.json, key)


    def as_dataframe_authors(self):
        """Utility method: return inner json as a pandas dataframe, exposing authors + pubId
            Note: affiliations are not broken down. So one gets one row per author
        """

        return self.df_factory.df_authors(self.json)


    def as_dataframe_authors_affiliations(self):
        """Utility method: return inner json as a pandas dataframe, exposing authors + affiliations + pubId
        Affiliations ARE broken down and are returned as JSON - So one gets one row per affiliation (+1 row per author if having more than one affiliation)
        """
        
        return self.df_factory.df_authors_affiliations(self.json)


    def as_dataframe_funders(self):
        """Utility method: return inner json as a pandas dataframe, for grants funders
        """
        return self.df_factory.df_grant_funders(self.json)

    def as_dataframe_investigators(self):
        """Utility method: return inner json as a pandas dataframe, for grants funders
        """
        return self.df_factory.df_grant_investigators(self.json)

    def __repr__(self):
        return "<dimcli.Result object #%s. Dict keys: %s>" % (str(id(self)), ", ".join([f"'{x}'" for x in self.json]))







class DataframeWrapper(object):
    """
    Wrapper for a dataframe representation of the results
    """
    def __init__(self, data):
        sef.__init__(self, data)

    def as_dataframe(self, key=""):
        "utility method: return inner json as a pandas dataframe"

        output = pd.DataFrame()
        
        if key and (key in self.good_data_keys()):
            output = output.from_dict(self.json[key])
        elif key and (key not in self.good_data_keys()):
            print(f"Warning: Dataframe cannot be created: invalid key. Should be one of {self.good_data_keys()}")
        elif not key and self.good_data_keys():
            if len(self.good_data_keys()) > 1:
                print(f"Warning: Dataframe created from first available key, but more than one JSON key found: {self.good_data_keys()}")
            key = self.good_data_keys()[0]
            output = output.from_dict(self.json[key])
        else:
            pass 

        return output



    def __repr__(self):
        return "<dimcli.Result object #%s. Dict keys: %s>" % (str(id(self)), ", ".join([f"'{x}'" for x in self.json]))



