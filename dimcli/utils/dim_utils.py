"""
Dimcli utilities for querying and working with Dimensions data.  
NOTE: these functions are attached to the top level ``dimcli.utils`` module. So you can load them as follows:

>>> from dimcli.utils import *

"""


import click
import time
import json
import sys
import os



def dslquery(query_string):
    """Shortcut for running a query without instantiating dimcli.Dsl(). 
    
    Added for backward compatibility with legacy API tutorials. Requires file-based credentials for logging in.
    
    Parameters
    ----------
    query_string: str 
        A valid DSL query.    

    Returns
    -------
    DslDataset
        A Dimcli wrapper object containing JSON data. 

    """
    from ..core.auth import is_logged_in_globally as is_logged_in
    from ..core.api import Dsl
    if is_logged_in():
        dsl = Dsl()
        res = dsl.query(query_string, verbose=True)
        return res


def dslquery_json(query_string):
    """Shortcut for running a query without instantiating dimcli.Dsl(). Same as ``dslquery`` but returns raw JSON instead of Api.DslDataset object
    
    Added for backward compatibility with legacy API tutorials. Requires file-based credentials for logging in.

    Parameters
    ----------
    query_string: str 
        A valid DSL query.    

    Returns
    -------
    Dict
        API JSON data, represented as a dict object.

    """
    from ..core.auth import is_logged_in_globally as is_logged_in
    from ..core.api import Dsl
    if is_logged_in():
        dsl = Dsl()
        return dsl.query(query_string).json


def dslqueryall(query_string):
    """Shortcut for running a loop query without instantiating dimcli.Dsl().
    
    Added for backward compatibility with legacy API tutorials. Requires file-based credentials for logging in.

    Parameters
    ----------
    query_string: str 
        A valid DSL query.    

    Returns
    -------
    DslDataset
        A Dimcli wrapper object containing JSON data.

    """
    from ..core.auth import is_logged_in_globally as is_logged_in
    from ..core.api import Dsl
    if is_logged_in():
        dsl = Dsl()
        return dsl.query_iterative(query_string)




def dimensions_url(obj_id, obj_type="", verbose=True):
    """Generate a valid Dimensions URL for one of the available sources.

    Parameters
    ----------
    obj_id: str 
        A Dimensions ID for one of the available sources.  
    obj_type: str, optional
        The name of the source: one of 'publications', 'grants', 'patents', 'policy_documents', 'clinical_trials', 'researchers'. If not provided, it's inferred using the ID structure.

    Returns
    -------
    str
        The object URL.

    Example
    ----------
    >>> from dimcli.utils import dimensions_url
    >>> dimensions_url("pub.1127419018")
    'https://app.dimensions.ai/details/publication/pub.1127419018'

    """
    
    from ..core.dsl_grammar import G 

    if obj_type and (obj_type not in G.sources()):
        raise ValueError("ERROR: valid sources are: " + " ".join([x for x in G.sources()]))
    else:
        if not obj_type:
            for source, prefix in G.object_id_patterns().items():
                if obj_id.startswith(prefix):
                    obj_type = source
        if obj_type:
            url = G.url_for_source(obj_type)
            if url:
                return url + obj_id



def dimensions_search_url(keywords_list_as_string):
    """Generate a valid keyword search URL for Dimensions.

    Parameters
    ----------
    keywords_list_as_string: str 
        List of search keywords.  

    Returns
    -------
    str
        The Dimensions URL.

    Example
    ----------
    >>> from dimcli.utils import dimensions_search_url
    >>> dimensions_search_url("graphene AND south korea")
    'https://app.dimensions.ai/discover/publication?search_text=graphene%20AND%20south%20korea&search_type=kws&search_field=full_search'

    """

    q = """https://app.dimensions.ai/discover/publication?search_text={}&search_type=kws&search_field=full_search"""
    from urllib.parse import quote   
    s = quote(keywords_list_as_string)  
    return q.format(s)




def dsl_escape(stringa, all=False):   
    """Helper for escaping the full-text inner query strings, when they includes quotes. 
    
    EG with the query string:
    '"2019-nCoV" OR "COVID-19" OR "SARS-CoV-2" OR (("coronavirus"  OR "corona virus") AND (Wuhan OR China))'
    
    In Python, if you want to embed it into a DSL query, it has to become:
    '\\"2019-nCoV\\" OR \\"COVID-19\\" OR \\"SARS-CoV-2\\" OR ((\\"coronavirus\\"  OR \\"corona virus\\") AND (Wuhan OR China))'

    See also: https://docs.dimensions.ai/dsl/language.html#for-search-term

    Parameters
    ----------
    stringa: str 
        Full-text search component of a DSL query.
    all: bool, default=False
        By default only quotes as escaped. Set to True to escape all special characters (eg colons)

    Example
    ----------
    >>> dsl_escape('Solar cells: a new technology?', True)
    'Solar cells\\: a new technology?'

    
    """
    
    if all:
        escaped = stringa.translate(str.maketrans({"^":  r"\^",
                                                    '"':  r'\"',
                                                    "\\": r"\\",
                                                    ":":  r"\:",
                                                    "~":  r"\~",
                                                    "[":  r"\[",
                                                    "]":  r"\]",
                                                    "{":  r"\{",
                                                    "}":  r"\}",
                                                    "(":  r"\(",
                                                    ")":  r"\)",
                                                    "!":  r"\!",
                                                    "|":  r"\|",
                                                    "&":  r"\&",
                                                    "+":  r"\+",
                                                    }))
    else:
        escaped = stringa.translate(str.maketrans({'"':  r'\"'}))        
    return escaped
