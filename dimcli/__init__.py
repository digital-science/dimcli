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
