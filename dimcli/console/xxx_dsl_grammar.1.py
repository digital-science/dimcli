#
# https://docs.dimensions.ai/dsl/data.html
#

# need a structure that contains desc / and possibly other lang metadata
# then maybe we can have 'children' as a key for nested objects


VOCABULARY = {
    'allowed_starts': {
        'help' : [],
        'quit' : [],
        'show' : [ 'json', 'json_pretty', 'json_html'],
        'search': [],
        'describe': [ 'version', 'source', 'entity', 'schema'],
    },
    'dimensions_urls' : {
        'publications' : 'https://app.dimensions.ai/details/publication/',
        'grants' : 'https://app.dimensions.ai/details/grant/',
        'patents' : 'https://app.dimensions.ai/details/patent/',
        'policy_documents' : 'https://app.dimensions.ai/details/clinical_trial/',
        'clinical_trials' : 'https://app.dimensions.ai/details/policy_documents/',
        'researchers' : 'https://app.dimensions.ai/discover/publication?and_facet_researcher=',
    },
    'lang': [
        'search',
        'return',
        'for',
        'where',
        'in',
        'limit',
        'skip',
        'aggregate',
        '=',  # filter operators https://docs.dimensions.ai/dsl/language.html#simple-filters
        '!=',
        '>',
        '<',
        '>=',
        '<=',
        '~',
        'is empty',
        'is not empty',
        "count", # https://docs.dimensions.ai/dsl/language.html#filter-functions
        'sort by',
        'asc',
        'desc',
        "AND", # boolean operators https://docs.dimensions.ai/dsl/language.html#id6
        "OR", 
        "NOT",
        "&&",
        "!",
        "||",
        "+",
        "-",
    ],
    'sources': {
        'publications': {
            'fields': [
                'altmetric',
                'author_affiliations',
                'book_doi',
                'book_series_title',
                'book_title',
                'date',
                'date_inserted',
                'doi',
                'field_citation_ratio',
                'id',
                'issn',
                'issue',
                'journal_lists',
                'linkout',
                'open_access',
                'pages',
                'pmcid',
                'pmid',
                'proceedings_title',
                'references',
                'relative_citation_ratio',
                'research_org_country_names',
                'supporting_grant_ids',
                'times_cited',
                'title',
                'type',
                'volume',
            ],
            'facets': [
                'mesh_terms', 'publisher', 'recent_citations',
                'research_org_state_names', 'year'
            ],
            'entities': [
                ('FOR', 'categories'),
                ('FOR_first', 'categories'),
                ('funder_countries', 'countries'),
                ('funders', 'orgs'),
                ('HRCS_HC', 'categories'),
                ('HRCS_RAC', 'categories'),
                ('journal', 'journals'),
                ('RCDC', 'categories'),
                ('research_org_cities', 'cities'),
                ('research_org_countries', 'countries'),
                ('research_org_state_codes', 'states'),
                ('research_orgs', 'orgs'),
                ('researchers', 'researchers'),
            ],
            'fieldsets': ['extras', 'book', 'basic'],
            'metrics': ['rcr_avg', 'count', 'altmetric_median'],
            'search_fields': [
                'title_only', 'title_abstract_only', 'researchers',
                'full_data', 'authors'
            ],
        },
        'grants': {
            'fields': [
                "abstract",
                "date_inserted",
                "end_date",
                "funding_aud",
                "funding_cad",
                "funding_chf",
                "funding_eur",
                "funding_gbp",
                "funding_jpy",
                "funding_usd",
                "id",
                "linkout",
                "original_title",
                "project_num",
                "resulting_publication_ids",
                "start_date",
                "title",
            ],
            'facets': [
                "active_year",
                "funding_org_acronym",
                "funding_org_city",
                "funding_org_name",
                "language",
                "research_org_name",
                "start_year",
                "title_language",
            ],
            'entities': [
                ("FOR", "categories"),
                ("FOR_first", "categories"),
                ("funder_countries", "countries"),
                ("funders", "orgs"),
                ("HRCS_HC", "categories"),
                ("HRCS_RAC", "categories"),
                ("RCDC", "categories"),
                ("research_org_cities", "cities"),
                ("research_org_countries", "countries"),
                ("research_org_state_codes", "states"),
                ("research_orgs", "orgs"),
                ("researchers", "researchers"),
            ],
            'fieldsets': ['extras', 'basics'],
            'metrics': ['funding', 'count'],
            'search_fields':
            ['title_only', 'title_abstract_only', 'full_data'],
        },
        'patents': {
            'fields': [
                "abstract",
                "additional_filters",
                "assignee_names",
                "associated_grant_ids",
                "cited_by_ids",
                "cpc",
                "current_assignee_names",
                "date",
                "date_inserted",
                "expiration_date",
                "filed_date",
                "filing_status",
                "id",
                "inventor_names",
                "ipcr",
                "jurisdiction",
                "legal_status",
                "original_assignee_names",
                "priority_date",
                "publication_date",
                "publication_ids",
                "reference_ids",
                "status",
                "times_cited",
                "title",
            ],
            'facets': [
                'assignee_state_names',
                'filed_year',
                'granted_year',
                'year',
            ],
            'entities': [
                ("assignee_cities", "cities"),
                ("assignee_countries", "countries"),
                ("assignee_state_codes", "states"),
                ("assignees", "orgs"),
                ("current_assignees", "orgs"),
                ("FOR", "categories"),
                ("FOR_first", "categories"),
                ("funder_groups", "org_groups"),
                ("funders", "orgs"),
                ("HRCS_HC", "categories"),
                ("HRCS_RAC", "categories"),
                ("original_assignees", "orgs"),
                ("RCDC", "categories"),
            ],
            'fieldsets': ['extras', 'basics'],
            'metrics': ['count'],
            'search_fields':
            ['title_only', 'title_abstract_only', 'full_data'],
        },
        'policy_documents': {
            'fields': [
                'grid_id', 'id', 'linkout', 'publication_ids', 'source_name',
                'title'
            ],
            'facets': ['year'],
            'entities': [
                ('broad_research_areas', 'categories'),
                ('city', 'cities'),
                ('country', 'countries'),
                ('FOR', 'categories'),
                ('FOR_first', 'categories'),
                ('health_research_areas', 'categories'),
                ('HRCS_HC', 'categories'),
                ('HRCS_RAC', 'categories'),
                ('RCDC', 'categories'),
            ],
            'fieldsets': ['categories', 'basics'],
            'metrics': ['count'],
            'search_fields': ['title_only', 'full_data'],
        },
        'clinical_trials': {
            'fields': [
                "abstract",
                "associated_grant_ids",
                "conditions",
                "date",
                "gender",
                "id",
                "investigators",
                "linkout",
                "phase",
                "publication_ids",
                "registry",
                "title",
            ],
            'facets': ['active_years'],
            'entities': [
                ("FOR", "categories"),
                ("FOR_first", "categories"),
                ("funder_countries", "countries"),
                ("funder_groups", "org_groups"),
                ("funders", "orgs"),
                ("HRCS_HC", "categories"),
                ("HRCS_RAC", "categories"),
                ("organizations", "orgs"),
                ("RCDC", "categories"),
            ],
            'fieldsets': ['extras', 'basics'],
            'metrics': ['count'],
            'search_fields':
            ['title_only', 'title_abstract_only', 'full_data'],
        },
    }
}


 



