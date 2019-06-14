
from . import *

def dslquery(query_string):
    """shortcut for backward compatibility
    import dimcli
    dslquery = dimcli.dslquery
    # then can use old notebooks....

    NOTE: this assumes you have the file-based credentials file set up, always!
    """
    dsl = Dsl()
    return dsl.query(query_string).json