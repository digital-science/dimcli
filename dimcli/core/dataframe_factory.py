import json
import pandas as pd
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
        "utility method: return inner json as a pandas dataframe"

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


    def df_concepts(self, data, max_per_pub=100):
        "from a list of publications including concepts, return a DF with one line per concept"

        output = pd.DataFrame(columns=['name', 'position', 'score', 'pubid', 'year', 'title']) 
        FIELD = "concepts"

        if 'publications' in self.data_keys:    
            for pub in data['publications']:
                if 'concepts' in pub and pub['concepts']:
                    concepts = pub['concepts'][:max_per_pub]
                    llen = len(concepts)
                    positions = list(range(1, llen+1))
                    scores = list(range(1, llen+1))[::-1] # highest score first, reverse list
                    scores = [float('%.2f'%(x / llen)) for x in scores] # normalize by items in list
                    pubids = [pub.get("id", None)] * llen
                    years = [pub.get("year", None)] * llen
                    titles = [pub.get("title", None)] * llen
                    z = list(zip(concepts, positions, scores, pubids, years, titles))
                    d = [{'name': a, 'position': b, 'score': c, 'pubid': d, 'year': e, 'title': f} for a,b,c,d,e,f in z]
                    output = output.append(d, sort=True)    
            # add correct data types
            output['position'] = pd.to_numeric(output['position'])
            output['score'] = pd.to_numeric(output['score'])
            # finally add another colum counting occurrences   
            output['frequency'] = output.groupby('name')['name'].transform('count')        
        else:
            print(f"[Warning] Dataframe cannot be created as 'publications' were not found in data. Available: {self.data_keys}")
        
        return output[['name', 'position', 'score', 'frequency', 'pubid', 'title', 'year']]



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




