import json
import pandas as pd
try:
    from pandas import json_normalize
except:
    from pandas.io.json import json_normalize

from ..utils.misc_utils import normalize_key, exists_key_in_dicts_list
from ..utils.dim_utils import  dimensions_styler
from ..utils.converters import *

class DfFactory(object):
    """
    Helper class containing methods for creating dataframes from API JSON

    The 'data' passed to its methods is always JSON/DICT data 
    """

    def __init__(self, good_data_keys=[]):
        self.good_keys = good_data_keys



    def _reorder_cols(self, df):
        """Reorder df columns based on Dimensions data. EG Try to have ID and TITLE always at the beginning.
        Goal is to improve readability of data returned. Currently used only with `df_simple`."""

        FIELDS = ["id", "title", "name", "first_name", "last_name"]

        for f in reversed(FIELDS):
            if f in df:
                df.insert(0, f, df.pop(f))
        
        return df


    def df_simple(self, data, key, links=False, nice=False):
        """Return inner json as a pandas dataframe

        Parameters
        ----------
        data: dict
            dict representation of JSON data from the DSL 
        key: string
            JSON key to be used to extract dataframe data from. If key is empty, the first available JSON key (eg 'publications') is used to determine what data should be turned into a dataframe.
        links: bool, False
            control to return a special dataframe with hyperlinks for Jupyter environments
         
        """

        output = pd.DataFrame()
        valid_key = False

        if key and (key in self.good_keys):
            valid_key = key
        elif key and (key not in self.good_keys):
            print(f"[Warning] Dataframe cannot be created: invalid key. Should be one of {self.good_keys}")
        elif not key and self.good_keys:
            if len(self.good_keys) > 1:
                print(f"[Warning] Dataframe created from first available key, but more than one JSON key found: {self.good_keys}")
            valid_key = self.good_keys[0]
        else:
            pass 

        if valid_key:
            if type(data[valid_key]) == list:
                if data[valid_key] and type(data[valid_key][0]) == dict:
                    output = json_normalize(data[valid_key], errors="ignore")
                else: # return empty list, or list of strings/numbers  
                    output = pd.DataFrame.from_dict(data[valid_key]) 
            elif type(data[valid_key]) == dict: # top level dict, use keys as index
                output = pd.DataFrame.from_dict(data[valid_key], orient="index", columns=[valid_key]) 
            else: # no list, then make one and try to return everything
                output = pd.DataFrame.from_dict([data])

        # move ID and Title at the beginning, always
        output = self._reorder_cols(output)

        if nice:
            if valid_key == "publications":
                output = DslPubsConverter(output).run()
            elif valid_key == "grants":
                output = DslGrantsConverter(output).run()
            elif valid_key == "patents":
                output = DslPatentsConverter(output).run()
            elif valid_key == "policy_documents":
                output = DslPolicyDocumentsConverter(output).run()
            elif valid_key == "clinical_trials":
                output = DslClinicaltrialsConverter(output).run()
            elif valid_key == "outputsets":
                output = DslDatasetsConverter(output).run()
            elif valid_key == "reports":
                output = DslReportsConverter(output).run()
            elif valid_key == "source_titles":
                output = DslSourceTitlesConverter(output).run()
            elif valid_key == "organizations":
                output = DslOrganizationsConverter(output).run()
            elif valid_key == "researchers":
                output = DslResearchersConverter(output).run()
            else:
                pass
            
        if links:
            output = dimensions_styler(output, valid_key)

        return output



    def df_authors(self, data, links=False):
        """Utility 
        Returns inner json as a pandas dataframe, exposing authors + pubId.
        List of affiliations per each author are not broken down and are returned as JSON. 
        So in essence you get one row per author.

        NOTE this method works only for publications searches -and it's clever enough to know if `authors` or `author_affiliations` (deprecated) field is used.

        Each publication.author_affiliations object has a nested list structure like this:
        ```
        [[{'first_name': 'Laura',
            'last_name': 'Pasin',
            'orcid': '',
            'current_organization_id': '',
            'researcher_id': '',
            'affiliations': [{'name': 'Department of Anesthesia and Intensive Care, Ospedale S. Antonio, Via Facciolati, 71, Padova, Italy'}]},
            {'first_name': 'Sabrina',
            'last_name': 'Boraso',
            'orcid': '',
            'current_organization_id': '',
            'researcher_id': '',
            'affiliations': [{'name': 'Department of Anesthesia and Intensive Care, Ospedale S. Antonio, Via Facciolati, 71, Padova, Italy'}]},
            {'first_name': 'Ivo',
            'last_name': 'Tiberio',
            'orcid': '',
            'current_organization_id': '',
            'researcher_id': '',
            'affiliations': [{'name': 'Department of Anesthesia and Intensive Care, Ospedale S. Antonio, Via Facciolati, 71, Padova, Italy'}]}]]
        ```

        """
        output = pd.DataFrame()

        if 'publications' in self.good_keys:

            if exists_key_in_dicts_list(data['publications'], "author_affiliations"):
                FIELD = "author_affiliations"
            elif exists_key_in_dicts_list(data['publications'], "authors"):
                FIELD = "authors"
            else:
                FIELD = ""

            if FIELD == "author_affiliations":
                # simplify deep nested dict structure for deprecated field 
                for x in data['publications']:
                    if 'author_affiliations' in x and x['author_affiliations']:  # if key exists and contents are not empty eg '[]'
                        if type(x['author_affiliations'][0]) == list: # then break down nested dict structure
                            x['author_affiliations'] = x['author_affiliations'][0]
                        elif type(x['author_affiliations'][0]) == dict: # = it's already been broken down
                            pass
                    else: # put in default empty element
                        x['author_affiliations'] = []
            elif FIELD == "authors":
                normalize_key("authors", data['publications'], [])
            
            if FIELD:
                output = json_normalize(data['publications'], record_path=[FIELD], meta=['id'], errors='ignore')
                output.rename(columns={"id": "pub_id"}, inplace=True)
        else:
            print(f"[Warning] Dataframe cannot be created as 'publications' were not found in data. Available: {self.good_keys}")

        if links:
            output = dimensions_styler(output, "publications")

        return output


    def df_authors_affiliations(self, data, links=False):
        """Utility method
        return inner json as a pandas dataframe, exposing authors + affiliations + pubId
        affiliations ARE broken down and are returned as JSON 
        So one gets one row per affiliation (+1 row per author if having more than one affiliation)

        NOTE this method builds on self.df_authors()
        """
        
        authors = self.df_authors(data)
        if len(authors):
            affiliations = json_normalize(json.loads(authors.to_json(orient='records')), 
                            record_path=['affiliations'], 
                            meta=['pub_id', 'researcher_id', 'first_name', 'last_name'], 
                            record_prefix='aff_',
                            errors="ignore")
        else:
            affiliations = authors # empty df
        affiliations.fillna('', inplace=True) # 2019-09-30: simplifies subsequent operations
        
        if links:
            affiliations = dimensions_styler(affiliations, "publications")
        
        return affiliations




    def df_concepts(self, data, key, links=False):
        """from a list of publications or grants including concepts, return a DF with one line per concept
        Enrich the dataframe with scores and other metrics.
        """

        FIELD_NAME = "concepts"
        FIELD_NAME_SCORES = "concepts_scores"
        ROUNDING = 5

        if not ('publications' in self.good_keys) and not ('grants' in self.good_keys): 
            s = f"Dataframe can be created only with searches returning 'publications' or 'grants' . Available: {self.good_keys}"
            raise Exception(s)

        concepts = self.df_simple(data, key)

        if (FIELD_NAME not in concepts.columns) and (FIELD_NAME_SCORES not in concepts.columns):
            s = f"Dataframe requires raw concepts data, but no 'concepts' or 'concepts_scores' column was not found in: {concepts.columns.to_list()}"
            raise Exception(s)             

        if not 'id' in concepts.columns:
            s = f"Dataframe requires an 'id' column for counting concepts, which was not found in: {concepts.columns.to_list()}"
            raise Exception(s)   

        if FIELD_NAME_SCORES in concepts.columns:
            # use `concepts_scores` field preferably

            df = concepts.explode(FIELD_NAME_SCORES)
            df.dropna(subset=[FIELD_NAME_SCORES], inplace=True)  # remove rows if there is no concept
            df.reset_index(inplace=True, drop=True)
            original_cols = [x for x in df.columns.to_list() if x != FIELD_NAME_SCORES]
            df = df.drop(FIELD_NAME_SCORES, axis=1).assign(**pd.json_normalize(df[FIELD_NAME_SCORES]))  # unpack dict with new columns
            df = df[df.relevance != 0]  # remove 0-relevance scores
            df['relevance'] = df['relevance'].round(ROUNDING)
            df.rename(columns={"relevance": "score"}, inplace=True) 
            df['frequency'] = df.groupby('concept')['concept'].transform('count')
            df['concepts_count'] = df.groupby("id")['concept'].transform('size')
  
        else: 
            # with traditional 'concepts', scores are simulated

            df = concepts.explode(FIELD_NAME)
            original_cols = [x for x in df.columns.to_list() if x != FIELD_NAME]
            df.dropna(subset=[FIELD_NAME], inplace=True) # remove rows if there is no concept
            df.rename(columns={FIELD_NAME: "concept"}, inplace=True)
            df['frequency'] = df.groupby('concept')['concept'].transform('count')
            df['concepts_count'] = df.groupby("id")['concept'].transform('size')
            ranks = df.groupby('id').cumcount()+1
            # scores = normalized rank from 0 to 1, where 1 is the highest rank
            df['score'] = ((df['concepts_count']+1) - ranks) / df['concepts_count']
            df['score'] = df['score'].round(ROUNDING)

        # finally
        df['score_avg'] = df.groupby('concept')['score'].transform('mean').round(ROUNDING)
        df.reset_index(drop=True, inplace=True)
        
 
        out_cols = original_cols + ['concepts_count', 'concept', 'score', 'frequency', 'score_avg' ]
        output = df[out_cols]
        
        if links:
            output = dimensions_styler(output)
        
        return output





    def df_grant_funders(self, data, links=False):
        """Utility method: return inner json as a pandas dataframe, for grants funders
        """
        output = pd.DataFrame()
        FIELD = "funders"

        if 'grants' in self.good_keys:    
            normalize_key(FIELD, data['grants'], [])   
            output = json_normalize(data['grants'], record_path=[FIELD], meta=['id', 'title', 'start_date', 'end_date'], meta_prefix="grant_", errors='ignore')
        else:
            print(f"[Warning] Dataframe cannot be created as 'grants' were not found in data. Available: {self.good_keys}")

        if links:
            output = dimensions_styler(output, "grants")

        return output

    def df_grant_investigators(self, data, links=False):
        """Utility method: return inner json as a pandas dataframe, for grants investigators 
        """
        output = pd.DataFrame()
        FIELD = "investigators"

        if 'grants' in self.good_keys:    
            normalize_key(FIELD, data['grants'], [])
            output = json_normalize(data['grants'], record_path=[FIELD], meta=['id', 'title', 'start_date', 'end_date'], meta_prefix="grant_", errors='ignore')
        else:
            print(f"[Warning] Dataframe cannot be created as 'grants' were not found in data. Available: {self.good_keys}")

        if links:
            output = dimensions_styler(output, "grants")

        return output

    def df_grant_investigators_affiliations(self, data, links=False):
        """Utility method
        return inner json as a pandas dataframe, exposing investigators + affiliations + pubId
        affiliations ARE broken down and are returned as JSON 
        So one gets one row per affiliation (+1 row per investigators if having more than one affiliation)

        NOTE this method builds on self.df_grant_investigators()
        """
        investigators = self.df_grant_investigators(data)
        if len(investigators):
            affiliations = json_normalize(json.loads(investigators.to_json(orient='records')), 
                                                record_path=['affiliations'], 
                                                meta=['id', 'first_name', 'last_name',  'role', 'grant_id', 'grant_title', 'grant_start_date', 'grant_end_date' ], 
                                                record_prefix='aff_',
                                                errors="ignore")
        else:
            affiliations = investigators # empty df
        affiliations.fillna('', inplace=True) # 2019-09-30: simplifies subsequent operations

        if links:
            affiliations = dimensions_styler(affiliations, "grants")

        return affiliations


