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





def gen_dslqueries(sources, text="Albert Einstein"):
    """Generate test DSL queries for each source
    eg
    >>> from dimcli import G
    >>> gen_dslqueries(G.sources())
    """
    
    _q = """ search {} for "{}" return {}[basics] limit 10 """
    out = []
    for source in sources:
        out += [_q.format(source, source)]
        return reversed(out)


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





def dimensions_styler(df, source_type="", title_links=True):
    """Format the text display value of a dataframe by including Dimensions hyperlinks whenever possible.
    Useful mainly in notebooks when printing out dataframes and clicking on links etc..
    Expects column names to match the default DSL field names. 

    Parameters
    ----------
    df: pd.Dataframe
        Pandas dataframe obtained from a DSL query e.g. via the `as_dataframe` methods.
    source_type: str, optional
        The name of the source: one of 'publications', 'grants', 'patents', 'policy_documents', 'clinical_trials', 'researchers'. If not provided, it can be inferred in some cases.
    title_links: bool, optional, True
        Hyperlink document titles too, using the ID (if available).

    Notes
    -----
    Implemented using https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.format.html. Side effect is that the resulting dataframe becomes an instance of pandas.io.formats.style.styler, which is a wrapper around the underlying Styler object. TIP To get back to the original dataframe, you can use the `.data` method. 
    See also: https://stackoverflow.com/questions/42263946/how-to-create-a-table-with-clickable-hyperlink-in-pandas-jupyter-notebook

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
    # 
    # alternatively, using the shortcut method:
    #
    >>> dsl.query(q).as_dataframe(links=True)
    """

    format_rules = {}
    cols = [x.lower() for x in df.columns]
    REPLACE_TITLES = title_links
    cols_to_drop = [] 


    def df_value_as_link(url, val, url_root="", verbose=False):
        """Generic method to create an HTML hyperlink from a dataframe cell value and a URL.
        If cell value is list, we just take the first element (e.g. for 'linkout' field).
        NOTE If cell value is a float, it means it's a Pandas NaN. So we don't want to return a link.
        """
        if verbose: print(f"""url: {url} / val: {val} / url_root: {url_root}""")
        if not val or type(val) == float:
            return val
        if type(val) == list:
            url = val[0]
        if url_root:
            url = url_root + url
        elif "###" in val: # title URL
            val, url = val.split("###")
        return '<a target="_blank" href="{}">{}</a>'.format(url, val)
            
    def df_format_gridids(val, verbose=False):
        """Version of df_value_as_link() for lists of GRID IDs. 
        NOTE If cell value is a float, it means it's a Pandas NaN. So we don't want to return a link.

        val: string
            List of GRID IDs separated by ';' (normal output of 'nice' converters)
        """
        if verbose: print(f"""val: {val} """)
        if not val or type(val) == float:
            return val
        grids = val.split(";")
        z = ['<a target="_blank" href="{}">{}</a>'.format(dimensions_url(g.strip(), "organizations"), g) for g in grids]
        return "; ".join(z)



    # TRANSFORMATIONS
    # NOTE multiple naming supported, so to handle columm conversions obtained via --nice flag

    for col in ["dimensions_url", 'Dimensions URL']:
        if col.lower() in cols:
            cols_to_drop += [col] # always drop cause IDs get linked already
            # format_rules[col] = lambda x: df_value_as_link(x, x)

    for col in ["linkout", "Source Linkout", "Linkout"]:
        if col.lower() in cols:
            # ps this is a list, only first el will be used
            format_rules[col] = lambda x: df_value_as_link(x, x)

    for col in ["doi", 'DOI']:
        if col.lower() in cols:
            url_root = "https://doi.org/"
            format_rules[col] = lambda x: df_value_as_link(x, x, url_root)

    for col in ["id", 'Publication ID', 'Patent ID', 'Dataset ID', 'Trial ID', 
                'Policy ID', 'Grant ID', 'GRID ID', 'Researcher ID', 'Report ID']:
        if col.lower() in cols:
            # print("Matched =", col)
            format_rules[col] = lambda x: df_value_as_link(dimensions_url(x, source_type), x)
            # HYPERLINK THE TITLE AS WELL, USING THE ID
            # create a new col with URL+title and split it when formatting the table
            if REPLACE_TITLES:    
                title_names = ["title", "Title", "name", "Name"]
                for t in title_names:
                    if t in df.columns:
                        # print("Matched Title=", t, source_type)
                        df[t] = df[t] + '###' + df[col].apply(lambda x: dimensions_url(x, source_type))
                        format_rules[t] = lambda x: df_value_as_link(x, x)
                        cols_to_drop += [col]

    for col in ["journal.id", 'Source ID']:
        if col.lower() in cols:
            format_rules[col] = lambda x: df_value_as_link(dimensions_url(x, "source_titles"), x)
            # HYPERLINK THE TITLE AS WELL, USING THE ID
            # create a new col with URL+title and split it when formatting the table
            if REPLACE_TITLES:    
                title_names = ["journal.title", "Source title"]
                for t in title_names:
                    if t in df.columns:
                        df[t] = df[t] + '###' + df[col].apply(lambda x: dimensions_url(x, "source_titles"))
                        format_rules[t] = lambda x: df_value_as_link(x, x)    
                        cols_to_drop += [col]    

    # denorm data for cols resulting from dimcli df methods 
    # TODO more testing needed
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

    for col in ["orcid_id", 'Orcid IDs']:
        if col.lower() in cols:
            url_root = "https://orcid.org/"
            format_rules[col] = lambda x: df_value_as_link(x, x, url_root)

    for col in ["GRID IDs", "Funders GRID IDs", "Assignees GRID IDs"]:
        if col.lower() in cols:
            format_rules[col] = lambda x: df_format_gridids(x)

    df = df.style.format(format_rules)
    if cols_to_drop:
        df = df.hide_columns(cols_to_drop)
    return df

