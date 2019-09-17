from .VERSION import __version__, VERSION

from .core.api import Dsl
from .core.dsl_grammar import G 

from .core.auth import do_global_login as login

try:
    # if run outside iPython, the magic fails so we use this as a test
    # https://stackoverflow.com/questions/32538758/nameerror-name-get-ipython-is-not-defined
    get_ipython()
    ipython_env = True
except:
    ipython_env = False

if ipython_env:
    from .jupyter import magics