"""
Dimcli objects for querying the Dimensions API. 
NOTE: these objects are attached to the top level ``dimcli`` module. So you can load them as follows:

>>> import dimcli
>>> dsl = dimcli.Dsl()

"""


import requests
import time
import json
import IPython.display
from itertools import islice
import urllib.parse

import pandas as pd

from .auth import get_global_connection 
from .dsl_grammar import G
from .dataframe_factory import DfFactory

from ..utils.all import *



class Dsl():

    """The Dsl object is the main interface for interacting with the Dimensions API.

    Parameters
    ----------
    show_results : bool, default=False
        Set a global setting that determines whether query JSON results get printed out. Note that in Jupyter environments this is not needed, because iPython rich widgets are used by default.
    auth_session : APISession, default=False
        Set an authenticated session object that should be used for querying. Used only in special situations, as an alternative to the dimcli.login() utility method. 
    verbose : bool, default=True
        Verbose mode.

    Example
    -------
    >>> import dimcli
    >>> dimcli.login()
    >>> dsl = dimcli.Dsl()
    >>> dsl.query(\"\""search grants for "graphene" return researchers"\"\")
    <dimcli.dimensions.DslDataset object>
    >>> _.json
    >>> {'researchers': [{'id': 'ur.01332073522.49',
            'count': 75,
            'last_name': 'White',
            'first_name': 'Nicholas J'},
        "... JSON data continues ... "

    In some special situations, you'd want to query two separate Dimensions servers 
    in parallel. To that end, it is possible to pass an `APISession` instance to the `Dsl()` constructor
    using the `auth_session` parameter, IE:

    >>> import dimcli
    >>> from dimcli.core.auth import APISession 
    # set up first authentication backend
    >>> mysession1 = APISession()
    >>> mysession1.login(instance="app.dimensions.ai")
    >>> d1 = Dsl(auth_session=mysession1)
    >>> d1.query("search publications return research_orgs")
    # set up second authentication backend
    >>> mysession2 = APISession()
    >>> mysession2.login(instance="another-app.dimensions.ai")
    >>> d2 = Dsl(auth_session=mysession2)
    >>> d2.query("search publications return research_orgs")

    """

    def __init__(self, show_results=False, verbose=True, auth_session=False):
        """Initialises a Dsl object.

        """
        self._show_results = show_results
        self._verbose = verbose
        self._url = None
        self._headers = None
        self.verify_ssl = True
        if auth_session:
            self._CONNECTION = auth_session 
        else:
            self._CONNECTION = get_global_connection()

        if self._CONNECTION.token:
            # if already logged in, reuse connection          
            self._url = self._CONNECTION.url
            self._headers = {'Authorization': "JWT " + self._CONNECTION.token}
            self.verify_ssl = self._CONNECTION.verify_ssl
        else:
            self._print_please_login()

    @property
    def is_logged_in(self):
        if self._url and  self._headers: return True
        else: return False

    def _print_please_login(self):
        printDebug("Warning: you are not logged in. Please use `dimcli.login(key, endpoint)` before querying.")

    def _refresh_login(self):
        if self._CONNECTION:
            self._CONNECTION.refresh_login()
            self._url = self._CONNECTION.url
            self._headers = {'Authorization': "JWT " + self._CONNECTION.token}
            self.verify_ssl = self._CONNECTION.verify_ssl
        else:
            printDebug("Warning: please login first.")

    def query(self, q, show_results=None, retry=0, verbose=None):
        """Execute a single DSL query.

        This method handles the query token from the API and regenerates it if it's expired. If the API throws a 'Too Many Requests for the Server' error, the method sleeps 30 seconds before retrying.

        Parameters
        ----------
        show_results : bool, default=None
            Setting that determines whether the query JSON results should be printed out. If None, it inherits from the Dsl global setting. Note that in Jupyter environments this is not needed, because iPython rich widgets are used by default.
        retry : int, default=0
            Number of times to retry the query if it fails.
        verbose : bool, default=None
            Verbose mode. If None, it inherits from the Dsl global setting. 


        Returns
        -------
        DslDataset
            A Dimcli wrapper object containing JSON data. 

        Example
        -------------
        >>> dsl = dimcli.Dsl()
        >>> dsl.query("search grants where start_year=2020 return grants")
        <dimcli.dimensions.DslDataset object>

        """
        if not self.is_logged_in:
            self._print_please_login()
            return False

        if verbose == None:
            verbose = self._verbose
        
        #   Execute DSL query.
        start = time.time()
        response = requests.post(self._url, data=q.encode(), headers=self._headers, verify=self.verify_ssl)
        if response.status_code == 429:  
            # Too Many Requests
            printDebug(
                'Too Many Requests for the Server. Sleeping for 30 seconds and then retrying.'
            )
            time.sleep(30)
            return self.query(q, show_results, retry, verbose)
        elif response.status_code == 403:  
            # Forbidden:
            printDebug('Login token expired. Logging in again.')
            self._refresh_login()
            # self._CONNECTION.refresh_login()
            # self._url = self._CONNECTION.url
            # self._headers = {'Authorization': "JWT " + self._CONNECTION.token}
            return self.query(q, show_results, retry, verbose)
        elif response.status_code in [200, 400, 500]:  
            ###  
            # OK or Error Info :-)
            ###
            try:
                res_json = response.json()
            except:
                printDebug('Unexpected error. JSON could not be parsed.')
                return response
            result = DslDataset(res_json)
            end = time.time()
            elapsed = end - start
            if verbose: print_json_stats(result, q, elapsed)
            print_json_errors(result) # ALWAYS print errors
            if verbose: print_json_warnings(result) # DON'T print warnings unless verbose=True
            if show_results or (show_results is None and self._show_results):
                IPython.display.display(result)
            return result
        else:
            if retry > 0:
                printDebug('Retrying in 30 secs')
                time.sleep(30)
                return self.query(
                    q,
                    show_results,
                    retry - 1, 
                    verbose)
            else:
                if verbose: printDebug("ERROR LOG\n---\nQuery\n---\n" + str(q), "red")
                if verbose: printDebug("Response.header\n---\n" + str(response.headers), "red")
                if verbose: printDebug("Response.content\n---\n" +str(response.content), "red")
                response.raise_for_status()



    def query_iterative(self, q, show_results=None, limit=1000, skip=0, pause=1.5, force=False, maxlimit=0, verbose=None, _tot_count_prev_query=0, _warnings_tot=None):       
        """Runs a DSL query and then keep querying until all matching records have been extracted. 
        
        The API returns a maximum of 1000 records per call. If a DSL query results in more than 1000 matches, it is possible to use pagination to get more results. 
        
        Iterative querying works by automatically paginating through all records available for a result set. The original query gets turned into a loop that uses the `limit` / `skip` operators until all the results available have been extracted. 
        
        Parameters
        ----------
        q: str 
            The DSL query. Important: pagination keywords eg `limit` / `skip` should be omitted.
        show_results : bool, default=True
            Determines whether the final results are rendered via the iPython display widget (for Jupyter notebooks).
        limit : int, default=1000
            How many records to extract per iteration. Defaults to 1000.
        skip : int, default=0
            Offset for first iteration. Defaults to 0. After the first iteration, this value is calculated dynamically.
        pause : float, default=1.5s
            How much time to pause after each iterarion, expressed in seconds. Defaults to 1.5. Note: each iteration gets timed, so the pause time is used only when the query time is more than 2s. 
        force : bool, default=False
            Continue the extraction even if one of the iterations fails due to an error. 
        maxlimit : int, default=0
            The maximum number of records to extract in total. If 0, all available records are extracted, up to the API upper limit of 50k records per query.
        verbose : bool, default=False
            Verbose mode.


        Returns
        -------
        DslDataset
            A Dimcli wrapper object containing JSON data. 

        Example
        -------
        >>> dsl = dimcli.Dsl()
        >>> dsl.query_iterative(\"\""search grants where category_for.name="0206 Quantum Physics" return grants"\"\")
        Starting iteration with limit=1000 skip=0 ...
        0-1000 / 8163 (4.062144994735718s)
        1000-2000 / 8163 (1.5146172046661377s)
        2000-3000 / 8163 (1.7225260734558105s)
        3000-4000 / 8163 (1.575329065322876s)
        4000-5000 / 8163 (1.521540880203247s)
        5000-6000 / 8163 (1.471721887588501s)
        6000-7000 / 8163 (1.5068159103393555s)
        7000-8000 / 8163 (1.4724757671356201s)
        8000-8163 / 8163 (0.7611980438232422s)
        ===
        Records extracted: 8163


        Returns
        -------
        DslDataset
            A Dimcli wrapper object containing JSON data. 

        """
        if not self.is_logged_in:
            self._print_please_login()
            return False

        if verbose == None:
            verbose = self._verbose

        if line_count_returns(q) != 1:
            raise Exception("Iterative queries support only 1 return statement")
        if line_has_limit_or_skip(q):
            raise Exception("Iterative queries should not contain the keywords `limit` or `skip`")
        sourcetype = line_search_return(q)  
        if not (sourcetype in G.sources()):
            raise Exception("Iterative queries can return only one of the Dimensions sources: %s" % ", ".join([s for s in G.sources()])) 

        IS_UNNEST = line_search_unnest(q)
        #
        # ensure we stop the loop at 50k **
        #
        MAXLIMIT = maxlimit or 50000
        flag_last_round = False
        if skip + limit >= MAXLIMIT:
            flag_last_round = True
            if skip + limit > MAXLIMIT:
                limit = MAXLIMIT - skip


        if not _tot_count_prev_query:
            # first iteration
            # if verbose: printDebug(f"{limit+skip} / ...")
            if verbose: printDebug(f"Starting iteration with limit={limit} skip={skip} ...")
            
        output, flag_force = [], False
        q2 = q + " limit %d skip %d" % (limit, skip)
        
        start = time.time()
        res = self.query(q2, show_results=False, retry=0, verbose=False)
        end = time.time()
        elapsed = end - start

        if (end - start) < 2:
            # printDebug("sleeping")
            time.sleep(pause)

        if res['errors'] and not force:
            printDebug(f"\n>>>[Dimcli tip] An error occurred with the batch '{skip}-{limit+skip}'. Consider using the 'limit' argument to retrieve fewer records per iteration, or use 'force=True' to ignore errors and continue the extraction.")
            return res
        elif res['errors'] and force:
            printDebug(f"\n>>>[Dimcli log] An error occurred with the batch '{skip}-{limit+skip}'. Skipping this batch and continuing iteration.. ")
            flag_force = True

        # RECURSION 

        try:
            tot = int(res['stats']['total_count'])
        except:
            tot =  _tot_count_prev_query # when force=True, we have no current query stats

        new_skip = skip+limit
        if tot > 0 and new_skip > tot:
            new_skip = tot
        if verbose and tot:  # if not first iteration
            t = "%.2f" % elapsed
            printDebug(f"{skip}-{new_skip} / {tot} ({t}s)")

        if res["_warnings"]:
            if _warnings_tot:
                _warnings_tot += res["_warnings"]
            else:
                _warnings_tot = res["_warnings"]

        if flag_force:
            output = self.query_iterative(q, show_results, limit, new_skip, pause, force, maxlimit, verbose, _tot_count_prev_query, _warnings_tot)                    

        elif not IS_UNNEST and len(res[sourcetype]) == limit and not flag_last_round:
            output = res[sourcetype] + self.query_iterative(q, show_results, limit, new_skip, pause, force,maxlimit, verbose, tot, _warnings_tot)

        elif IS_UNNEST and len(res[sourcetype]) > 0 and not flag_last_round:
            # unnest returns a number of records that don't relate to actual data left
            # hence can't match the lenght of results to limit in this case
            output = res[sourcetype] + self.query_iterative(q, show_results, limit, new_skip, pause, force, maxlimit, verbose, tot, _warnings_tot)

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
            if _warnings_tot:
                response_simulation["_warnings"] = _warnings_tot
            result = DslDataset(response_simulation)
            if show_results or (show_results is None and self._show_results):
                IPython.display.display(result)
            if verbose: printDebug(f"===\nRecords extracted: {len(output)}")
            return result
        else:
            return output


    def __repr__(self):
        return f"<dimcli.Dsl #{id(self)}. API endpoint: {self._url}>"



        

