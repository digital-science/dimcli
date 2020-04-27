import json
import pandas as pd
try:
    from pandas import json_normalize
except:
    from pandas.io.json import json_normalize
from .utils import normalize_key, exists_key_in_dicts_list


class DfFactory(object):
    """
    Helper class containing methods for creating dataframes from API JSON

    The 'data' passed to its methods is always JSON/DICT data 
    """

    def __init__(self, good_data_keys=[]):
        self.data_keys = good_data_keys


    def df_simple(self, data, key):
        """Return inner json as a pandas dataframe
        If key is empty, the first available JSON key (eg 'publications') is used to determine
        what data should be turned into a dataframe. 
        """

        output = pd.DataFrame()
        
        if key and (key in self.data_keys):
            output = json_normalize(data[key])
        elif key and (key not in self.data_keys):
            print(f"[Warning] Dataframe cannot be created: invalid key. Should be one of {self.data_keys}")
        elif not key and self.data_keys:
            if len(self.data_keys) > 1:
                print(f"[Warning] Dataframe created from first available key, but more than one JSON key found: {self.data_keys}")
            output = json_normalize(data[self.data_keys[0]])
        else:
            pass 

        return output


    def df_authors(self, data):
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

        if 'publications' in self.data_keys:

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
            print(f"[Warning] Dataframe cannot be created as 'publications' were not found in data. Available: {self.data_keys}")
        return output


    def df_authors_affiliations(self, data):
        """Utility method
        return inner json as a pandas dataframe, exposing authors + affiliations + pubId
        affiliations ARE broken down and are returned as JSON 
        So one gets one row per affiliation (+1 row per author if having more than one affiliation)

        NOTE this method builds on self.df_authors()
        """
        
        authors = self.df_authors(data)
        if len(authors):
            affiliations = json_normalize(json.loads(authors.to_json(orient='records')), record_path=['affiliations'], 
               meta=['pub_id', 'researcher_id', 'first_name', 'last_name'], record_prefix='aff_')
        else:
            affiliations = authors # empty df
        affiliations.fillna('', inplace=True) # 2019-09-30: simplifies subsequent operations
        return affiliations


    def df_concepts(self, data, key):
        """from a list of publications or grants including concepts, return a DF with one line per concept
        Enrich the dataframe with scores and other metrics.
        """

        FIELD_NAME = "concepts"
        ROUNDING = 3

        if not ('publications' in self.data_keys) and not ('grants' in self.data_keys): 
            s = f"Dataframe can be created only with searches returning 'publications' or 'grants' . Available: {self.data_keys}"
            raise Exception(s)

        concepts = self.df_simple(data, key)

        if not 'concepts' in concepts.columns:
            s = f"Dataframe requires raw concepts data, but a 'concepts' column was not found in: {concepts.columns.to_list()}"
            raise Exception(s)             

        if not 'id' in concepts.columns:
            s = f"Dataframe requires an 'id' column for counting concepts, which was not found in: {concepts.columns.to_list()}"
            raise Exception(s)   

        df = concepts.explode(FIELD_NAME)
        original_cols = [x for x in df.columns.to_list() if x != FIELD_NAME]
        df.rename(columns={FIELD_NAME: "concept"}, inplace=True)
        df.dropna(inplace=True) # remove rows if there is no concept
        df['frequency'] = df.groupby('concept')['concept'].transform('count')
        df['concepts_count'] = df.groupby("id")['concept'].transform('size')
        ranks = df.groupby('id').cumcount()+1
        # scores = normalized rank from 0 to 1, where 1 is the highest rank
        df['score'] = ((df['concepts_count']+1) - ranks) / df['concepts_count']
        df['score'] = df['score'].round(ROUNDING)

        df['score_avg'] = df.groupby('concept')['score'].transform('mean').round(ROUNDING)

        df.reset_index(drop=True, inplace=True)

        out_cols = original_cols + ['concepts_count', 'concept', 'score', 'frequency', 'score_avg' ]
        return df[out_cols]


    def df_grant_funders(self, data):
        """Utility method: return inner json as a pandas dataframe, for grants funders
        """
        output = pd.DataFrame()
        FIELD = "funders"

        if 'grants' in self.data_keys:    
            normalize_key(FIELD, data['grants'], [])   
            output = json_normalize(data['grants'], record_path=[FIELD], meta=['id', 'title', 'start_date', 'end_date'], meta_prefix="grant_", errors='ignore')
        else:
            print(f"[Warning] Dataframe cannot be created as 'grants' were not found in data. Available: {self.data_keys}")

        return output

    def df_grant_investigators(self, data):
        """Utility method: return inner json as a pandas dataframe, for grants investigators 
        """
        output = pd.DataFrame()
        FIELD = "investigator_details"

        if 'grants' in self.data_keys:    
            normalize_key(FIELD, data['grants'], [])
            output = json_normalize(data['grants'], record_path=[FIELD], meta=['id', 'title', 'start_date', 'end_date'], meta_prefix="grant_", errors='ignore')
        else:
            print(f"[Warning] Dataframe cannot be created as 'grants' were not found in data. Available: {self.data_keys}")

        return output

    def df_grant_investigators_affiliations(self, data):
        """Utility method
        return inner json as a pandas dataframe, exposing investigators + affiliations + pubId
        affiliations ARE broken down and are returned as JSON 
        So one gets one row per affiliation (+1 row per investigators if having more than one affiliation)

        NOTE this method builds on self.df_grant_investigators()
        """
        
        investigators = self.df_grant_investigators(data)
        if len(investigators):
            affiliations = json_normalize(json.loads(investigators.to_json(orient='records')), record_path=['affiliations'], 
               meta=['id', 'first_name', 'last_name',  'role', 'grant_id', 'grant_title', 'grant_start_date', 'grant_end_date' ], record_prefix='aff_')
        else:
            affiliations = authors # empty df
        affiliations.fillna('', inplace=True) # 2019-09-30: simplifies subsequent operations
        return affiliations


