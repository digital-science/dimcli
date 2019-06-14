
from . import *

def dslquery(query_string):
    """shortcut for running a query
    NOTE: this requires the file-based credentials file set up
    """
    dsl = Dsl()
    return dsl.query(query_string)


def dslquery_json(query_string):
    """shortcut for backward compatibility
    Same as above but returns raw JSON instead of Api.Result object
    """
    dsl = Dsl()
    return dsl.query(query_string).json