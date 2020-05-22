import configparser
import requests
import os.path
import os
import time
import json
import click
import IPython.display
from itertools import islice
import urllib.parse

import pandas as pd

from .auth import do_global_login, get_connection, refresh_login
from .utils import *
from .walkup import *
from .dsl_grammar import G
from .dataframe_factory import DfFactory



class Dsl():
    """
    Object for abstracting common interaction steps with the Dimensions API. 
    Most often you just want to instantiate and query() - yeah!

    >>> import dimcli
    # if you have already set up the credentials file (see above), no need to pass log in details
    >>> dimcli.login()
    # otherwise you can authenticate by passing your login details as arguments
    >>> dimcli.login(user="mary.poppins", password="chimneysweeper")
    # instantiate the query object
    >>> dsl = dimcli.Dsl()
    # queries always return a DslDataset object (subclassing IPython.display.JSON)
    >>> dsl.query("search grants for \"malaria\" return researchers")
    >>> <dimcli.dimensions.DslDataset object>
    # use the .json method to get the JSON
    >>> dsl.query("search grants for \"malaria\" return researchers").json
    >>> {'researchers': [{'id': 'ur.01332073522.49',
            'count': 75,
            'last_name': 'White',
            'first_name': 'Nicholas J'},
        "... JSON data continues ... "

    """
    def __init__(self, show_results=False, verbose=True):
        # print(os.getcwd())
        self._show_results = show_results
        self._verbose = verbose
        self._url = None
        self._headers = None
        self._CONNECTION = get_connection()

        if self._CONNECTION['token']:
            # if already logged in, reuse connection          
            self._url = self._CONNECTION['url']
            self._headers = {'Authorization': "JWT " + self._CONNECTION['token']}
        else:
            self._print_please_login()

    @property
    def is_logged_in(self):
        if self._url and  self._headers: return True
        else: return False

    def _print_please_login(self):
        print("Warning: you are not logged in. Please use `dimcli.login(username, password)` before querying.")

    def query(self, q, show_results=None, retry=0, verbose=None):
        """
        Execute a DSL query.
        By default it doesn't show results, but it uses the iPython rich widgets for it, optimized for Jupyter Notebooks.
        """
        if not self.is_logged_in:
            self._print_please_login()
            return False

        if verbose == None:
            verbose = self._verbose

        #   Execute DSL query.
        response = requests.post(
            '{}/api/dsl.json'.format(self._url), data=q.encode(), headers=self._headers)
        if response.status_code == 429:  
            # Too Many Requests
            print(
                'Too Many Requests for the Server. Sleeping for 30 seconds and then retrying.'
            )
            time.sleep(30)
            return self.query(q, show_results, retry, verbose)
        elif response.status_code == 403:  
            # Forbidden:
            print('Login token expired. Logging in again.')
            refresh_login()
            self._CONNECTION = get_connection()
            self._url = self._CONNECTION['url']
            self._headers = {'Authorization': "JWT " + self._CONNECTION['token']}
            return self.query(q, show_results, retry, verbose)
        elif response.status_code in [200, 400, 500]:  
            ###  
            # OK or Error Info :-)
            ###
            try:
                res_json = response.json()
            except:
                print('Unexpected error. JSON could not be parsed.')
                return response
            result = DslDataset(res_json)
            if verbose: print_json_stats(result, q)
            print_json_errors(result) # ALWAYS print errors
            if verbose: print_json_warnings(result)
            if show_results or (show_results is None and self._show_results):
                IPython.display.display(result)
            return result
        else:
            if retry > 0:
                print('Retrying in 30 secs')
                time.sleep(30)
                return self.query(
                    q,
                    show_results,
                    retry - 1, 
                    verbose)
            else:
                response.raise_for_status()



    def query_iterative(self, q, show_results=None, limit=1000, skip=0, pause=1.5, force=False, verbose=None, tot_count_prev_query=0):       
        """Runs a DSL query iteratively, by automatically turning it into a loop with limit/skip operators until all the results available have been extracted.
        
        Args:
            q (str): The DSL query.
            show_results (bool): Determines whether the final results are rendered via the iPython display widget (for Jupyter notebooks).
            limit (int): How many records to extract per iteration. Defaults to 1000.
            skip (int): Offset for first iteration. Defaults to 0. After the first iteration, this value is calculated dynamically.
            pause (float): How much time to pause after each iterarion, expressed in seconds. Defaults to 1.5. Note: each iteration gets timed, so the pause time is used only when the query time is more than 2s. 
            verbose (bool): Verbose mode.

        
        Returns:
            DslDataset -- query results collated within a single object 
        """
        if not self.is_logged_in:
            self._print_please_login()
            return False

        if verbose == None:
            verbose = self._verbose

        if q.split().count('return') != 1:
            raise Exception("Iterative queries support only 1 return statement")
        if line_has_limit_or_skip(q):
            raise Exception("Iterative queries should not contain the keywords `limit` or `skip`")
        sourcetype = line_search_return(q)  
        if not (sourcetype in G.sources()):
            raise Exception("Iterative queries can return only one of the Dimensions sources: %s" % ", ".join([s for s in G.sources()])) 
        #
        # ensure we stop the loop at 50k **
        #
        MAXLIMIT = 50000
        flag_last_round = False
        if skip + limit >= MAXLIMIT:
            flag_last_round = True
            if skip + limit > MAXLIMIT:
                limit = MAXLIMIT - skip


        if not tot_count_prev_query:
            # first iteration
            if verbose: print(f"{limit+skip} / ...")
            
        output, flag_force = [], False
        q2 = q + " limit %d skip %d" % (limit, skip)
        
        start = time.time()
        res = self.query(q2, show_results=False, retry=0, verbose=False)
        end = time.time()
        # print(end - start)
        if (end - start) < 2:
            # print("sleeping")
            time.sleep(pause)

        if res['errors'] and not force:
            print(f"\n>>>[Dimcli tip] An error occurred with the batch '{skip}-{limit+skip}'. Consider using the 'limit' argument to retrieve fewer records per iteration, or use 'force=True' to ignore errors and continue the extraction.")
            return res
        elif res['errors'] and force:
            print(f"\n>>>[Dimcli log] An error occurred with the batch '{skip}-{limit+skip}'. Skipping this batch and continuing iteration.. ")
            flag_force = True

        # RECURSION 

        try:
            tot = int(res['stats']['total_count'])
        except:
            tot =  tot_count_prev_query # when force=True, we have no current query stats

        new_skip = skip+limit
        if tot > 0 and new_skip > tot:
            new_skip = tot
        if verbose and tot:  # if not first iteration
            print(f"{new_skip} / {tot}")

        if flag_force:
            output = self.query_iterative(q, show_results, limit, new_skip, pause, force, verbose, tot_count_prev_query)                    

        elif len(res[sourcetype]) == limit and not flag_last_round:
            output = res[sourcetype] + self.query_iterative(q, show_results, limit, new_skip, pause, force, verbose, tot)

        else:
            output = res[sourcetype]

        # FINALLY 
        #
        # if recursion is complete (we are at top level, hence skip=0) 
        #   build the DslDataset obj
        # else 
        #   just return current iteration results 
        #
        if skip == 0: 
            response_simulation = {
                "_stats": {
                    "total_count": tot or len(output)  # fallback..
                    },
                sourcetype: output
            }
            result = DslDataset(response_simulation)
            if show_results or (show_results is None and self._show_results):
                IPython.display.display(result)
            if verbose: print(f"===\nRecords extracted: {len(output)}")
            return result
        else:
            return output


    def __repr__(self):
        return f"<dimcli.Dsl #{id(self)}. API endpoint: {self._url}>"



        