def search_vocab_get_key(val, dct=VOCABULARY, parent=None):
    """
    quick and dirty way to search for a match in the voc dict
    >> print(search_vocab_get_key("journal")) # =entities

    So that the autocomplete can determine the grammar-type of an object
    """
    for x in dct:
        if x == val and parent != "dimensions_urls":
            return parent
        # print(x, type(dct[x]))
        if type(dct[x]) == dict:
            # print("recur")
            res = search_vocab_get_key(val, dct[x], x)
            if res is not None:
                return res
        if type(dct[x]) == list:
            for y in dct[x]:
                if type(y) == tuple:
                    if y[0] == val:
                        return x      
                elif y == val:
                    return x   
                





# template

# VOCABULARY = {
#     'sources': {
#         'publications': {
#             'fields': [],
#             'facets': [],
#             'entities': [],
#             'fieldsets': [],
#             'metrics': [],
#             'search_fields': [],
#         },
#         'grants': {
#             'fields': [],
#             'facets': [],
#             'entities': [],
#             'fieldsets': [],
#             'metrics': [],
#             'search_fields': [],
#         },
#         'patents': {
#             'fields': [],
#             'facets': [],
#             'entities': [],
#             'fieldsets': [],
#             'metrics': [],
#             'search_fields': [],
#         },
#         'clinical_trials': {
#             'fields': [],
#             'facets': [],
#             'entities': [],
#             'fieldsets': [],
#             'metrics': [],
#             'search_fields': [],
#         },
#         'policy_documents': {
#             'fields': [],
#             'facets': [],
#             'entities': [],
#             'fieldsets': [],
#             'metrics': [],
#             'search_fields': [],
#         },
#     }
# }