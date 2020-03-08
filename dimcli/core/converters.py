from .utils import dimensions_url


# ===========
# TESTING - UNSUPPORTED FEATURE
# ===========
#


class DfConverter(object):
    """
    Helper class containing methods for transforming JSON complex snippets to other formats.


    # ALGORITHM
    # iterate through all keys/columns in dataframe
    #
    # if column name == key in fields_mappings:
    #   apply all functions => generate new columns
    #   remove old column 
    # else if column value is list 
    #   break down list into semicolon delimited string
    #   replace old column
    #
    #  PS dimensions_url special case, we just add a new column without removing 'ID'
    #   also, it applies only to sources

    """

    def __init__(self, df, object_type="", verbose=True):

        self.df_original = df
        self.object_type = object_type
        # self.df_converted = df.copy()
        self.verbose = verbose

        self.columns_original = self.df_original.columns.to_list()
        if self.verbose: print("Columns are:", self.columns_original)

        # PS decided to not deal with DEPRECATED FIELDS!
        self.column_transformations = {
            # ('new_col_name', 'fun_name')
            'id' : 
                [('Publication ID' , '', ),  # duplicate == keep col
                 ('Dimensions URL' , 'convert_id_to_url', )],
            'abstract' : 
                [('Abstract' , '', )],
            'doi' : 
                [('DOI' , '', )],
            'pmid' : 
                [('PMID' , '', )],
            'pmcid' : 
                [('PMCID' , '', )],
            'title' : 
                [('Title' , '', )],
            'journal.title' : 
                [('Source title' , '', )],
            'journal.id' : 
                [('Source UID' , '', )],
            'publisher' : 
                [('Publisher' , '', )],
            'mesh_terms' : 
                [('MeSH terms', 'convert_list')],
            'date' : 
                [('Publication Date' , '', )],
            'year' : 
                [('PubYear' , '', )],
            'volume' : 
                [('Volume' , '', )],
            'issue' : 
                [('Issue' , '', )],
            'pages' : 
                [('Pagination' , '', )],
            'open_access_categories' : 
                [('Open Access', 'convert_dict_name')],
            'type' : 
                [('Publication Type' , '', )],
            'authors' : 
                [ ('Authors', 'convert_authors_to_names' ),
                  ('Corresponding Author', 'convert_authors_corresponding' ),
                  ('Authors Affiliations', 'convert_authors_affiliations' )],
            'research_orgs' : 
                [('Research Organizations - standardized', 'convert_dict_name'),
                 ('GRID IDs', 'convert_dict_ids'),
                 ('City of Research organization', 'convert_city_name'),
                #  ('State of Research organization', 'convert_state_name'),
                 ('Country of Research organization', 'convert_country_name'),
                 ],
            'funders' : 
                [('Funder', 'convert_dict_name')],
            'supporting_grant_ids' : 
                [('UIDs of supporting grants', 'convert_list')],
            # TODO Supporting Grants (proj number?)
            'times_cited' : 
                [('Times cited' , '', )],
            'altmetric' : 
                [('Altmetric' , '', )],
            'linkout' : 
                [('Source Linkout' , '', )],
            # NOT USED
            'category_for' : 
                [('FOR (ANZSRC) Categories', 'convert_dict_name')],
            'category_rcdc' : 
                [('RCDC Categories', 'convert_dict_name')],
            'category_hrcs_hc' : 
                [('HRCS HC Categories', 'convert_dict_name')],
            'category_hrcs_rac' : 
                [('HRCS RAC Categories', 'convert_dict_name')],
            'category_icrp_ct' : 
                [('ICRP Cancer Types', 'convert_dict_name')],
            'category_icrp_cso' : 
                [('ICRP CSO Categories', 'convert_dict_name')],
        }

    def simplify_nested_objects(self, remove_old_columns=True):
        df = self.df_original.copy()
        for x in self.columns_original:
            if x in self.column_transformations:
                for new_col, action in self.column_transformations[x]:
                    if action:
                        function = getattr(self, action)
                        # new_col = action + "_new"
                        if self.verbose: print("Converting ", x, "to", new_col)
                        if x == "author_affiliationss":
                            df[new_col] = df[x].fillna("").apply(lambda x: function(x[0]))
                        else:
                            df[new_col] = df[x].fillna("").apply(lambda x: function(x))
                    else:
                        df[new_col] = df[x]

        if remove_old_columns:
            # drop transformed cols, except 'id'
            cols_to_drop = [*self.column_transformations.keys()]
            # cols_to_drop.remove('id') # DEPRECATED
            cols_to_drop = [x for x in cols_to_drop if x in self.columns_original]
            if self.verbose: print("Dropping columns:", cols_to_drop)
            df.drop(columns=cols_to_drop, inplace=True)
        return df


    # CONVERSION METHODS


    def convert_id_to_url(self, idd, ttype=None):
        """
        """
        if ttype:
            return dimensions_url(idd, ttype)
        else:
            return dimensions_url(idd)

    # PS decided to not deal with DEPRECATED FIELDS!
    # can be removed
    def _handleDeprecatedAuthors(self, authorslist):
        "Handle the old `author_affiliations` that has an external extra list"
        if authorslist and type(authorslist) == list:
            if type(authorslist[0]) == list:
                # print("nested!")
                return authorslist[0]
            else:
                return authorslist 
        else:
            return []

    def convert_authors_to_names(self, authorslist):
        """
        """
        authorslist = self._handleDeprecatedAuthors(authorslist)
        authors = []
        for x in authorslist:
            name = x.get('last_name', "") + ", "+ x.get('first_name', "") 
            authors.append(name)
        return "; ".join(authors)


    def convert_authors_corresponding(self, authorslist):
        authors = []
        for x in authorslist:
            if x.get("corresponding", ""):
                name = x.get('last_name', "") + ", "+ x.get('first_name', "")
                authors.append(name)
        return "; ".join(authors)        

    def convert_authors_affiliations(self, authorslist):
        """
        """
        authorslist = self._handleDeprecatedAuthors(authorslist)
        author_affiliations = []
        for x in authorslist:
            name = x.get('last_name', "") + ", "+ x.get('first_name', "")
            affiliations = "; ".join([a.get('name', "") for a in x['affiliations']])
            author_affiliations.append(f"{name} ({affiliations})")
        return "; ".join(author_affiliations)

    def convert_list(self, data):
        return "; ".join([x for x in data])

    def convert_dict_name(self, data):
        return "; ".join([y['name'] for y in data])

    def convert_dict_ids(self, data):
        return "; ".join([y['id'] for y in data])

    def convert_city_name(self, data):
        return "; ".join([y['city_name'] for y in data])

    def convert_state_name(self, data):
        return "; ".join([y['city_name'] for y in data])

    def convert_country_name(self, data):
        return "; ".join([y['country_name'] for y in data])


