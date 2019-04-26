#!/usr/bin/python
# -*- coding: utf-8 -*-



#
#
# SYNTAX_DICT is a dictionary representation of operators and other constants of the DSL language 
#
#

SYNTAX_DICT = {
    'allowed_starts': {
        'help' : [],
        'quit' : [],
        'show' : [ 'json_compact'],
        'export_html' : [],
        'export_csv' : [],
        'search': [],
        'describe': [ 'version', 'source', 'entity', 'schema'],
        'check_researcher_ids': [],
        'classify': [],
        'extract_grants': [],
        'extract_terms': [],
    },
    'allowed_starts_dsl_query': ['search' ,'describe', 'check_researcher_ids', 'classify', 'extract_grants', 'extract_terms'],
    'dimensions_urls' : {
        'publications' : 'https://app.dimensions.ai/details/publication/',
        'grants' : 'https://app.dimensions.ai/details/grant/',
        'patents' : 'https://app.dimensions.ai/details/patent/',
        'policy_documents' : 'https://app.dimensions.ai/details/clinical_trial/',
        'clinical_trials' : 'https://app.dimensions.ai/details/policy_documents/',
        'researchers' : 'https://app.dimensions.ai/discover/publication?and_facet_researcher=',
    },
    'lang_all': [
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
    'lang_after_search' : ['in', 'where', 'for', 'return'],
    'lang_after_filter' : ['and', 'or', 'not', 'return', ],
    'lang_after_for_text' : ['and', 'or', 'not', 'return', 'where' ],
    'lang_after_return' : ['sort by', 'asc', 'desc', 'aggregate', 'limit', 'skip' ],
    'lang_filter_operators' : ['=', '!=', '>', '<', '>=', '<=', '~', 'is empty', 'is not empty'],
    'lang_text_operators' : ['AND', 'OR', 'NOT', '&&', '!', '||', '+', '-', '?', '*', '~'],
}


#
# GRAMMAR_DICT is a dictionary rendering of the DSL grammar JSON
# which can be obtained with the query `describe schema`
#
# last updated: v1.16
# how to create:
#
# In [1]: import json
# In [2]: json.load(open("dsl_describe.bk.json"))
#
# then save the results in this file
#
#

GRAMMAR_DICT = {
    'sources': {
        'publications': {
            'fields': {
                'research_org_country_names': {
                    'type': 'string',
                    'description': 'GeoNames country name',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'RCDC': {
                    'type':
                    'categories',
                    'description':
                    'Research, Condition, and Disease Categorization',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'entity_type':
                    'categories',
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'times_cited': {
                    'type':
                    'count',
                    'description':
                    'Number of citations. Does not support emptiness filters',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'research_org_countries': {
                    'type': 'countries',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'countries',
                    'is_filter': True,
                    'is_facet': True
                },
                'linkout': {
                    'type': 'text',
                    'description': 'URL address',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'research_org_cities': {
                    'type': 'cities',
                    'description': 'GeoNames id and name',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'cities',
                    'is_filter': True,
                    'is_facet': True
                },
                'mesh_terms': {
                    'type':
                    'label',
                    'description':
                    'Medical Subject Heading terms as used in PubMed.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'open_access': {
                    'type':
                    'string',
                    'description':
                    'Open Access status for publication. Deprecated in favor of `open_access_categories`',
                    'long_description':
                    "\n\n        **DEPRECATED in favor of `open_access_categories`**\n\n        Open Access field data for publications can make reference to information on the host location and the record version.\n\n        **Open Access host location**\n\n        Host location information can describes if the document is either hosted by the publisher or in an institutional repository.\n\n           * **Open access - publisher** means the linked full-text version is served by the article's publisher.\n           * **Open access - repository** means the linked full-text version is served by an Open Access repository.\n\n        **Record Version**\n\n        Record version refers to the version of the content as defined by Unpaywall (see `Unpaywall Data Format <https://unpaywall.org/data-format>`_)\n\n           * **Open access - submitted** means the linked full-text version is not yet peer-reviewed.\n           * **Open access - accepted** means the linked full-text version is peer-reviewed, but lacks publisher-specific formatting.\n           * **Open access - published** means the linked full-text version is the version of record.\n        ",
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'doi': {
                    'type': 'identifier',
                    'description': 'Digital object identifier',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'recent_citations': {
                    'type':
                    'integer',
                    'description':
                    'Number of citations received in the last two years. Does not support emptiness filters',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'pmid': {
                    'type': 'identifier',
                    'description': 'PubMed ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'researchers': {
                    'type': 'researchers',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'researchers',
                    'is_filter': True,
                    'is_facet': True
                },
                'proceedings_title': {
                    'type':
                    'text',
                    'description':
                    'Title of a conference corresponding to documents that are `type` of "proceeding"',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    False,
                    'is_facet':
                    False
                },
                'referenced_pubs': {
                    'type':
                    'publications_entity',
                    'description':
                    'Dimensions publication id for documents referencing another document',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'entity_type':
                    'publications',
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'book_series_title': {
                    'type': 'text',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'relative_citation_ratio': {
                    'type':
                    'float',
                    'description':
                    'Relative citation performance of an article when compared to others in its area of research. Does not support emptiness filters',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'open_access_categories': {
                    'type':
                    'open_access',
                    'description':
                    'Open Access category for publication. Filtering on values is case sensitive.',
                    'long_description':
                    '\n        Open Access category data for publications values:\n\n        * `oa_all`: Article is freely available\n        * `gold_pure`: Version Of Record (VOR) is free under an open licence from a full OA journal\n        * `gold_hybrid`: Version Of Record (VOR) is free under an open licence in a paid-access journal\n        * `gold_bronze`: Freely available on publisher page, but without an open licence\n        * `green_pub`: Free copy of published version in an OA repository\n        * `green_acc`: Free copy of accepted version in an OA repository\n        * `green_sub`: Free copy of submitted version, or where version is unknown, in an OA repository\n        * `closed`: No freely available copy has been identified\n        ',
                    'is_entity':
                    True,
                    'entity_type':
                    'open_access',
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'supporting_grant_ids': {
                    'type': 'identifier',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'title': {
                    'type': 'text',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'FOR_first': {
                    'type': 'categories',
                    'description': 'Division level FOR',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'date_inserted': {
                    'type':
                    'timestamp',
                    'description':
                    'Date when publication was inserted into Dimensions',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'date': {
                    'type': 'date',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'volume': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'id': {
                    'type': 'identifier',
                    'description': 'Dimensions publication id',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'HRCS_HC': {
                    'type': 'categories',
                    'description': 'HRCS - Health Categories',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'terms': {
                    'type':
                    'text',
                    'description':
                    'Extracted terms. See :ref:`for-terms` regarding searching terms vs phrases',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    False,
                    'is_facet':
                    False
                },
                'type': {
                    'type':
                    'string',
                    'description':
                    'Publication type (article, chapter, proceeding, monograph, preprint or book)',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'issn': {
                    'type': 'string',
                    'description': 'International Standard Serial Number',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'publisher': {
                    'type': 'label',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'author_affiliations': {
                    'type':
                    'json',
                    'description':
                    "List of JSON lists of researchers' first and last names and affiliations",
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'issue': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'references': {
                    'type':
                    'identifier',
                    'description':
                    'Dimensions publication id for documents referencing another document',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'book_doi': {
                    'type': 'identifier',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'HRCS_RAC': {
                    'type': 'categories',
                    'description': 'HRCS – Research Activity Codes',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'FOR': {
                    'type': 'categories',
                    'description': 'ANZSRC Fields of Research classification',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'pmcid': {
                    'type': 'identifier',
                    'description': 'PubMed Central ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'journal': {
                    'type': 'journals',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'journals',
                    'is_filter': True,
                    'is_facet': True
                },
                'research_org_state_codes': {
                    'type': 'states',
                    'description': 'ISO\u200c-3166-2 code and name',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'states',
                    'is_filter': True,
                    'is_facet': True
                },
                'funder_countries': {
                    'type': 'countries',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'countries',
                    'is_filter': True,
                    'is_facet': True
                },
                'altmetric': {
                    'type':
                    'float',
                    'description':
                    'Altmetric attention score. Does not support emptiness filters',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'research_orgs': {
                    'type': 'orgs',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'orgs',
                    'is_filter': True,
                    'is_facet': True
                },
                'pages': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'field_citation_ratio': {
                    'type':
                    'float',
                    'description':
                    'Relative citation performance of article when compared to similarly aged articles in its area of research. Does not support emptiness filters',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'journal_lists': {
                    'type':
                    'string',
                    'description':
                    'Independent grouping of journals outside of Dimensions',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'research_org_state_names': {
                    'type': 'string',
                    'description': 'GeoNames state name',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'book_title': {
                    'type': 'text',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'funders': {
                    'type': 'orgs',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'orgs',
                    'is_filter': True,
                    'is_facet': True
                }
            },
            'fieldsets': ['all', 'basics', 'extras', 'book'],
            'metrics': {
                'count': {
                    'name': 'count',
                    'description': 'Total count'
                },
                'altmetric_median': {
                    'name': 'altmetric_median',
                    'description': 'Median Altmetric attention score'
                },
                'citations_total': {
                    'name': 'citations_total',
                    'description': 'Aggregated number of citations'
                },
                'citations_avg': {
                    'name': 'citations_avg',
                    'description': 'Arithmetic mean of citations'
                },
                'citations_median': {
                    'name': 'citations_median',
                    'description': 'Median of citations'
                },
                'recent_citations_total': {
                    'name':
                    'recent_citations_total',
                    'description':
                    'For a given article, in a given year, the number of citations accrued in the last two year period. Single value stored per document, year window rolls over in July.'
                },
                'rcr_avg': {
                    'name': 'rcr_avg',
                    'description':
                    'Arithmetic mean of `relative_citation_ratio`'
                },
                'fcr_gavg': {
                    'name': 'fcr_gavg',
                    'description': 'Geometric mean of `field_citation_ratio`'
                }
            },
            'search_fields': [
                'terms', 'title_only', 'terms_experimental', 'authors',
                'title_abstract_only', 'full_data', 'noun_phrases',
                'researchers'
            ]
        },
        'grants': {
            'fields': {
                'RCDC': {
                    'type':
                    'categories',
                    'description':
                    'Research, Condition, and Disease Categorization',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'entity_type':
                    'categories',
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'original_title': {
                    'type': 'text',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'active_year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'linkout': {
                    'type': 'text',
                    'description': 'URL linked to grant',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'research_org_countries': {
                    'type': 'countries',
                    'description': 'GeoNames code and name',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'countries',
                    'is_filter': True,
                    'is_facet': True
                },
                'research_org_name': {
                    'type': 'label',
                    'description': 'Name for research organisation',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'research_org_cities': {
                    'type': 'cities',
                    'description': 'GeoNames id and name',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'cities',
                    'is_filter': True,
                    'is_facet': True
                },
                'funding_chf': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in CHF',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'title_language': {
                    'type': 'label',
                    'description': 'ISO 639-1 language code used in title',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'researchers': {
                    'type': 'researchers',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'researchers',
                    'is_filter': True,
                    'is_facet': True
                },
                'end_date': {
                    'type': 'timestamp',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funding_gbp': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in GBP',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funding_org_city': {
                    'type': 'label',
                    'description': 'City name for funding organisation',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'funding_usd': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in USD',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'title': {
                    'type': 'text',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'start_year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'FOR_first': {
                    'type': 'categories',
                    'description': 'Division level FOR',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'date_inserted': {
                    'type':
                    'timestamp',
                    'description':
                    'Date when publication was inserted into Dimensions',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'funding_aud': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in AUD',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'id': {
                    'type': 'identifier',
                    'description': 'Dimensions grant id',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'HRCS_HC': {
                    'type': 'categories',
                    'description': 'HRCS - Health Categories',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'terms': {
                    'type': 'text',
                    'description': 'Extracted terms',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'abstract': {
                    'type': 'text',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'project_num': {
                    'type': 'identifier',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funding_jpy': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in JPY',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funding_cad': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in CAD',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'HRCS_RAC': {
                    'type': 'categories',
                    'description': 'HRCS – Research Activity Codes',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'researcher_details': {
                    'type':
                    'json',
                    'description':
                    'Additional details about researchers including affiliations and role',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'FOR': {
                    'type': 'categories',
                    'description': 'ANZSRC Fields of Research classification',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'funding_eur': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in EUR',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'research_org_state_codes': {
                    'type': 'states',
                    'description': 'ISO\u200c-3166-2 code and name',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'states',
                    'is_filter': True,
                    'is_facet': True
                },
                'funder_countries': {
                    'type': 'countries',
                    'description': 'GeoNames code and name',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'countries',
                    'is_filter': True,
                    'is_facet': True
                },
                'funding_org_name': {
                    'type': 'label',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'research_orgs': {
                    'type': 'orgs',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'orgs',
                    'is_filter': True,
                    'is_facet': True
                },
                'start_date': {
                    'type': 'timestamp',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'language': {
                    'type': 'label',
                    'description': 'ISO 639-1 language codes',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'funding_org_acronym': {
                    'type': 'label',
                    'description': 'Acronym for funding organisation',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'resulting_publication_ids': {
                    'type':
                    'identifier',
                    'description':
                    'Resulting Publication IDs. Deprecated, use `publications` field `supporting_grant_ids` instead',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'funders': {
                    'type': 'orgs',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'orgs',
                    'is_filter': True,
                    'is_facet': True
                }
            },
            'fieldsets': ['all', 'basics', 'extras'],
            'metrics': {
                'count': {
                    'name': 'count',
                    'description': 'Total count'
                },
                'funding': {
                    'name': 'funding',
                    'description': None
                }
            },
            'search_fields': [
                'terms', 'title_only', 'title_abstract_only', 'full_data',
                'noun_phrases', 'researchers'
            ]
        },
        'patents': {
            'fields': {
                'RCDC': {
                    'type':
                    'categories',
                    'description':
                    'Research, Condition, and Disease Categorization',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'entity_type':
                    'categories',
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'times_cited': {
                    'type': 'count',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'filing_status': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'assignee_cities': {
                    'type': 'cities',
                    'description': 'GeoNames id and name',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'cities',
                    'is_filter': True,
                    'is_facet': True
                },
                'additional_filters': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'expiration_date': {
                    'type': 'timestamp',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'reference_ids': {
                    'type': 'identifier',
                    'description': 'Patents which are cited by this patent',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'assignee_names': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'granted_year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'cited_by_ids': {
                    'type': 'identifier',
                    'description': 'Patents which cite this patent',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'assignees': {
                    'type': 'orgs',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'orgs',
                    'is_filter': True,
                    'is_facet': True
                },
                'jurisdiction': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'publication_ids': {
                    'type': 'identifier',
                    'description': 'Related publication IDs',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'associated_grant_ids': {
                    'type': 'identifier',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'original_assignees': {
                    'type': 'orgs',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'orgs',
                    'is_filter': True,
                    'is_facet': True
                },
                'title': {
                    'type': 'text',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'FOR_first': {
                    'type': 'categories',
                    'description': 'Division level FOR',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'date_inserted': {
                    'type':
                    'timestamp',
                    'description':
                    'Date when publication was inserted into Dimensions',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'status': {
                    'type': 'string',
                    'description': 'Deprecated in favor of `legal_status`',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'date': {
                    'type': 'timestamp',
                    'description': 'Date when the patent was filed',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'publication_date': {
                    'type': 'timestamp',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'cpc': {
                    'type':
                    'identifier',
                    'description':
                    'Cooperative Patent Classification number for a patent',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'HRCS_HC': {
                    'type': 'categories',
                    'description': 'HRCS - Health Categories',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'id': {
                    'type': 'identifier',
                    'description': 'Dimensions patent id',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'inventor_names': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'abstract': {
                    'type': 'text',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'assignee_countries': {
                    'type': 'countries',
                    'description': 'GeoNames code and name',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'countries',
                    'is_filter': True,
                    'is_facet': True
                },
                'assignee_state_codes': {
                    'type': 'states',
                    'description': 'GeoNames code and name',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'states',
                    'is_filter': True,
                    'is_facet': True
                },
                'current_assignees': {
                    'type': 'orgs',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'orgs',
                    'is_filter': True,
                    'is_facet': True
                },
                'current_assignee_names': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'original_assignee_names': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'HRCS_RAC': {
                    'type': 'categories',
                    'description': 'HRCS – Research Activity Codes',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'FOR': {
                    'type': 'categories',
                    'description': 'ANZSRC Fields of Research classification',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'filed_year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'ipcr': {
                    'type':
                    'identifier',
                    'description':
                    'International Patent Classification Reform number for a patent',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'filed_date': {
                    'type': 'timestamp',
                    'description': 'Deprecated in favor of `filed_date`',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funder_groups': {
                    'type': 'org_groups',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'org_groups',
                    'is_filter': True,
                    'is_facet': True
                },
                'legal_status': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'priority_date': {
                    'type': 'timestamp',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'assignee_state_names': {
                    'type': 'label',
                    'description': 'GeoNames name',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'funders': {
                    'type': 'orgs',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'orgs',
                    'is_filter': True,
                    'is_facet': True
                }
            },
            'fieldsets': ['all', 'basics', 'extras'],
            'metrics': {
                'count': {
                    'name': 'count',
                    'description': 'Total count'
                }
            },
            'search_fields':
            ['full_data', 'title_only', 'title_abstract_only']
        },
        'clinical_trials': {
            'fields': {
                'RCDC': {
                    'type':
                    'categories',
                    'description':
                    'Research, Condition, and Disease Categorization',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'entity_type':
                    'categories',
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'linkout': {
                    'type': 'text',
                    'description': 'URL linked to clinical trial',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'conditions': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'organizations': {
                    'type':
                    'orgs',
                    'description':
                    'IDs of any organizations involved in any way, e.g. as sponsors or collaborators',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'entity_type':
                    'orgs',
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'publication_ids': {
                    'type': 'identifier',
                    'description': 'Linked Publication IDs',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'associated_grant_ids': {
                    'type': 'identifier',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'title': {
                    'type': 'text',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'FOR_first': {
                    'type': 'categories',
                    'description': 'Division level FOR',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'date_inserted': {
                    'type':
                    'timestamp',
                    'description':
                    'Date when publication was inserted into Dimensions',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'date': {
                    'type': 'timestamp',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'investigators': {
                    'type':
                    'json',
                    'description':
                    'JSON with names, titles, & roles (no ids) of involved researchers for display purposes',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'HRCS_HC': {
                    'type': 'categories',
                    'description': 'HRCS - Health Categories',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'id': {
                    'type': 'identifier',
                    'description': 'Dimensions clinical trial id',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'abstract': {
                    'type': 'text',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'registry': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'phase': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'HRCS_RAC': {
                    'type': 'categories',
                    'description': 'HRCS – Research Activity Codes',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'FOR': {
                    'type': 'categories',
                    'description': 'ANZSRC Fields of Research classification',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'funder_countries': {
                    'type': 'countries',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'countries',
                    'is_filter': True,
                    'is_facet': True
                },
                'gender': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funder_groups': {
                    'type': 'org_groups',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'org_groups',
                    'is_filter': True,
                    'is_facet': True
                },
                'active_years': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'funders': {
                    'type': 'orgs',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'orgs',
                    'is_filter': True,
                    'is_facet': True
                }
            },
            'fieldsets': ['all', 'basics', 'extras'],
            'metrics': {
                'count': {
                    'name': 'count',
                    'description': 'Total count'
                }
            },
            'search_fields':
            ['full_data', 'title_only', 'researchers', 'title_abstract_only']
        },
        'policy_documents': {
            'fields': {
                'HRCS_HC': {
                    'type': 'categories',
                    'description': 'HRCS - Health Categories',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'id': {
                    'type': 'identifier',
                    'description': 'Dimensions clinical trial id',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'health_research_areas': {
                    'type': 'categories',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'RCDC': {
                    'type':
                    'categories',
                    'description':
                    'Research, Condition, and Disease Categorization',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'entity_type':
                    'categories',
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'year': {
                    'type': 'integer',
                    'description': 'Policy posted on year',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'linkout': {
                    'type': 'text',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'country': {
                    'type': 'countries',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'countries',
                    'is_filter': True,
                    'is_facet': True
                },
                'publication_ids': {
                    'type': 'identifier',
                    'description': 'Referenced Publication IDs',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'state': {
                    'type': 'states',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'states',
                    'is_filter': True,
                    'is_facet': True
                },
                'broad_research_areas': {
                    'type': 'categories',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'source_name': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'grid_id': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'title': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'FOR_first': {
                    'type': 'categories',
                    'description': 'Division level FOR',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'city': {
                    'type': 'cities',
                    'description': None,
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'cities',
                    'is_filter': True,
                    'is_facet': True
                },
                'HRCS_RAC': {
                    'type': 'categories',
                    'description': 'HRCS – Research Activity Codes',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                },
                'FOR': {
                    'type': 'categories',
                    'description': 'ANZSRC Fields of Research classification',
                    'long_description': None,
                    'is_entity': True,
                    'entity_type': 'categories',
                    'is_filter': True,
                    'is_facet': True
                }
            },
            'fieldsets': ['all', 'basics', 'categories'],
            'metrics': {
                'count': {
                    'name': 'count',
                    'description': 'Total count'
                }
            },
            'search_fields': ['full_data', 'title_only']
        },
        'researchers': {
            'fields': {
                'id': {
                    'type': 'identifier',
                    'description': 'Dimensions researcher id',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'last_grant_year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'current_research_org': {
                    'type':
                    'orgs',
                    'description':
                    'The most recent research organization linked to the researcher',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'entity_type':
                    'orgs',
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'research_orgs': {
                    'type':
                    'orgs',
                    'description':
                    'All research organizations linked to the researcher',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'entity_type':
                    'orgs',
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'obsolete': {
                    'type':
                    'integer',
                    'description':
                    '\n        Indicates researcher ID status. 0 means that the researcher ID is still active, 1 means that the researcher ID is no longer valid. See redirect field for further information on invalid researcher IDs.\n        ',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'redirect': {
                    'type':
                    'identifier',
                    'description':
                    '\n        Indicates status of obsolete researcher ID. Empty means that the researcher ID was deleted. Otherwise ID provided means that is the new id into which the obsolete one was redirected. If multiple values are available, it means that the original researcher ID was split into multiple IDs.\n        ',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'first_grant_year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'total_publications': {
                    'type': 'integer',
                    'description': 'Total publications count',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'last_name': {
                    'type': 'string',
                    'description': 'Last Name',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'last_publication_year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'total_grants': {
                    'type': 'integer',
                    'description': 'Total grants count',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'first_name': {
                    'type': 'string',
                    'description': 'First Name',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'orcid_id': {
                    'type': 'text',
                    'description': '`ORCID <https://orcid.org/>`_ ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'first_publication_year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                }
            },
            'fieldsets': ['all', 'basics', 'extras'],
            'metrics': {
                'count': {
                    'name': 'count',
                    'description': 'Total count'
                }
            },
            'search_fields': ['researcher']
        }
    },
    'entities': {
        'categories': {
            'fields': {
                'id': {
                    'name': 'id',
                    'type': 'string',
                    'description': 'Dimensions category id',
                    'long_description': None,
                    'is_filter': True
                },
                'name': {
                    'name': 'name',
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_filter': True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'cities': {
            'fields': {
                'id': {
                    'name': 'id',
                    'type': 'identifier',
                    'description': 'Dimensions city id',
                    'long_description': None,
                    'is_filter': True
                },
                'name': {
                    'name': 'name',
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_filter': True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'countries': {
            'fields': {
                'id': {
                    'name': 'id',
                    'type': 'string',
                    'description': 'Dimensions city id',
                    'long_description': None,
                    'is_filter': True
                },
                'name': {
                    'name': 'name',
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_filter': True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'journals': {
            'fields': {
                'id': {
                    'name': 'id',
                    'type': 'string',
                    'description': 'Dimensions journal id',
                    'long_description': None,
                    'is_filter': True
                },
                'title': {
                    'name': 'title',
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_filter': True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'org_groups': {
            'fields': {
                'id': {
                    'name': 'id',
                    'type': 'identifier',
                    'description': 'Dimensions organization group id',
                    'long_description': None,
                    'is_filter': True
                },
                'name': {
                    'name': 'name',
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_filter': True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'orgs': {
            'fields': {
                'id': {
                    'name': 'id',
                    'type': 'identifier',
                    'description': 'Dimensions organization id',
                    'long_description': None,
                    'is_filter': True
                },
                'name': {
                    'name': 'name',
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_filter': True
                },
                'acronym': {
                    'name': 'acronym',
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_filter': True
                },
                'country_name': {
                    'name': 'country_name',
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_filter': True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'states': {
            'fields': {
                'id': {
                    'name': 'id',
                    'type': 'identifier',
                    'description': 'Dimensions state id',
                    'long_description': None,
                    'is_filter': True
                },
                'name': {
                    'name': 'name',
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_filter': True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'publications_entity': {
            'fields': {
                'id': {
                    'name': 'id',
                    'type': 'identifier',
                    'description': 'Dimensions publication id',
                    'long_description': None,
                    'is_filter': True
                },
                'doi': {
                    'name': 'doi',
                    'type': 'identifier',
                    'description': 'Digital object identifier',
                    'long_description': None,
                    'is_filter': True
                },
                'pmid': {
                    'name': 'pmid',
                    'type': 'identifier',
                    'description': 'PubMed ID',
                    'long_description': None,
                    'is_filter': True
                },
                'pmcid': {
                    'name': 'pmcid',
                    'type': 'identifier',
                    'description': 'PubMed Central ID',
                    'long_description': None,
                    'is_filter': True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'open_access': {
            'fields': {
                'id': {
                    'name': 'id',
                    'type': 'identifier',
                    'description': None,
                    'long_description': None,
                    'is_filter': True
                },
                'name': {
                    'name': 'name',
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_filter': True
                },
                'description': {
                    'name': 'description',
                    'type': 'text',
                    'description': None,
                    'long_description': None,
                    'is_filter': False
                }
            },
            'fieldsets': ['all', 'basics']
        }
    }
}
