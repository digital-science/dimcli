from .VERSION import __version__, VERSION

from .core.api import Dsl
from .core.dsl_grammar import G 



try:
    # https://stackoverflow.com/questions/32538758/nameerror-name-get-ipython-is-not-defined
    # if run outside iPython, the magic fails so we use this as a test 
    type(get_ipython)
    ipython_env = True
except:
    ipython_env = False

if ipython_env:
    from .jupyter import magics