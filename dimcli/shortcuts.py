"""
NOTE this module is deprecated and will be removed in future versions.

Use instead dimcli.utils 
"""


from . import *
from .core.utils import chunks_of, normalize_key, dimensions_url, google_url, save2File, exists_key_in_dicts_list, dsl_escape



def dslquery(query_string):
    """shortcut for running a query - meant to be used only within interactive computing environments
    """
    from .core.auth import is_logged_in
    if is_logged_in():
        dsl = Dsl()
        res = dsl.query(query_string, verbose=True)
        return res


def dslquery_json(query_string):
    """shortcut for backward compatibility 
    Same as above but returns raw JSON instead of Api.DslDataset object

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




def extract_concepts(text, with_scores=True, as_df=True):
    """wrapper for the `extract_concepts` function
    https://docs.dimensions.ai/dsl/functions.html#function-extract-concepts
    """
    from .core.auth import is_logged_in
    if is_logged_in():
        dsl = Dsl()
        _score = 'true' if with_scores else 'false'
        if as_df:
            return dsl.query(f"""extract_concepts("{text}", return_scores={_score})""").as_dataframe()
        else:
            return dsl.query(f"""extract_concepts("{text}", return_scores={_score})""")




def extract_grants(grant_number, fundref="", funder_name=""):
    """wrapper for the `extract_grants` function
    https://docs.dimensions.ai/dsl/functions.html#function-extract-grants
    NOTE either fundref or funder_name needs to be provided
    """
    from .core.auth import is_logged_in
    if is_logged_in():
        dsl = Dsl()
        if fundref:
            return dsl.query(f"""extract_grants(grant_number="{grant_number}", fundref="{fundref}")""")
        else:
            return dsl.query(f"""extract_grants(grant_number="{grant_number}", funder_name="{funder_name}")""")



def extract_classification(title, abstract, system="", verbose=True):
    """wrapper for the `classify` function
    https://docs.dimensions.ai/dsl/functions.html#function-classify

    `system` must be an acronym from the supported classification systems:

    * Fields of Research (FOR)
    * Research, Condition, and Disease Categorization (RCDC)
    * Health Research Classification System Health Categories (HRCS_HC)
    * Health Research Classification System Research Activity Classifications (HRCS_RAC)
    * Health Research Areas (HRA)
    * Broad Research Areas (BRA)
    * ICRP Common Scientific Outline (ICRP_CSO)
    * ICRP Cancer Types (ICRP_CT)
    * Units of Assessment (UOA)
    * Sustainable Development Goals (SDG)

    """
    from .core.auth import is_logged_in
    classifications = ["FOR", "RCDC", "HRCS_HC", "HRCS_RAC", "HRA", "BRA", "ICRP_CSO", "ICRP_CT", "UOA", "SDG"]
    if is_logged_in():
        dsl = Dsl()
        if system:
            return dsl.query(f"""classify(title="{dsl_escape(title)}", 
                                        abstract="{dsl_escape(abstract)}", 
                                        system="{system}")""")
        else:
            if verbose: print(f"""No system provided, using all known systems ({len(classifications)} queries). Warning: This may lead to 'too many API queries' errors.""")
            d = {}
            for classifier in classifications:
                new = dsl.query(f"""classify(title="{dsl_escape(title)}", 
                                        abstract="{dsl_escape(abstract)}", 
                                        system="{classifier}")""").json
                d.update(new)
            return d