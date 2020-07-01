"""
Wrappers around DSL functions

https://docs.dimensions.ai/dsl/functions.html
"""

from .utils import dsl_escape
from .api import Dsl
from .auth import is_logged_in


def extract_concepts(text, with_scores=True, as_df=True):
    """wrapper for the `extract_concepts` function
    https://docs.dimensions.ai/dsl/functions.html#function-extract-concepts
    """
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