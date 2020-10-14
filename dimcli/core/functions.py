"""
Wrappers around DSL functions

https://docs.dimensions.ai/dsl/functions.html
"""

from .api import Dsl
from .auth import is_logged_in

from ..utils.utils_dimensions import dsl_escape


def extract_concepts(text, with_scores=True, as_df=True):
    """Python wrapper for the DSL function `extract_concepts`.

    Extract concepts from any text. Text input is processed and extracted concepts are returned as an array of strings ordered by their relevance. See also: https://docs.dimensions.ai/dsl/functions.html#function-extract-concepts

    Parameters
    ----------
    text : str
        The text paragraphs to extract concepts from. 
    with_scores : bool, optional
        Return the concepts scores as well, by default True
    as_df : bool, optional
        Return results as a pandas dataframe (instead of JSON), by default True

    Returns
    -------
    pandas.Dataframe or dimcli.DslDataset
        The list of concepts that have been extracted. 

    Example
    -------
    >>> from dimcli.functions import extract_concepts
    >>> extract_concepts("The impact of solar rays on the moon is not trivial.")
    n	concept	relevance
    0	impact	0.070622
    1	rays	0.062369
    2	solar rays	0.022934
    3	Moon	0.013245
    """
     

    if is_logged_in():
        dsl = Dsl()
        _score = 'true' if with_scores else 'false'
        if as_df:
            return dsl.query(f"""extract_concepts("{text}", return_scores={_score})""").as_dataframe()
        else:
            return dsl.query(f"""extract_concepts("{text}", return_scores={_score})""")




def extract_grants(grant_number, fundref="", funder_name=""):
    """Python wrapper for the DSL function `extract_grants`.

    Extract grant Dimensions ID from provided parameters. Grant number must be provided with either a fundref or a funder name as an argument. See also: https://docs.dimensions.ai/dsl/functions.html#function-extract-grants

    Parameters
    ----------
    grant_number : str
        The grant number/ID
    fundref : str, optional
        Fundref name    
    funder_name : str, optional
        Funder name

    Returns
    -------
    dimcli.DslDataset
        A Dimcli wrapper object containing JSON data. 

    Example
    -------
    >>> from dimcli.functions import extract_grants
    >>> extract_grants("R01HL117329",  fundref="100000050").json
    {'grant_id': 'grant.2544064'}
    """    
    if is_logged_in():
        dsl = Dsl()
        if fundref:
            return dsl.query(f"""extract_grants(grant_number="{grant_number}", fundref="{fundref}")""")
        else:
            return dsl.query(f"""extract_grants(grant_number="{grant_number}", funder_name="{funder_name}")""")



def extract_classification(title, abstract, system="", verbose=True):
    """Python wrapper for the DSL function `classify`.

    This function retrieves suggested classifications codes for any text. See also: https://docs.dimensions.ai/dsl/functions.html#function-classify

    NOTE `system` must be the acronym of one of the supported classification systems:

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

    Parameters
    ----------
    title : str
        The title of the document to classify.
    abstract : str
        The abstract of the document to classify.
    system : str, optional
        The classification system to use. Either an acronym from the supported classification systems, or null. If no system is provided, all systems are attempted in sequence (one query per system).
    verbose : bool, optional
        Verbose mode, by default True

    Returns
    -------
    dimcli.DslDataset
        A Dimcli wrapper object containing JSON data. 

    Example
    --------
    >>> from dimcli.functions import extract_classification
    >>> title="Burnout and intentions to quit the practice among community pediatricians: associations with specific professional activities"
    >>> extract_classification(title, "", "FOR").json
    {'FOR': [{'id': '3177', 'name': '1117 Public Health and Health Services'}]}
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