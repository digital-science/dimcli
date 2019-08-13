import json
import pandas as pd
from pandas.io.json import json_normalize


class DfFactory(object):
    """
    Helper class containing methods for creating dataframes from API JSON

    The 'data' passed to its methods is always JSON/DICT data 
    """

    def __init__(self, good_data_keys=[]):
        self.gdk = good_data_keys


    def df_simple(self, data, key):
        "utility method: return inner json as a pandas dataframe"

        output = pd.DataFrame()
        
        if key and (key in self.gdk):
            output = json_normalize(data[key])
        elif key and (key not in self.gdk):
            print(f"[Warning] Dataframe cannot be created: invalid key. Should be one of {self.gdk}")
        elif not key and self.gdk:
            if len(self.gdk) > 1:
                print(f"[Warning] Dataframe created from first available key, but more than one JSON key found: {self.gdk}")
            output = json_normalize(data[self.gdk[0]])
        else:
            pass 

        return output


    def df_authors(self, data):
        """Utility method
        return inner json as a pandas dataframe, exposing authors + pubId
        affiliations are not broken down and are returned as JSON 
        So one gets one row per author

        NOTE this method works only for publications searches

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

        if 'publications' in self.gdk:
            # simplify dict structure 
            for x in data['publications']:
                if 'author_affiliations' in x and x['author_affiliations']:  # if key exists and contents are not empty eg '[]'
                    if type(x['author_affiliations'][0]) == list: # then break down nested dict structure
                        x['author_affiliations'] = x['author_affiliations'][0]
                    elif type(x['author_affiliations'][0]) == dict: # = it's already been broken down
                        pass
                else: # put in default empty element
                    x['author_affiliations'] = []
        
            output = json_normalize(data['publications'], record_path=['author_affiliations'], meta=['id'], errors='ignore')
            output.rename(columns={"id": "pub_id"}, inplace=True)
        else:
            print(f"[Warning] Dataframe cannot be created as 'publications' were not found in data. Available: {self.gdk}")

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
        return affiliations


    def df_grant_funders(self, data):
        """Utility method: return inner json as a pandas dataframe, for grants funders
        """
        output = pd.DataFrame()

        if 'grants' in self.gdk:       
            output = json_normalize(data['grants'], record_path=['funders'], meta=['id', 'title', 'start_date', 'end_date'], meta_prefix="grant_", errors='ignore')
        else:
            print(f"[Warning] Dataframe cannot be created as 'grants' were not found in data. Available: {self.gdk}")

        return output

    def df_grant_investigators(self, data):
        """Utility method: return inner json as a pandas dataframe, for grants investigators 
        """
        output = pd.DataFrame()

        if 'grants' in self.gdk:    
            if 'investigator_details' in data['grants'][0]:   
                output = json_normalize(data['grants'], record_path=['investigator_details'], meta=['id', 'title', 'start_date', 'end_date'], meta_prefix="grant_", errors='ignore')
            else:
                print(f"[Warning] Dataframe cannot be created as 'investigator_details' were not found in data. You need a query like this: search grants return grants[basics+investigator_details]")
        else:
            print(f"[Warning] Dataframe cannot be created as 'grants' were not found in data. Available: {self.gdk}")

        return output
