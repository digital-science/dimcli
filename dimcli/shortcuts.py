
from . import *
from .core.utils import print_json_stats, chunks_of, normalize_key
# chunks_of/normalize_key imported so that it's in the shortcuts namespace and easier to import

def dslquery(query_string):
    """shortcut for running a query - meant to be used only within interactive computing environments
    """
    from .core.auth import is_logged_in
    if is_logged_in():
        dsl = Dsl()
        res = dsl.query(query_string)
        # print results
        print_json_stats(res, query_string)
        return res


def dslquery_json(query_string):
    """shortcut for backward compatibility 
    Same as above but returns raw JSON instead of Api.Result object

    Pattern: `from dimcli.shortcuts import dslquery_json as dslquery`
    """
    from .core.auth import is_logged_in
    if is_logged_in():
        dsl = Dsl()
        return dsl.query(query_string).json


def dslqueryall(query_string):
    """shortcut for running a loop query - meant to be used only within interactive computing environments
    NOTE: this requires the file-based credentials file set up.
    """
    from .core.auth import is_logged_in
    if is_logged_in():
        dsl = Dsl()
        return dsl.query_iterative(query_string)