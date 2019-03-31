from .VERSION import __version__, VERSION

from .dimensions import Dsl, chunks_of

from .repl.dsl_grammar import VOCABULARY

try:
    # https://stackoverflow.com/questions/32538758/nameerror-name-get-ipython-is-not-defined
    # if run outside iPython, the magic fail so we use this as a test 
    type(get_ipython)
    ipython_env = True
except:
    ipython_env = False

if ipython_env:
    from .jupyter import magics