from .VERSION import __version__, VERSION

from .core.api import Dsl
from .core.dsl_grammar import G 


try:
    # if run outside iPython, the magic fails so we use this as a test
    # https://stackoverflow.com/questions/32538758/nameerror-name-get-ipython-is-not-defined
    get_ipython()
    ipython_env = True
except:
    ipython_env = False

if ipython_env:
    from .jupyter import magics



def login(username="", password="", endpoint="https://app.dimensions.ai", instance="live"):
    """
    Login into the Dimensions API and obtain a query token. If credentials are not passed, we attempt to login using the local dsl.ini credentials file. 

    Args: 
    * username
    * password
    * endpoint (defaults to "https://app.dimensions.ai")
    * instance (defaults to "live")
    """
    from .core.auth import do_global_login, CONNECTION

    try:
        do_global_login(instance, username, password, endpoint)
    except Exception as e:
        print(str(e))
        print("Login failed: please ensure your credentials are correct.")

    if CONNECTION['token']:
        if username and password:
            print("DimCli %s - Succesfully connected to <%s> (method: manual login)" % (str(VERSION), CONNECTION['url'])) 
        else:
            # try to use local init file using instance parameter
            print("DimCli %s - Succesfully connected to <%s> (method: dsl.ini file)" % (str(VERSION), CONNECTION['url']))


def logout():
    """
    Reset the connectiont to the Dimensions API. This allows to create a new connection subsequently, eg to a different endpoint.
    """
    from .core.auth import reset_login, CONNECTION
    reset_login()
    if CONNECTION['token']:
        print("Log out failed!") 
    else:
        print("Log out operation successful.") 