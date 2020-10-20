"""
Dimcli utilities for logging in/out of the Dimensions API.  
NOTE: these functions are attached to the top level ``dimcli`` module. So you can load them as follows::

>>> import dimcli
>>> dimcli.login()

"""

from .VERSION import __version__, VERSION

from .core.api import Dsl, DslDataset
from .core.dsl_grammar import G 
from .utils.version_utils import print_dimcli_report_if_outdated

import click

try:
    # if run outside iPython, the magic fails so we use this as a test
    # https://stackoverflow.com/questions/32538758/nameerror-name-get-ipython-is-not-defined
    get_ipython()
    ipython_env = True
except:
    ipython_env = False

if ipython_env:
    from .jupyter import magics


#
# determine if we are in Google Colab or Jupyter
try:
    from google.colab import files
    # load table plugin => %load_ext google.colab.data_table
    get_ipython().run_line_magic("load_ext", "google.colab.data_table")
    COLAB_ENV = True
except:
    COLAB_ENV = False



def login(username="", password="", endpoint="https://app.dimensions.ai", instance="live", key="", verbose=True):
    """Login into the Dimensions API and store the query token in memory. 

    Two cases:

    * If credentials are not passed, login is attempted using the local dsl.ini credentials file. 
    
    * If Google COLAB is detected and user/psw is not available, the interactive login workflow is triggered

    Parameters
    ----------
    username: str, optional
        The API username
    password: str, optional
        The API password
    endpoint: str, optional
        The API endpoint - default is "https://app.dimensions.ai"
    instance: str, optional
        The instance name, from the local dsl.ini credentials file. Default: 'live'
    key: str, optional
        The API key (available to some users instead of username/password)
    verbose: bool, optional
        Verbose mode. Default: True.
       

    Example
    -------
    If you have already set up the credentials file (see above), no need to pass log in details
    
    >>> dimcli.login()

    Otherwise you can authenticate by passing your login details as arguments
    
    >>> dimcli.login(user="mary.poppins", password="chimneysweeper")

    You can specify endpoint, which by default is set to "https://app.dimensions.ai"
    
    >>> dimcli.login(user="mary.poppins", password="chimneysweeper", ednpoint="https://nannies-research.dimensions.ai")

    If you use key based authentication, then do
    
    >>> dimcli.login(key="my-secret-key", endpoint="https://your-url.dimensions.ai")


    """

    from .core.auth import do_global_login, get_connection

    try:
        do_global_login(instance, username, password, key, endpoint)
    except Exception as e:
        print("Login failed: please ensure your credentials are correct.")
        raise(e)

    CONNECTION = get_connection()

    if CONNECTION['token'] and verbose:
        _print_login_success(CONNECTION, username, password, key)
        print_dimcli_report_if_outdated()



def _print_login_success(CONNECTION, username, password, key):
    click.secho("Dimcli - Dimensions API Client (" + VERSION + ")", dim=True)
    CLIENT = Dsl(verbose=False)
    # dynamically retrieve dsl version 
    try:
        _info = CLIENT.query("describe version")['release']
    except:
        _info = "not available"

    if (username and password) or key:
        _method = "manual login"
    else:
        _method = "dsl.ini file"
    click.secho(f"Connected to: {CLIENT._url} - DSL v{_info}", dim=True)
    click.secho(f"Method: {_method}", dim=True)




def logout():
    """Reset the connection to the Dimensions API. 
    
    This allows to create a new connection subsequently, eg to a different endpoint.

    Example
    -------

    >>> dimcli.logout()

    """
    from .core.auth import reset_login, get_connection
    CONNECTION = get_connection()
    if CONNECTION['token']:
        reset_login()
        print("Logging out... done") 
    else:
        print("Please login first") 



def login_status():
    """Utility to check whether we are logged in or not

    Returns
    -------
    bool
        True if logged in, otherwise False.  

    Example
    -------

    >>> dimcli.login_status()
    False

    """
    from .core.auth import get_connection
    CONNECTION = get_connection()
    if CONNECTION['token']:
        print("Dimcli %s - Succesfully connected to <%s>" % (str(VERSION), CONNECTION['url'])) 
        return True
    else:
        print("Status: not logged in") 
        return False