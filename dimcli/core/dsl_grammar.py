#
# https://docs.dimensions.ai/dsl/data.html
#

VOCABULARY = {
    'allowed_starts': [
        'quit',  # meta
        'show',  # meta
        'search',
    ],
    'lang': [
        'search',
        'return',
        'for',
        'where',
        'in',
        'limit',
        '=',
        '!=',
        '>',
        '<',
        '>=',
        '<=',
        '~',
        'is empty',
        'is not empty',
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
            'fields': [],
            'facets': [],
            'entities': [],
            'fieldsets': [],
            'metrics': [],
            'search_fields': [],
        },
        'patents': {
            'fields': [],
            'facets': [],
            'entities': [],
            'fieldsets': [],
            'metrics': [],
            'search_fields': [],
        },
        'clinical_trials': {
            'fields': [],
            'facets': [],
            'entities': [],
            'fieldsets': [],
            'metrics': [],
            'search_fields': [],
        },
        'policy_documents': {
            'fields': [],
            'facets': [],
            'entities': [],
            'fieldsets': [],
            'metrics': [],
            'search_fields': [],
        },
    }
}

Allowed_Starts = [
    # here go the main gramma words without the dot notation
    'quit',  # meta
    'show',  # meta
    'search',
]

dim_lang_1 = [
    # https://docs.dimensions.ai/dsl/language.html
    'search',
    'return',
]

dim_lang_2 = [
    # https://docs.dimensions.ai/dsl/language.html
    'for',
    'where',
    'in',
    'limit',
]

dim_lang_3 = [
    # https://docs.dimensions.ai/dsl/language.html#simple-filters
    '=',
    '!=',
    '>',
    '<',
    '>=',
    '<=',
    '~',
    'is empty',
    'is not empty',
]
dim_lang = dim_lang_1 + dim_lang_2 + dim_lang_3

Sources_All = [
    # https://docs.dimensions.ai/dsl/data.html#sources
    'publications',
    'grants',
    'patents',
    'clinical_trials',
    'policy_documents',
]

dim_all_completions = dim_lang

dim_entities_after_dot = [
    'research_orgs.name',  # trying to add DOT notation
    # @TODO programmatically add all variations based on docs
]

# PUBLICATIONS FIELDS

Publication_Literal_Fields = [
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
]

Publications_Facet_Fields = [
    'mesh_terms',
    'publisher',
    'recent_citations',
    'research_org_state_names',
    'year',
]

Publications_Entity_Fields = [
    'FOR',
    'FOR_first',
    'funder_countries',
    'funders',
    'HRCS_HC',
    'HRCS_RAC',
    'journal',
    'RCDC',
    'research_org_cities',
    'research_org_countries',
    'research_org_state_code',
    'research_orgs',
    'researchers',
]
Publications_Fieldsets = ['extras', 'book', 'basics']
Publications_Metrics = ['rcr_avg', 'count', 'altmetric_median']
Publications_Search_Fields = [
    'title_only',
    'title_abstract_only',
    'researchers',
    'full_data',
    'researchers',
]

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