class DslDataset(IPython.display.JSON):
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

    # class methods to build DslDataset object from raw data (obtained not from a query eg from multiple queries concatenated)
    # these allow to then take advantage of other functionalities in DslDataset objects eg dataframes etc...
    @classmethod
    def from_publications_list(cls, data):
        return cls.from_any_list(data, "publications")
    @classmethod
    def from_grants_list(cls, data):
        return cls.from_any_list(data, "grants")
    @classmethod
    def from_researchers_list(cls, data):
        return cls.from_any_list(data, "researchers")
    @classmethod
    def from_clinical_trials_list(cls, data):
        return cls.from_any_list(data, "clinical_trials")
    @classmethod
    def from_patents_list(cls, data):
        return cls.from_any_list(data, "patents")
    @classmethod
    def from_policy_documents_list(cls, data):
        return cls.from_any_list(data, "policy_documents")
    @classmethod
    def from_organizations_list(cls, data):
        return cls.from_any_list(data, "organizations")
    @classmethod
    def from_any_list(cls, data, source_type):
        "Generic method used by all the ones above"
        if type(data) == list:
            return cls({source_type : data, '_stats' : {'total_count' : len(data)}})
        elif type(data) == pd.DataFrame:
            jsondata = json.loads(data.to_json(orient="records"))
            return cls({source_type : jsondata, '_stats' : {'total_count' : len(jsondata)}})
        else:
            raise ValueError('Invalid data format. Must be either a dict list, or a pandas dataframe')



    def __init__(self, data):
        IPython.display.JSON.__init__(self, data)
        self.json = self.data
        self.errors = None
        for k in self.json.keys(): # add result dict keys as attributes dynamically
            if k == "_stats":
                setattr(self, "stats", self.json[k])
            else:
                setattr(self, k, self.json[k])

        self.df_factory = DfFactory(good_data_keys=self.good_data_keys())

    def __getitem__(self, key):
        "Trick to return any dict key as a property"
        # print(key, "==========")
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
        skips = ["_warnings", "_notes", "_stats", "_version"]
        return [x for x in self.json.keys() if x not in skips]

    def keys_and_count(self,):
        "Utility to preview contents of results object"
        return [(x, len(self.json[x])) for x in self.json.keys()]

    @property
    def count_total(self,):
        "Quickly return tot count for query (not for current payload)"
        if self.json.get("_stats"):
            return self.json['_stats']['total_count']
        else:
            return None

    @property
    def count_batch(self,):
        "Quickly return tot count for current batch from query"
        return len(self)

    @property
    def errors_string(self,):  # can't be called 'error' due to conflict with auto-set field
        "Quickly return errors string"
        if self.json.get("errors"):
            return self.json['errors']['query']['header'] + self.json['errors']['query']['details'][0]
        else:
            return ""

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

        if not self.json.get("errors"):
            return self.df_factory.df_simple(self.json, key)


    def as_dataframe_authors(self):
        """Utility method: return inner json as a pandas dataframe, exposing authors + pubId
            Note: affiliations are not broken down. So one gets one row per author
        """
        if not self.json.get("errors"):
            return self.df_factory.df_authors(self.json)


    def as_dataframe_authors_affiliations(self):
        """Utility method: return inner json as a pandas dataframe, exposing authors + affiliations + pubId
        Affiliations ARE broken down and are returned as JSON - So one gets one row per affiliation (+1 row per author if having more than one affiliation)
        """
        if not self.json.get("errors"):
            return self.df_factory.df_authors_affiliations(self.json)

    def as_dataframe_concepts(self, key=""):
        """Utility method: return inner concepts list as a pandas dataframe, including several metrics for working with concepts.

        :param key: the JSON data key including concept information. If key is empty, the first available JSON key (eg 'publications') is used to build the dataframe

        The resulting dataframe has extra columns for ranking concepts:
        1) `concepts_count`: an integer representing the total number of concepts per document.
        2) `rank`: an integer representing the ranking of the concept within the list of concepts for a single document. E.g., the first concept has rank=1, while the fifth has rank=5.
        3) `score`: a float representing the importance of the concept in within a document. This is obtained by  normalizing its ranking against the total number of concepts for a single document (eg publication or grant). So if a document has 10 concepts in total, the first concept gets a score=1, the second score=0.9, etc..
        4) `frequency`: an integer representing how often that concept occurs within the full results-set returned by a query, i.e. how many documents have that concept name. So if a concept appears in 5 documents, frequency=5.
        5) `rank_avg`: the average (mean) value of all ranks for a single concept, across the full set of documents returned by the query. 
        6) `score_avg`: the average (mean) value of all scores for a single concept, across the full set of documents returned by a query.  
        7) `score_sum`: the sum of all scores for a single concept, across the full set of documents returned by a query.  
        """
        if not self.json.get("errors"):
            return self.df_factory.df_concepts(self.json, key)


    def as_dataframe_funders(self):
        """Utility method: return inner json as a pandas dataframe, for grants funders
        """
        if not self.json.get("errors"):
            return self.df_factory.df_grant_funders(self.json)

    def as_dataframe_investigators(self):
        """Utility method: return inner json as a pandas dataframe, for grants funders
        """
        if not self.json.get("errors"):
            return self.df_factory.df_grant_investigators(self.json)

    def as_dimensions_url(self, max=500, verbose=True):
        """Generates a valid Dimensions search URL using all the object IDs as filters.
        NOTE: this is EXPERIMENTAL and may break or be removed in future versions. 
        Also, doesn't work with all sources. 

        <max> 500 cause to prevent error 414 Request-URI Too Large 
        <verbose> to print out the warning

        General query structure for IDs: 
           
        `id: (pub.1120715293 OR pub.1120975084 OR pub.1122068834 OR pub.1120602308)`

        Final URL looks like this https://app.dimensions.ai/discover/publication?search_text=id%3A+%28pub.1120715293+OR+pub.1120975084+OR+pub.1122068834+OR+pub.1120602308%29

        """
        
        if verbose: print("Warning: this is an experimental and unsupported feature.")

        # hardcoded
        supported_url_templates = {
            'publications' : "https://app.dimensions.ai/discover/publication?search_text=",
            'grants' : "https://app.dimensions.ai/discover/grant?search_text=",
            'patents' : "https://app.dimensions.ai/discover/patent?search_text=",
            'clinical_trials' : "https://app.dimensions.ai/discover/clinical_trial?search_text=",
            'policy_documents' : "https://app.dimensions.ai/discover/policy_document?search_text=",
        }

        # just return first valid source found in results
        ids = []
        for sourcetype in supported_url_templates:
            if sourcetype in self.good_data_keys():
                try:
                    ids = [x['id'] for x in self.json[sourcetype]]
                    q = " OR ".join(ids)
                    if sourcetype == "grants":
                        q =  "grant_id: (" + q + ")"
                    else:
                        q =  "id: (" + q + ")"
                    q =  urllib.parse.quote_plus(q)
                    return supported_url_templates[sourcetype] + q
                except:
                    raise Exception("DslDataset records do not contain a valid ID field.")
        return None


    def __repr__(self):
        if self.json.get("errors"):
            return "<dimcli.DslDataset object #%s. Errors: %d>" % (str(id(self)), len(self.json['errors']))
        else:
            try:
                return "<dimcli.DslDataset object #%s. Records: %d/%d>" % (str(id(self)), self.count_batch, self.count_total)
            except:
                # non-search queries
                return "<dimcli.DslDataset object #%s. Dict keys: %s>" % (str(id(self)), ", ".join([f"'{x}'" for x in self.json]))





# 2019-12-17: for backward compatibility
# remove once all notebooks code has been updated 
Result = DslDataset
Dataset = DslDataset