class DslDataset(IPython.display.JSON):
    """Wrapper for JSON results from DSL.

    This object makes it easier to process, save and load API JSON data. 

    Example
    ----------
    >>> dsl = dimcli.Dsl()
    >>> data = dsl.query(\"\""search publications for "machine learning" return publications limit 100"\"\")
    Returned Publications: 20 (total = 2501114)
    Time: 1.36s
    >>> print(data)
    <dimcli.DslDataset object #4383191536. Records: 100/2501114>
    >>> len(data)
    100
    >>> data.count_batch
    100
    >>> data.count_total
    2501114
    >>> data.json
    #  => returns the underlying JSON data
    >>> data['publications'] 
    #  => shortcut for the 'publications' key in the underlying JSON data
    >>> data.publications
    #  => ..this is valid too!

    """

    @classmethod
    def from_publications_list(cls, data):
        """Utility method that allows to simulate an API results DslDataset object from raw publications data. 
        
        This functionality can be used to reload data that was cached locally, or to combine the merged results of separate API queries into a single DslDataset object. 

        Once created, the DslDataset object has the same exact behaviour as when it is obtained from an API query (so one can take advatange of dataframe creation methods, for example).

        Parameters
        ----------
        data: list or pandas dataframe 
            A list of publications, in the form of either a list of dictionaries, or as a pandas dataframe. 


        Returns
        -------
        DslDataset
            A Dimcli wrapper object containing JSON data. 

        Example
        ----------
        >>> dsl = dimcli.Dsl()
        >>> rawdata = dsl.query("search publications return publications").publications
        >>> type(rawdata)
        list
        >>> newDataset = dimcli.DslDataset.from_publications_list(rawdata)
        >>> newDataset
        <dimcli.DslDataset object #4767014816. Records: 20/20>
        """
        return cls._from_any_list(data, "publications")
    
    @classmethod
    def from_grants_list(cls, data):
        """Utility method that allows to simulate an API results DslDataset object from raw grants data. See the `from_publications_list` method for more information. 

        Parameters
        ----------
        data: list or pandas dataframe 
            A grants list (using the API DSL structure), in the form of either a list of dictionaries, or as a pandas dataframe. 

        Returns
        -------
        DslDataset
            A Dimcli wrapper object containing JSON data.         
        
        """
        return cls._from_any_list(data, "grants")
    
    @classmethod
    def from_researchers_list(cls, data):
        """Utility method that allows to simulate an API results DslDataset object from raw researchers data. See the `from_publications_list` method for more information. 

        Parameters
        ----------
        data: list or pandas dataframe 
            A researchers list (using the API DSL structure), in the form of either a list of dictionaries, or as a pandas dataframe. 

        Returns
        -------
        DslDataset
            A Dimcli wrapper object containing JSON data.         
        
        """
        return cls._from_any_list(data, "researchers")
    
    @classmethod
    def from_clinical_trials_list(cls, data):
        """Utility method that allows to simulate an API results DslDataset object from raw clinical_trials data. See the `from_publications_list` method for more information. 

        Parameters
        ----------
        data: list or pandas dataframe 
            A clinical_trials list (using the API DSL structure), in the form of either a list of dictionaries, or as a pandas dataframe. 

        Returns
        -------
        DslDataset
            A Dimcli wrapper object containing JSON data.         
        
        """
        return cls._from_any_list(data, "clinical_trials")
    
    @classmethod
    def from_patents_list(cls, data):
        """Utility method that allows to simulate an API results DslDataset object from raw patents data. See the `from_publications_list` method for more information. 

        Parameters
        ----------
        data: list or pandas dataframe 
            A patents list (using the API DSL structure), in the form of either a list of dictionaries, or as a pandas dataframe. 

        Returns
        -------
        DslDataset
            A Dimcli wrapper object containing JSON data.         
        
        """
        return cls._from_any_list(data, "patents")
    
    @classmethod
    def from_policy_documents_list(cls, data):
        """Utility method that allows to simulate an API results DslDataset object from raw policy_documents data. See the `from_publications_list` method for more information. 

        Parameters
        ----------
        data: list or pandas dataframe 
            A policy_documents list (using the API DSL structure), in the form of either a list of dictionaries, or as a pandas dataframe. 

        Returns
        -------
        DslDataset
            A Dimcli wrapper object containing JSON data.         
        
        """
        return cls._from_any_list(data, "policy_documents")
    
    @classmethod
    def from_organizations_list(cls, data):
        """Utility method that allows to simulate an API results DslDataset object from raw organizations data. See the `from_publications_list` method for more information. 

        Parameters
        ----------
        data: list or pandas dataframe 
            An organizations list (using the API DSL structure), in the form of either a list of dictionaries, or as a pandas dataframe. 

        Returns
        -------
        DslDataset
            A Dimcli wrapper object containing JSON data.         
        
        """
        return cls._from_any_list(data, "organizations")
    
    @classmethod
    def _from_any_list(cls, data, source_type):
        """Generic method that allows to simulate an API results DslDataset object from raw data.
        """
        if type(data) == list:
            return cls({source_type : data, '_stats' : {'total_count' : len(data)}})
        elif type(data) == pd.DataFrame:
            jsondata = json.loads(data.to_json(orient="records"))
            return cls({source_type : jsondata, '_stats' : {'total_count' : len(jsondata)}})
        else:
            raise ValueError('Invalid data format. Must be either a dict list, or a pandas dataframe')
    
    @classmethod
    def load_json_file(cls, filename, verbose=False):
        """Load a file containing DSL JSON data and returns a valid DslDataset object. 

        Note: this is normally used in combination with the `to_json_file` method.

        Parameters
        ----------
        filename: str 
            A valid filename (including path if necessary) that contains the JSON data.

        Returns
        -------
        DslDataset
            A Dimcli wrapper object containing JSON data.         

        Example
        -------
        Save the results of a query to a JSON file, then reload the same file and create a new dataset.

        >>> dataset = dsl.query(\"\""search publications where journal.title="nature medicine" return publications[id+title+year+concepts] limit 100"\"\")
        Returned Publications: 100 (total = 12641)

        Save the data to a local json file

        >>> FILENAME = "test-api-save.json"
        >>> dataset.to_json_file(FILENAME, verbose=True)
        Saved to file:  test-api-save.json
        
        Create a new DslDataset object by loading the contents of the JSON file.

        >>> new_dataset = DslDataset.load_json_file(FILENAME, verbose=True)
        Loaded file:  test-api-save.json
        >>> print(new_dataset)
        <dimcli.DslDataset object #4370267824. Records: 100/12641>

        """
        with open(filename) as json_file:
            jsondata = json.load(json_file)
        if verbose: printDebug("Loaded file: ", filename)
        return cls(jsondata)


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
        # printDebug(key, "==========")
        if key == "stats":
            key = "_stats" # syntactic sugar
        if key in self.json:
            return self.json[key]
        else:
            return [] # empty list so to support iteration tests / previously: False

    def __len__(self):
        "Return length of first object in JSON"
        k = self.good_data_keys()
        try:
            return len(self.json[k[0]])
        except:
            return 0

    def good_data_keys(self,):
        """Utility that returns the 'data' keys of the inner JSON object, excluding metadata like 'stats', 'warnings' and 'version' info. 

        Returns
        -------
        list
            A list of dictionary keys.         

        Example
        -------
        >>> queryresults.good_data_keys()
        ['publications']

        """
        skips = ["_warnings", "_notes", "_stats", "_version", "_copyright"]
        return [x for x in self.json.keys() if x not in skips]

    def keys_and_count(self,):
        """Utility that previews the contents of the inner JSON object. 

        Returns
        -------
        list
            A list of tuples.       

        Example
        -------
        >>> queryresults.keys_and_count()
        [('_stats', 3), ('_warnings', 1), ('_version', 2), ('publications', 100)]

        """
        return [(x, len(self.json[x])) for x in self.json.keys()]

    @property
    def count_total(self,):
        """Total number of results in Dimensions for the query (as opposed to the results returned in the JSON payload). 

        Returns
        -------
        int
            The number of results
        """
        if self.json.get("_stats"):
            return self.json['_stats']['total_count']
        else:
            return None

    @property
    def count_batch(self,):
        """Number of results returned from the query. 

        Returns
        -------
        int
            The number of results
        """
        return len(self)

    @property
    def errors_string(self,):  # can't be called 'error' due to conflict with auto-set field
        """Utility that merges all errors messages into a single string."""
        if self.json.get("errors"):
            return self.json['errors']['query']['header'] + self.json['errors']['query']['details'][0]
        else:
            return ""

    def chunks(self, size=400, key=""):
        """Return an iterator for going through chunks of the JSON results. 

        Note: in DSL queries with multiple `return` statements it is better to specify which result-type needs to be chunked using the `key` parameter. 

        Parameters
        ----------
        size: int, default=400 
            Number of objects (records) to include in each chunk.
        key: str, optional
            The JSON results data object that needs to be chunked eg 'publications' or 'grants'. If not specified, the first available dict key is used. 

        Returns
        -------
        iterator
            A iterator object         

        Example
        -------
        Break up a 1000 records dataset into groups of 100.

        >>> data = dslquery("search publications return publications limit 1000")
        >>> groups = [len(x) for x in data.chunks(size=100)]

        """

        if not key:
            if len(self.good_data_keys()) > 1:
                printDebug(f"Please specify a key from {self.good_data_keys()}")
                return
            else:
                key = self.good_data_keys()[0]
        elif key not in self.good_data_keys():
            printDebug(f"Invalid key: should be one of {self.good_data_keys()}")
            return 

        it = iter(self.json[key])
        chunk = list(islice(it, size))
        while chunk:
            yield chunk
            chunk = list(islice(it, size))

    # Dataframe Methods 

    def as_dataframe(self, key="", links=False, nice=False):
        """Return the JSON data as a Pandas DataFrame. 

        If `key` is empty, the first available JSON key (eg 'publications') is used to determine
        what JSON data should be turned into a dataframe (mostly relevant when using multi-result DSL queries).

        Parameters
        ----------
        key: str, optional
            The JSON results data object that needs to be processed.
        links: bool, optional 
            Tranform suitable fields to hyperlinks. Default: False.
        nice: bool, optional 
            Reformat column names and complex values where possible. Useful for visual inspection and printing our. Default: False.

        Returns
        -------
        pandas.DataFrame
            A DataFrame instance containing API records.   

        Example
        -------
        See https://api-lab.dimensions.ai/cookbooks/1-getting-started/3-Working-with-dataframes.html        

        """

        if not self.json.get("errors"):
            return self.df_factory.df_simple(self.json, key, links, nice)


    def as_dataframe_authors(self, links=False):
        """Return the JSON data as a Pandas DataFrame, in which each row corresponds to a publication author.

        This method works only with 'publications' queries and it's clever enough to know if the `authors` or `author_affiliations` (deprecated) fields are used. The list of affiliations per each author are not broken down and are returned as JSON. So in essence you get one row per author.

        Returns
        -------
        pandas.DataFrame
            A DataFrame instance containing API records.          

        Example
        -------
        See https://api-lab.dimensions.ai/cookbooks/1-getting-started/3-Working-with-dataframes.html  
        """
        if not self.json.get("errors"):
            return self.df_factory.df_authors(self.json, links)


    def as_dataframe_authors_affiliations(self, links=False):
        """Return the JSON data as a Pandas DataFrame, in which each row corresponds to a publication affiliation.

        This method works only with 'publications' queries and it's clever enough to know if the `authors` or `author_affiliations` (deprecated) fields are used. If an author has multiple affiliations, they would be represented in different rows (hence the same authors may appear on different rows). 

        Returns
        -------
        pandas.DataFrame
            A DataFrame instance containing API records.          

        Example
        -------
        See https://api-lab.dimensions.ai/cookbooks/1-getting-started/3-Working-with-dataframes.html  
        """
        if not self.json.get("errors"):
            return self.df_factory.df_authors_affiliations(self.json, links)

    def as_dataframe_concepts(self, key="", links=False):
        """Return the JSON data as a Pandas DataFrame, in which each row corresponds to a single 'concept'.

        This method works only with 'publications' and 'grants' queries and it's clever enough to know if the `concepts` or `concepts_scores` fields are used. Additional metrics like 'frequency' and 'score_average' are also included in the results. 

        Returns
        -------
        pandas.DataFrame
            A DataFrame instance containing API records.          

        Example
        -------
        See https://api-lab.dimensions.ai/cookbooks/1-getting-started/3-Working-with-dataframes.html  
        """
        if not self.json.get("errors"):
            return self.df_factory.df_concepts(self.json, key, links)


    def as_dataframe_funders(self, links=False):
        """Return the JSON data as a Pandas DataFrame, in which each row corresponds to a single 'funder'.

        This method works only with 'grants' queries.

        Returns
        -------
        pandas.DataFrame
            A DataFrame instance containing API records.          

        Example
        -------
        See https://api-lab.dimensions.ai/cookbooks/1-getting-started/3-Working-with-dataframes.html  
        """
        if not self.json.get("errors"):
            return self.df_factory.df_grant_funders(self.json, links)

    def as_dataframe_investigators(self, links=False):
        """Return the JSON data as a Pandas DataFrame, in which each row corresponds to a single 'investigator'.

        This method works only with 'grants' queries.

        Returns
        -------
        pandas.DataFrame
            A DataFrame instance containing API records.          

        Example
        -------
        See https://api-lab.dimensions.ai/cookbooks/1-getting-started/3-Working-with-dataframes.html  
        """
        if not self.json.get("errors"):
            return self.df_factory.df_grant_investigators(self.json, links)

    def as_dimensions_url(self, records=500, verbose=True):
        """Utility that turns a list of records into a Dimensions webapp URL, by using the record IDs as filters.
        
        NOTE: this functionality is EXPERIMENTAL and may break or be removed in future versions. Also, it works only with: publications, grants, patents, clinical_trials, policy_documents.

        Parameters
        ----------
        records: int, default=500 
            The number of record IDs to use. With more than 500, it is likely to incur into a '414 Request-URI Too Large' error. 
        verbose: bool, default=True
            Verbose mode

        Returns
        -------
        str
            A string representing a Dimensions URL.  

        Example
        -------

        >>> data = dsl.query(\"\""search publications where id in ["pub.1120715293", "pub.1120975084", "pub1122068834", "pub.1120602308"] return publications\"\"")
        >>> data.as_dimensions_url()
        'https://app.dimensions.ai/discover/publication?search_text=id%3A+%28pub.1120975084+OR+pub.1120715293+OR+pub.1120602308%29'
        """
        
        if verbose: printDebug("Warning: this is an experimental and unsupported feature.")


        # General query structure for IDs: 
           
        # `id: (pub.1120715293 OR pub.112097508 4 OR pub.1122068834 OR pub.1120602308)`

        # Final URL looks like this https://app.dimensions.ai/discover/publication?search_text=id%3A+%28pub.1120715293+OR+pub.1120975084+OR+pub.1122068834+OR+pub.1120602308%29

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


    def to_json_file(self, filename="", verbose=True):
        """Export API results data to a JSON file. 

        Note: this is normally used in combination with the `load_json_file` method.

        Parameters
        ----------
        filename: str, optional 
            A filename/path where to save the data. If not provided, a unique name is generated automatically.

        Returns
        -------
        str
            The string representation of the filename the data is saved to.         

        Example
        -------
        Save the results of a query to a JSON file, then reload the same file and create a new dataset.

        >>> dataset = dsl.query(\"\""search publications where journal.title="nature medicine" return publications[id+title+year+concepts] limit 100"\"\")
        Returned Publications: 100 (total = 12641)

        Save the data to a local json file

        >>> FILENAME = "test-api-save.json"
        >>> dataset.to_json_file(FILENAME, verbose=True)
        Saved to file:  test-api-save.json
        
        Data can be reloaded from file, using the `load_json_file` class method. 

        >>> new_dataset = DslDataset.load_json_file(FILENAME, verbose=True)
        Loaded file:  test-api-save.json
        >>> print(new_dataset)
        <dimcli.DslDataset object #4370267824. Records: 100/12641>

        """
        if not self.json.get("errors"):
            if not filename:
                filename = time.strftime(f"dimensions_data_%Y-%m-%d_%H-%M-%S.json")
            with open(filename, 'w') as outfile:
                json.dump(self.json, outfile)
                if verbose: printDebug("Saved to file: ", filename)
                return filename




    def to_gsheets(self, title=None, verbose=True):
        """Export the dataframe version of some API results to a public google sheet. Google OAUTH client credentials are a prerequisite for this method to work correctly. 

        Parameters
        ----------
        title: str, optional 
            The spreadsheet title, if one wants to reuse an existing spreadsheet.
        verbose: bool, default=True
            Verbose mode

        Notes
        -----
        This method assumes that the calling environment can provide valid Google authentication credentials.
        There are two routes to make this work, depending on whether one is using Google Colab or a traditional Jupyter environment.

        **Google Colab**
        This is the easiest route. In Google Colab, all required libraries are already available. The `to_gsheets` method simply triggers the built-in authentication process via a pop up window. 
        
        **Jupyter**
        This route involves a few more steps. In Jupyter, it is necessary to install the gspread, oauth2client and gspread_dataframe modules first. Secondly, one needs to create Google Drive access credentials using OAUTH (which boils down to a JSON file). Note that the credentials file needs to be saved in: `~/.config/gspread/credentials.json` (for gpread). 
        The steps are described at https://gspread.readthedocs.io/en/latest/oauth2.html#for-end-users-using-oauth-client-id.

        Returns
        -------
        str
            The google sheet URL as a string.   

        """
        if self.json.get("errors"):
            return None

        df = self.as_dataframe()

        return export_as_gsheets(df,  title=title, verbose=verbose)        
             
    

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