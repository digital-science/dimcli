"""
DSL / API specific utilities

"""


import click
import time
import json
import sys
import subprocess
import os
import re
import webbrowser
from itertools import islice
from pandas import json_normalize, DataFrame

from ..core.dsl_grammar import *

from .html import html_template_interactive



def dslquery(query_string):
    """shortcut for running a query - meant to be used only within interactive computing environments
    """
    from ..core.auth import is_logged_in
    if is_logged_in():
        dsl = Dsl()
        res = dsl.query(query_string, verbose=True)
        return res


def dslquery_json(query_string):
    """shortcut for backward compatibility 
    Same as above but returns raw JSON instead of Api.DslDataset object

    Pattern: `from dimcli.shortcuts import dslquery_json as dslquery`
    """
    from ..core.auth import is_logged_in
    if is_logged_in():
        dsl = Dsl()
        return dsl.query(query_string).json


def dslqueryall(query_string):
    """shortcut for running a loop query - meant to be used only within interactive computing environments
    NOTE: this requires the file-based credentials file set up.
    """
    from ..core.auth import is_logged_in
    if is_logged_in():
        dsl = Dsl()
        return dsl.query_iterative(query_string)




def dimensions_url(obj_id, obj_type="", verbose=True):
    """
    Generate a valid Dimensions URL for one of the available sources.
    obj_id: the dimensions ID of the object
    obj_type: one of 'publications', 'grants', 'patents', 'policy_documents', 'clinical_trials', 'researchers'
    """
    
    if obj_type and obj_type not in G.sources():
        raise ValueError("ERROR: valid sources are: " + " ".join([x for x in G.sources()]))
    if not obj_type:
        for source, prefix in G.object_id_patterns().items():
            if obj_id.startswith(prefix):
                obj_type = source
    if obj_type:
        url = G.url_for_source(obj_type)
        if url:
            return url + obj_id



def dimensions_url_search(keywords_list_as_string):
    "Returns a valid keyword search URL for Dimensions"
    q = """https://app.dimensions.ai/discover/publication?search_text={}&search_type=kws&search_field=full_search"""
    from urllib.parse import quote   
    s = quote(keywords_list_as_string)  
    return q.format(s)




def dsl_escape(stringa, all=False):   
    """
    Helper for escaping the full-text inner query string, when it includes quotes. Usage:

    `search publications for "{dsl_escape(complex_q)}" return publications`

    EG imagine the query string:
    '"2019-nCoV" OR "COVID-19" OR "SARS-CoV-2" OR (("coronavirus"  OR "corona virus") AND (Wuhan OR China))'
    
    In Python, if you want to embed it into a DSL query, it has to become:
    '\\"2019-nCoV\\" OR \\"COVID-19\\" OR \\"SARS-CoV-2\\" OR ((\\"coronavirus\\"  OR \\"corona virus\\") AND (Wuhan OR China))'

    NOTE by default only quotes as escaped. If you want to escape all special chars, pass all=True, eg

    > dsl_escape('Solar cells: a new technology?', True)
    > 'Solar cells\\: a new technology?'

    See also: https://docs.dimensions.ai/dsl/language.html#for-search-term
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
