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
from .utils.misc_utils import printDebug

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



def login(  username="", 
            password="", 
            endpoint="", 
            instance="", 
            key="", 
            verify_ssl=True, 
            verbose=True):
    """Login into the Dimensions API and store the query token in memory. 

    Two cases, with a few defaults:

    * If credentials are provided, the login is performed using those credentials.
        * If endpoint is not provided, the default endpoint is used ("https://app.dimensions.ai")
    * If credentials are not passed, login is attempted using the local dsl.ini credentials file. 
        * If neither instance nor endpoint are provided, instance defaults to 'live'.
        * If an endpoint url is provided, the first matching directive in the credentials file is used.

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
    verify_ssl: bool, optional
        Verify SSL certificates for HTTPS requests. Default: True.
    verbose: bool, optional
        Verbose mode. Default: True.


    Notes
    ---------------
    The endpoint value can either be simply the Dimensions server hostname or the full API endpoint path. All the options below are valid endpoints: 

        * `https://app.dimensions.ai`
        * `https://app.dimensions.ai/api/dsl/v1` 
        * `https://app.dimensions.ai/api/dsl/v2`


    About SSL verification:

    Dimcli internally uses the Requests library, which verifies SSL certificates for HTTPS requests, just like a web browser. For some users, it is necessary to turn off SSL verification in order to connect to the API. This can be achieved by passing `verify_ssl=False` at login time. All subsequent API queries will not use SSL verification. NOTE This setting can also be added to the `dsl.ini` file with the following line: `verify_ssl=false`.


    Example
    -------
    If you have already set up the credentials file (see above), no need to pass log in details
    
    >>> dimcli.login()

    Otherwise you can authenticate by passing your login details as arguments
    
    >>> dimcli.login(key="my-secret-key", endpoint="https://your-url.dimensions.ai")

    You can specify endpoint, which by default is set to "https://app.dimensions.ai"
    
    >>> dimcli.login(key="my-secret-key", endpoint="https://nannies-research.dimensions.ai")

    Legacy authentication mechanisms with username/password are also supported

    >>> dimcli.login(username="mary.poppins", password="chimneysweeper", endpoint="https://nannies-research.dimensions.ai")

    See Also
    ---------------
    dimcli.core.api.Dsl

    """

    from .core.auth import do_global_login, get_global_connection

    try:
        do_global_login(instance, username, password, key, endpoint, verify_ssl)
    except Exception as e:
        printDebug("Login failed: please ensure your credentials are correct.")
        raise(e)

    CONNECTION = get_global_connection()

    if CONNECTION.token and verbose:
        _print_login_success(username, password, key)
        print_dimcli_report_if_outdated()



def _print_login_success(username, password, key):
    click.secho("Dimcli - Dimensions API Client (" + VERSION + ")", dim=True)
    CLIENT = Dsl(verbose=False)
    # dynamically retrieve dsl version 
    try:
        _info = "v" + CLIENT.query("describe version")['release']
    except:
        _info = "[failed to retrieve version information]"

    if (username and password) or key:
        _method = "manual login"
    else:
        _method = "dsl.ini file"
    click.secho(f"Connected to: <{CLIENT._url}> - DSL {_info}", dim=True)
    click.secho(f"Method: {_method}", dim=True)




def logout():
    """Reset the connection to the Dimensions API. 
    
    This allows to create a new connection subsequently, eg to a different endpoint.

    Example
    -------

    >>> dimcli.logout()

    """
    from .core.auth import get_global_connection
    CONNECTION = get_global_connection()
    if CONNECTION.token:
        CONNECTION.reset_login()
        printDebug("Logging out... done") 
    else:
        printDebug("Please login first") 



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
    from .core.auth import get_global_connection
    CONNECTION = get_global_connection()
    if CONNECTION.token:
        printDebug("Dimcli %s - Succesfully connected to <%s>" % (str(VERSION), CONNECTION.url)) 
        return True
    else:
        printDebug("Status: not logged in") 
        return False

