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
    if type(obj_id) != str:
        return ""
    obj_id = obj_id.strip()

    if obj_type and (obj_type not in G.sources()):
        obj_type = ""
        # raise ValueError("ERROR: valid sources are: " + " ".join([x for x in G.sources()]))
    
    if not obj_type: # then infer it from the ID
        for source, prefix in G.object_id_patterns().items():
            # print("Inferring source from ID: {}".format(obj_id), source, prefix)
            if obj_id.startswith(prefix):
                # print("Inferred source: {}".format(source))
                obj_type = source
    if obj_type:
        url = G.url_for_source(obj_type)
        if url:
            return url + str(obj_id)



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





def dimensions_styler(df, source_type=""):
    """Format the text display value of a dataframe by including Dimensions hyperlinks whenever possible.
    Useful mainly in notebooks when printing out dataframes and clicking on links etc..
    Expects column names to match the default DSL field names. 

    Parameters
    ----------
    df: pd.Dataframe
        Pandas dataframe obtained from a DSL query e.g. via the `as_dataframe` methods.
    source_type: str, optional
        The name of the source: one of 'publications', 'grants', 'patents', 'policy_documents', 'clinical_trials', 'researchers'. If not provided, it can be inferred in some cases.

    Notes
    -----
    Implemented using https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.format.html. Side effect is that the resulting dataframe becomes an instance of https://pandas.io.formats.style.styler/, which is a wrapper around the underlying Styler object. 
    NOTE To get back to the original dataframe, you can use the `.data` method.

    Returns
    -------
    pandas.io.formats.style.Styler
        Wrapper for a dataframe object, including custom Dimensions hyperlinks.

    Example
    -------
    >>> from dimcli.utils import dimensions_styler
    >>> dsl = dimcli.Dsl() 
    >>> q = 'search publications for "scientometrics" return publications[basics]' 
    >>> df = dsl.query(q).as_dataframe()
    >>> dimensions_styler(df)
    # alternatively, use the shortcut method:
    >>> dsl.query(q).as_dataframe(links=True)
    """

    format_rules = {}

    def df_value_as_link(url, val, url_root=""):
        """Val is the value found in the dataframe column. It should be a string or an integer, or a list.
        If it's a list, we just take the first element (e.g. for 'linkout' field).
        If it's a float, it means it's a Pandas NaN. So we don't want to return a link.
        """
        if not val or type(val) == float:
            return val
        if type(val) == list:
            url = val[0]
        if url_root:
            url = url_root + url
        return '<a target="_blank" href="{}">{}</a>'.format(url, val)
            

    cols = [x.lower() for x in df.columns]


    # transformations
    # multiple naming supported, so to handle standard conversion (--nice flag)
    for test in ["dimensions_url", 'Dimensions URL']:
        if test.lower() in cols:
            format_rules[test] = lambda x: df_value_as_link(x, x)

    for test in ["linkout", 'Source Linkout']:
        if test.lower() in cols:
            # ps this is a list, only first el will be used
            format_rules['linkout'] = lambda x: df_value_as_link(x, x)

    if "orcid" in cols:
        # ps this is a list, only first el will be used
        url_root = "https://orcid.org/"
        format_rules['orcid'] = lambda x: df_value_as_link(x, x, url_root)

    for test in ["doi", 'DOI']:
        if test.lower() in cols:
            url_root = "https://doi.org/"
            format_rules[test] = lambda x: df_value_as_link(x, x, url_root)

    for test in ["id", 'Publication ID', 'Dataset ID', 'Trial ID', 'Grant ID',]:
        if test.lower() in cols:
            format_rules[test] = lambda x: df_value_as_link(dimensions_url(x, source_type), x)

    for test in ["journal.id", 'Source ID']:
        if test.lower() in cols:
            format_rules[test] = lambda x: df_value_as_link(dimensions_url(x, "source_titles"), x)

    # denorm data for special df methods
    if "pub_id" in cols:
        format_rules["pub_id"] = lambda x: df_value_as_link(dimensions_url(x, "publications"), x)

    if "researcher_id" in cols:
        format_rules["researcher_id"] = lambda x: df_value_as_link(dimensions_url(x, "researchers"), x)

    if "grant_id" in cols:
        format_rules["grant_id"] = lambda x: df_value_as_link(dimensions_url(x, "grants"), x)

    if "aff_id" in cols:
        format_rules["aff_id"] = lambda x: df_value_as_link(dimensions_url(x, "organizations"), x)

    if "current_organization_id" in cols:
        format_rules["current_organization_id"] = lambda x: df_value_as_link(dimensions_url(x, "organizations"), x)

    


    return df.style.format(format_rules)