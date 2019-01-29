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
            # @TODO
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