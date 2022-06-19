#!/usr/bin/python
# -*- coding: utf-8 -*-


#
#
# SYNTAX_DICT is a dictionary representation of operators and other constants of the DSL language 
#
#

SYNTAX_DICT = {
    'allowed_starts_special_commands': {
        'help' : [],
        '.docs' : [],
        'quit' : [],
        '.show' : [],
        '.json_compact' : [],
        '.json_full' : [],
        '.export_as_html' : [],
        '.export_as_csv' : [],
        '.export_as_gist' : [],
        '.export_as_json' : [],
        '.export_as_bar_chart' : [],
        '.export_as_jupyter' : [],
        '.export_as_gsheets' : [],
        '.url' : [],
    },
    'allowed_starts_dsl_query': {
        'search': [],
        'describe': [ 'version', 'source', 'entity', 'schema'],
        'check_researcher_ids': [],
        'classify': [],
        'extract_grants': [],
        'extract_concepts': [],
        'extract_affiliations': [],
        'identify': [],
    },
    'dimensions_urls' : {
        'publications' : 'https://app.dimensions.ai/details/publication/',
        'grants' : 'https://app.dimensions.ai/details/grant/',
        'patents' : 'https://app.dimensions.ai/details/patent/',
        'policy_documents' : 'https://app.dimensions.ai/details/policy_documents/',
        'clinical_trials' : 'https://app.dimensions.ai/details/clinical_trial/',
        'datasets' : 'https://app.dimensions.ai/details/data_set/',
        'researchers' : 'https://app.dimensions.ai/discover/publication?and_facet_researcher=',
        'organizations' : 'https://app.dimensions.ai/discover/publication?and_facet_research_org=',
        'reports' : '',
        'source_titles' : 'https://app.dimensions.ai/discover/publication?and_facet_source_title=',
    },
    'dimensions_object_id_patterns' : {
        'publications' : 'pub.',
        'grants' : 'grant.',
        # 'patents' : ' ', # not yet supported
        'policy_documents' : 'policy.',
        # 'clinical_trials' : ' ',
        # 'datasets' : ' ',
        'researchers' : 'ur.',
        'organizations' : 'grid.',
        # 'reports' : ' ',
        'source_titles' : 'jour.',
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
        'unnest',
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
    'lang_after_return' : ['sort by', 'aggregate', 'limit'],
    'lang_after_return_functions' : ['citations_per_year', 'funding_per_year'],  # unused in rules yet
    'lang_after_sort_by' : ['asc', 'desc', 'limit', ],
    'lang_after_limit' : ['skip' ],
    'lang_filter_operators' : ['=', '!=', '>', '<', '>=', '<=', '~', 'is empty', 'is not empty'],
    'lang_text_operators' : ['AND', 'OR', 'NOT', '&&', '!', '||', '+', '-', '?', '*', '~'],
}

