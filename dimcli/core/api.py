import configparser
import requests
import os.path
import os
import time
import json
import click
import IPython.display
from itertools import islice

from .utils import line_search_return
from .dsl_grammar import G


#
#
# File-based Authentication : how to
# ===================
#
# Authentication details can be stored in a `dsl.ini` file in `~/.dimensions/`
# File contents need to have this structure:
#
#
# [instance.live]
# url=https://app.dimensions.ai
# login=your_username
# password=your_password
#
#
# The section name has to start with "instance.". 
# "live" is the default name for most installations.
#
# If you have access to other Dimensions APIs just add an entry for them with a suitable name.
#
#
#


USER_DIR = os.path.expanduser("~/.dimensions/")
USER_CONFIG_FILE_NAME = "dsl.ini"
USER_CONFIG_FILE = os.path.expanduser(USER_DIR + USER_CONFIG_FILE_NAME)
USER_JSON_OUTPUTS_DIR = os.path.expanduser(USER_DIR + "json/")
USER_HISTORY_FILE = os.path.expanduser(USER_DIR + "history.txt")




class Result(IPython.display.JSON):
    """
    Wrapper for JSON results from DSL

    >>> res = dsl.query("search publications return publications")
    >>> res.data # => shows the underlying JSON data

    # Magic methods: 

    >>> res['publications'] # => the dict section
    >>> res.['xxx'] # => false, not found
    >>> res.['stats'] # => the _stats dict

    """
    def __init__(self, data):
        IPython.display.JSON.__init__(self, data)

    def __getitem__(self, key):
        "return dict key as slice"
        if key == "stats":
            key = "_stats" # syntactic sugar
        if key in self.data:
            return self.data[key]
        else:
            return False

    def json(self):
        "return the raw json for this query"
        return self.data 

    def keys(self,):
        return list(self.data.keys())

    def keys_and_count(self,):
        return [(x, len(self.data[x])) for x in self.data.keys()]

    def __repr__(self):
        return "<dimcli.Result object #%s: %s>" % (str(id(self)), str(self.keys_and_count()))
        # return '{Query Results:'+self.id+', age:'+str(self.age)+ '}'



class Dsl:
    """
    Object for abstracting common interaction steps with the Dimensions API. 
    Most often you just want to instantiate, autheticate and query() - yeah!

    >>> import dimcli
    # if you have set up a credentials file, no need to pass log in details
    >>> dsl = dimcli.Dsl()
    # queries always return a Result object (subclassing IPython.display.JSON)
    >>> dsl.query("search grants for \"malaria\" return researchers")
    >>> <dimcli.dimensions.Result object>
    # use the .data method to get the JSON
    >>> dsl.query("search grants for \"malaria\" return researchers").data
    >>> {'researchers': [{'id': 'ur.01332073522.49',
            'count': 75,
            'last_name': 'White',
            'first_name': 'Nicholas J'},
        "... JSON data continues ... "

    """
    def __init__(self, instance="live", user="", password="", endpoint="https://app.dimensions.ai", show_results=True):
        # print(os.getcwd())
        if user and password:
            self._url = endpoint
            self._username = user
            self._password = password
        else:
            config_section = self._get_config_from_file(instance)
            self._url = config_section['url']
            self._username = config_section['login']
            self._password = config_section['password']

        self._show_results = show_results
        self._login()

    def _get_config_from_file(self, instance_name):
        """
        get the dsl.ini file and extraction credentials
        * first use the current WD 
            => useful for jup notebooks without system wide installation
        * second use the default system location 
            => this is the usual case for CLI
        """
        config = configparser.ConfigParser()
        if os.path.exists(os.getcwd() + "/" + USER_CONFIG_FILE_NAME):
            credentials = os.getcwd() + "/" + USER_CONFIG_FILE_NAME
        else:
            credentials = os.path.expanduser(USER_CONFIG_FILE)
        try:
            config.read(credentials)
        except:
            click.secho("ERROR: Credentials file not found at: %s" % credentials, fg="red")
            click.secho("HowTo: https://github.com/lambdamusic/dimcli#credentials-file", fg="red")
            raise
        try:
            section = config['instance.' + instance_name]
        except:
            click.secho("ERROR: Credentials file does contain settings for instance: %s" % instance_name, fg="red")
            click.secho("HowTo: https://github.com/lambdamusic/dimcli#credentials-file", fg="red")
            raise
        return section

    def _login(self):
        login = {'username': self._username, 'password': self._password}
        response = requests.post(
            '{}/api/auth.json'.format(self._url), json=login)
        response.raise_for_status()

        token = response.json()['token']
        self._headers = {'Authorization': "JWT " + token}

    def query(self, q, show_results=None, retry=0):
        """
        Execute DSL query.
        By default it doesn't show results, but it uses the iPython rich widgets for it, optimized for Jupyter Notebooks.
        """
        #   Execute DSL query.
        response = requests.post(
            '{}/api/dsl.json'.format(self._url), data=q, headers=self._headers)
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
            self._login()
            return self.query(q)
        elif response.status_code in [200, 400, 500]:  
            ###  
            # OK or Error Info :-)
            ###
            result = Result(response.json())
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
        transform a query into a loop that pulls out all data available 
        @TODO is there a hard limit of 50k results for limit/skip?
        """

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


