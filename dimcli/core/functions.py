"""
Python wrappers for the DSL functions.
See also: https://docs.dimensions.ai/dsl/functions.html
NOTE: these objects are attached to the top level ``dimcli.functions`` module. So you can load them as follows:

>>> from dimcli.functions import *
"""

import json
import pandas as pd
import click
from tqdm import tqdm
import time

from .api import Dsl
from .auth import is_logged_in_globally as is_logged_in

from ..utils.dim_utils import dsl_escape


def extract_concepts(text, scores=True, as_df=True):
    """Python wrapper for the DSL function `extract_concepts`.

    Extract concepts from any text. Text input is processed and extracted concepts are returned as an array of strings ordered by their relevance. See also: https://docs.dimensions.ai/dsl/functions.html#function-extract-concepts

    Parameters
    ----------
    text : str
        The text paragraphs to extract concepts from. 
    scores : bool, optional
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
        _score = 'true' if scores else 'false'
        if as_df:
            df = dsl.query(f"""extract_concepts("{text}", return_scores={_score})""").as_dataframe()
            if not scores:
                df.rename(columns={ df.columns[0]: "concepts" }, inplace = True)
            return df
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
            if verbose: print(f"""No system provided, using all known systems ({len(classifications)} queries).""")
            d = {}
            for classifier in classifications:
                new = dsl.query(f"""classify(title="{dsl_escape(title)}", 
                                        abstract="{dsl_escape(abstract)}", 
                                        system="{classifier}")""").json
                d.update(new)
                time.sleep(1)
            return d




def extract_affiliations(affiliations, as_json=False):
    """Python wrapper for the DSL function `extract_affiliations`. 

    This function returns GRID affiliations either using structured or unstructured input. Up to 200 input objects are allowed per request. See also: https://docs.dimensions.ai/dsl/functions.html#function-extract-affiliations

    The input argument ``affiliations`` can be one of the following:

    * a string, representing a single **unstructured** 'affiliation', eg

         "new york university"

    * a list of strings, representing **unstructured** 'affiliations', eg

        ["new york university", "london college of surgeons"]

    * a list of dictionaries of **unstructured** 'affiliations' data, eg 
        
        [{"affiliation": "london college"}, {"affiliation": "new york university"}]
    
    * a list of dictionaries of **structured** 'affiliations' data, eg 

        [{"name":"london college cambridge",
        "city":"",
        "state":"",
        "country":""},
        {"name":"milano bicocca",
        "city":"Milano",
        "state":"",
        "country":"Italy"}
        ]

    By default, the JSON results are flattened and returned as a pandas dataframe.

    **NOTE** internally this function always uses the 'batch processing' version of the API. The optional argument `results` is currently not supported (and hence defaults to 'basic').

    


    Parameters
    ----------
    affiliations : str or list or dict
        The raw affiliation data to process. 
    as_json : bool, optional
        Return raw JSON encoded as a Python dict (instead of a pandas dataframe, by default). 

    Returns
    -------
    pandas.DataFrame or dict 
        A pandas dataframe containing a flattened representation of the JSON results. 

    Example
    --------
    >>> from dimcli.functions import extract_affiliations
    >>> extract_affiliations("stanford medical center")
    n  affiliation_part        grid_id          grid_name grid_city  grid_state   grid_country  requires_review geo_country_id geo_country_name geo_country_code geo_state_id geo_state_name geo_state_code geo_city_id geo_city_name
    0  stanford medical center  grid.240952.8  Stanford Medicine  Stanford  California  United States             True        6252001    United States               US      5332921     California          US-CA     5398563      Stanford    
    >>> data = [{"affiliation": "london college"}, {"affiliation": "new york university"}]
    >>> extract_affiliations(data)
    n  affiliation_part        grid_id            grid_name grid_city grid_state    grid_country  requires_review geo_country_id geo_country_name geo_country_code geo_state_id geo_state_name geo_state_code geo_city_id  geo_city_name
    0  london college  grid.499389.6   The London College    London       None  United Kingdom             True        2635167   United Kingdom               GB      6269131        England           None     2643743         London
    1  new york university  grid.137628.9  New York University  New York   New York   United States            False        6252001    United States               US      5128638       New York          US-NY     5128581  New York City
    """
    if not is_logged_in(): return
    dsl = Dsl()
    affiliation_type = "UNSTRUCTURED"
    
    if type(affiliations) == str:
        input_data = [{"affiliation": affiliations}]
    
    elif type(affiliations) == list and type(affiliations[0]) == str:
        input_data = [{"affiliation": x} for x in affiliations]
        
    elif type(affiliations) == list and type(affiliations[0]) == dict:
        if "affiliation" in affiliations[0]:
            input_data = affiliations
        elif "name" in affiliations[0]:
            affiliation_type = "STRUCTURED"
            input_data = affiliations
        else:
            raise Exception("Dictionary is badly formatted. Cannot find 'affiliation', nor 'name' keys. See https://docs.dimensions.ai/dsl/functions.html#function-extract-affiliations")

    #        
    # == main DSL query == 
    #        
    # Saving utf-8 texts in json.dumps as UTF8, not as \u escape sequence
    # https://stackoverflow.com/questions/18337407/saving-utf-8-texts-in-json-dumps-as-utf8-not-as-u-escape-sequence
    output = dsl.query(f"""extract_affiliations(json={json.dumps(input_data, ensure_ascii=False)}, results="basic")""")  # same query for both struct and unstruct
    
    if as_json:
        return output.json
    elif "results" in output.json: # return DF
        if affiliation_type == "STRUCTURED":
            temp = pd.json_normalize(output.json['results'],  errors='ignore')
        if affiliation_type == "UNSTRUCTURED": 
            temp = pd.json_normalize(output.json['results'],  'matches', errors='ignore')
        temp = temp.explode("institutes")
        temp = temp.explode("geo.countries")
        temp = temp.explode("geo.states")
        temp = temp.explode("geo.cities")
        # institutes fields
        temp['grid_id'] = temp['institutes'].apply(lambda x: x['institute']['id'] if type(x) == dict else None)
        temp['grid_name'] = temp['institutes'].apply(lambda x: x['institute']['name'] if type(x) == dict else None)
        temp['grid_city'] = temp['institutes'].apply(lambda x: x['institute']['city'] if type(x) == dict else None)
        temp['grid_state'] = temp['institutes'].apply(lambda x: x['institute']['state'] if type(x) == dict else None)
        temp['grid_country'] = temp['institutes'].apply(lambda x: x['institute']['country'] if type(x) == dict else None)
        temp['requires_review'] = temp['institutes'].apply(lambda x: x['metadata']['requires_manual_review'] if type(x) == dict else None if type(x) == dict else None)
        # geo fields - country
        temp['geo_country_id'] = temp['geo.countries'].apply(lambda x: str(x['geonames_id']) if type(x) == dict else None)
        temp['geo_country_name'] = temp['geo.countries'].apply(lambda x: x['name'] if type(x) == dict else None)
        temp['geo_country_code'] = temp['geo.countries'].apply(lambda x: x['code'] if type(x) == dict else None)
        # state
        temp['geo_state_id'] = temp['geo.states'].apply(lambda x: str(x['geonames_id']) if type(x) == dict else None)
        temp['geo_state_name'] = temp['geo.states'].apply(lambda x: x['name'] if type(x) == dict else None)
        temp['geo_state_code'] = temp['geo.states'].apply(lambda x: x['code'] if type(x) == dict else None)
        # city
        temp['geo_city_id'] = temp['geo.cities'].apply(lambda x: str(x['geonames_id']) if type(x) == dict else None)
        temp['geo_city_name'] = temp['geo.cities'].apply(lambda x: x['name'] if type(x) == dict else None)
        # drop cols
        temp = temp.drop(columns=['institutes', 'geo.countries', 'geo.states', 'geo.cities'])
        return temp





# ===
# extract_affiliations sample raw outputs 
# ===


# API OUTPUT for UNSTRUCTURED SEARCH

# {
#     "results": [
#         {
#             "matches": [
#                 {
#                     "affiliation_part": "london college cambridge",
#                     "institutes": [
#                         {
#                             "institute": {
#                                 "id": "grid.499389.6",
#                                 "name": "The London College",
#                                 "city": "London",
#                                 "state": None,
#                                 "country": "United Kingdom"
#                             },
#                             "metadata": { "requires_manual_review": True }
#                         }
#                     ],
#                     "geo": {
#                         "cities": [
#                             { "geonames_id": 2643743, "name": "London" }
#                         ],
#                         "states": [
#                             {
#                                 "geonames_id": 6269131,
#                                 "name": "England",
#                                 "code": None
#                             }
#                         ],
#                         "countries": [
#                             {
#                                 "geonames_id": 2635167,
#                                 "name": "United Kingdom",
#                                 "code": "GB"
#                             }
#                         ]
#                     }
#                 }
#             ],
#             "input": { "affiliation": "london college cambridge" }
#         }]
# }

# API OUTPUT for STRUCTURED SEARCH

# {
#     "results": [
#         {
#             "institutes": [
#                 {
#                     "institute": {
#                         "id": "grid.499389.6",
#                         "name": "The London College",
#                         "city": "London",
#                         "state": None,
#                         "country": "United Kingdom"
#                     },
#                     "metadata": { "requires_manual_review": True }
#                 }
#             ],
#             "geo": {
#                 "cities": [{ "geonames_id": 2643743, "name": "London" }],
#                 "states": [
#                     { "geonames_id": 6269131, "name": "England", "code": None }
#                 ],
#                 "countries": [
#                     {
#                         "geonames_id": 2635167,
#                         "name": "United Kingdom",
#                         "code": "GB"
#                     }
#                 ]
#             },
#             "input": {
#                 "name": "london college cambridge",
#                 "city": "",
#                 "state": "",
#                 "country": ""
#             }
#         }
#     ]
# }





def identify_experts(abstract, max_concepts=15, connector="OR", conflicts=None, extra_dsl="where year >= 2010", source="publications", verbose=False):
    """Python wrapper for the expert identification workflow. See also https://docs.dimensions.ai/dsl/expert-identification.html

    This wrapper provide a simpler version of the expert identification API. It is meant to be a convenient alternative for basic queries. For more options, it is advised to use the API directly. 

    Parameters
    ----------
    abstract : str
        The abstract text used to identify experts. Concepts are automatically extracted from it.
    max_concepts : int, optional
        The maximum number of concepts to use for the identification. By default, this is 15. Concepts are ranked by relevance.
    connector : str, optional
        The logical connector used in the concepts query. Should be either 'AND', or 'OR' (=default).
    conflicts : list, optional
        A list of Dimensions researchers IDs used to determine overlap / conflicts of interest.
    extra_dsl : str, optional
        A DSL clause to add after the main concepts search statement. Default is ``where year >= 2010``.
    source : str, optional
        The DSL source to derive experts from. Either 'publications' (default) or 'grants'.  
    verbose : bool, optional
        Verbose mode, by default False

    Returns
    -------
    pandas.Dataframe
        A dataframe containing experts details, including the dimensions URL of the experts. 

    Example
    --------
    >>> from dimcli.functions import identify_experts
    >>> identify_experts("Moon landing paved the way for supercomputers becoming mainstream", verbose=True)
    Concepts extracted: 5
    Query:
    "
    identify experts
        from concepts "\"landing\" OR \"way\" OR \"mainstream\" OR \"moon landing\" OR \"supercomputers\""
        using publications where year >= 2010
    return experts[id+first_name+last_name+dimensions_url-obsolete] 
    "
    Experts found: 20
    [..experts list..]
    """       

    if not is_logged_in(): return
    dsl = Dsl()

    connector = connector.strip()
    if connector not in ["AND", "OR"]:
        raise Exception("Invalid connector: must be either 'AND' or 'OR'.")

    source = source.strip()
    if source not in ["publications", "grants"]:
        raise Exception("Invalid source: must be either 'publications' or 'grants'.")
        
    if extra_dsl=="where year >= 2010" and source=="grants":
        extra_dsl="where start_year >= 2010"

    conflicts_query = ""
    if conflicts:
        conflicts_query = f"""annotate coauthorship, organizational overlap
            with {json.dumps(conflicts)}"""
    
    # get concepts
    df = extract_concepts(abstract)
    if verbose: click.secho(f"Concepts extracted: {len(df)}")
    if len(df) == 0: 
        return []
    concepts_list = df.concept[:max_concepts]
    concepts_list_query = f" {connector} ".join(['"%s"' % x for x in concepts_list])
    
    
    # get experts
    experts_fields = "id+first_name+last_name+total_publications+total_grants+first_publication_year+orcid_id+dimensions_url-obsolete"
    thequery = f"""
        identify experts
            from concepts "{dsl_escape(concepts_list_query)}"
            using {source} {extra_dsl}
        return experts[{experts_fields}] {conflicts_query}
        """
    
    if verbose: click.secho("Query:\n======" + thequery + "\n======")
    results = dsl.query(thequery)

    if "experts" in results.json:
        if verbose: click.secho(f"Experts found: {len(results.experts)}" )
        df = results.as_dataframe()
        df = df[ [ col for col in df.columns if col != 'dimensions_url' ] + ['dimensions_url'] ]
        return df
    else:
        if verbose: click.secho(f"Experts found: 0" )
        return []






def build_reviewers_matrix(abstracts, candidates, max_concepts=15, connector="OR", source="publications", verbose=False):
    """Generates a matrix of candidate reviewers for abstracts, using the expert identification workflow. See also https://docs.dimensions.ai/dsl/expert-identification.html

    If the input abstracts include identifiers, then those are used in the resulting matrix. 
    Alternatively, a simple list of strings as input will result in a matrix where the identifiers are auto-generated from the abstracts order (first one is 1, etc..).
    
    Parameters
    ----------
    abstracts : list
        The list of abstracts used for matching reviewers. Should be either a list of strings, or a list of dictionaries ``{'id' : '{unique-ID}', 'text' : '{the-abstract}'}`` including a unique identifier for each abstract.  
    candidates : list
        A list of Dimensions researchers IDs. 
    max_concepts : int, optional
        The maximum number of concepts to use for the matching. By default, this is 15. Concepts are ranked by relevance.
    connector : str, optional
        The logical connector used in the concepts query. Should be either 'AND', or 'OR' (=default).
    source : str, optional
        The DSL source to derive experts from. Either 'publications' (default) or 'grants'.  
    verbose : bool, optional
        Verbose mode, by default False

    Returns
    -------
    pandas.Dataframe
        A dataframe containing experts details, including the dimensions URL of the experts. 

    Example
    --------
    >>> from dimcli.functions import build_reviewers_matrix
    >>> abstracts = [
    ...:     {
    ...:     'id' : 'A1',
    ...:     'text' : We describe monocrystalline graphitic films, which are a few atoms thick but are nonetheless stable under ambient conditions,
    ...: metallic, and of remarkably high quality. The films are found to be a two-dimensional semimetal with a tiny overlap between
    ...: valence and conductance bands, and they exhibit a strong ambipolar electric field effect such that electrons and
    ...: holes in concentrations up to 10 per square centimeter and with room-temperature mobilities of approximately 10,000 square
    ...: centimeters per volt-second can be induced by applying gate voltage."
    ...:     },
    ...:     {
    ...:     'id' : "A2",
    ...:     'text' : ""The physicochemical properties of a molecule-metal interface, in principle, can play a significant role in tuning the electronic properties
    ...: of organic devices. In this report, we demonstrate an electrode engineering approach in a robust, reproducible molecular memristor that
    ...: enables a colossal tunability in both switching voltage (from 130 mV to 4 V i.e. >2500% variation) and current (by ~6 orders of magnitude).
    ...: This provides a spectrum of device design parameters that can be “dialed-in” to create fast, scalable and ultralow energy organic
    ...: memristors optimal for applications spanning digital memory, logic circuits and brain-inspired computing."
    ...:     }
    ...: ]
    ...:
    >>> candidates = ["ur.01146544531.57", "ur.011535264111.51", "ur.0767105504.29",
    ...:               "ur.011513332561.53", "ur.01055006635.53"]
    >>> build_reviewers_matrix(abstracts, candidates)
               researcher         A1        A2
    0   ur.01146544531.57   8.185277  0.000000
    1  ur.011535264111.51   8.203130  0.000000
    2    ur.0767105504.29   8.686363  2.626348
    3  ur.011513332561.53  12.920304  1.551920
    4   ur.01055006635.53   6.756862  1.797738
    """    


    if type(abstracts) == list and type(abstracts[0]) == str:
        abstracts = [{'id' : x+1, 'text' : y} for x,y in enumerate(abstracts)]
    elif type(abstracts) == list and type(abstracts[0]) == dict and 'id' in abstracts[0]:
        pass
    else:
        raise Exception("Invalid abstracts data: must be either a list of strings, or a list of dictionaries.") 


    if type(candidates) == list and candidates[0].startswith("ur."):
        pass
    else:
        raise Exception("Invalid candidates data: must be a list of Dimensions researchers IDs.") 

    
    # boostrap matrix table
    matrix = pd.DataFrame(columns=["researcher"])
    matrix["researcher"] = candidates

    # helper method: get score from candidates dataframe 
    def _get_score(experts_df, resid):
        try:
            return experts_df.query(f"id=='{resid}'").iloc[0]['score']
        except:
            return 0

    # finally..
    for abstract in tqdm(abstracts):
        results = identify_experts(abstract['text'], 
                                   max_concepts = max_concepts,
                                   connector = connector,
                                   source=source,
                                   extra_dsl=f"where researchers in {json.dumps(candidates)}", 
                                   verbose=verbose)
        if len(results):
            matrix[abstract['id']] = matrix["researcher"].apply(lambda x: _get_score(results, x))
        time.sleep(1)

    return matrix