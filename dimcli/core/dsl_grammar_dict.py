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
        '.show_json_compact' : [],
        '.show_json_full' : [],
        '.export_as_html' : [],
        '.export_as_csv' : [],
        '.export_as_json' : [],
    },
    'allowed_starts_dsl_query': {
        'search': [],
        'describe': [ 'version', 'source', 'entity', 'schema'],
        'check_researcher_ids': [],
        'classify': [],
        'extract_grants': [],
        'extract_terms': [],
    },
    'dimensions_urls' : {
        'publications' : 'https://app.dimensions.ai/details/publication/',
        'grants' : 'https://app.dimensions.ai/details/grant/',
        'patents' : 'https://app.dimensions.ai/details/patent/',
        'policy_documents' : 'https://app.dimensions.ai/details/policy_documents/',
        'clinical_trials' : 'https://app.dimensions.ai/details/clinical_trial/',
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
    'lang_after_return' : ['sort by', 'aggregate', 'limit',],
    'lang_after_sort_by' : ['asc', 'desc', 'limit', ],
    'lang_after_limit' : ['skip' ],
    'lang_filter_operators' : ['=', '!=', '>', '<', '>=', '<=', '~', 'is empty', 'is not empty'],
    'lang_text_operators' : ['AND', 'OR', 'NOT', '&&', '!', '||', '+', '-', '?', '*', '~'],
}


#
# GRAMMAR_DICT is a dictionary rendering of the DSL grammar JSON
# which can be obtained with the query `describe schema`
#
# last updated: v1.16 2019-04-26
# how to create:
#
# In [1]: import dimcli
# In [2]: dsl = dimcli.Dsl()
# In [3]: dsl.query("describe schema").json
#
# then save the results in GRAMMAR_DICT symbol
#
#

GRAMMAR_DICT = {
    'sources': {
        'publications': {
            'fields': {
                'relative_citation_ratio': {
                    'type':
                    'float',
                    'description':
                    'Relative citation performance of an article when compared to others in its area of research (note: does not support emptiness filters).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
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
                'open_access_categories': {
                    'type':
                    'open_access',
                    'description':
                    'Open Access categories for publications. See below for more examples.',
                    'long_description':
                    'Open Access category data for publications values:\n\n        * `oa_all`: Article is freely available\n        * `gold_pure`: Version Of Record (VOR) is free under an open licence from a full OA journal\n        * `gold_hybrid`: Version Of Record (VOR) is free under an open licence in a paid-access journal\n        * `gold_bronze`: Freely available on publisher page, but without an open licence\n        * `green_pub`: Free copy of published version in an OA repository\n        * `green_acc`: Free copy of accepted version in an OA repository\n        * `green_sub`: Free copy of submitted version, or where version is unknown, in an OA repository\n        * `closed`: No freely available copy has been identified',
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'funder_countries': {
                    'type':
                    'countries',
                    'description':
                    'The country of the GRID organisation funding this publication.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'field_citation_ratio': {
                    'type':
                    'float',
                    'description':
                    'Relative citation performance of article when compared to similarly aged articles in its area of research (note: does not support emptiness filters).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'author_affiliations': {
                    'type':
                    'json',
                    'description':
                    'Ordered list of authors names and their affiliations, as they appear in the original publication. The list can include researcher and organization identifiers, when available (note: in order to search for disambiguated authors, use the `in researchers` syntax).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'research_org_country_names': {
                    'type':
                    'string',
                    'description':
                    'Country name of the GRID organisations authors are affiliated to, as a string.',
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
                    'type':
                    'countries',
                    'description':
                    'Country of the GRID organisations authors are affiliated to, identified using GeoNames codes (note: this field supports :ref:`filter-functions`: ``count``).',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'research_orgs': {
                    'type':
                    'orgs',
                    'description':
                    'GRID organisations associated to a publication. Identifiers are automatically extracted from author affiliations text, so they can be missing in some cases (note: this field supports :ref:`filter-functions`: ``count``).',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'title': {
                    'type': 'text',
                    'description': 'Title of a publication.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'date_inserted': {
                    'type':
                    'timestamp',
                    'description':
                    "Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=').",
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'pages': {
                    'type':
                    'string',
                    'description':
                    'The pages of the publication, as they would appear in a citation record.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'publisher': {
                    'type': 'label',
                    'description': 'Name of the publisher as a string.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'pmid': {
                    'type': 'identifier',
                    'description': 'PubMed ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'year': {
                    'type':
                    'integer',
                    'description':
                    'The year of publication (note: when the `date` field is available, this is equal to the year part of the full date).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'HRCS_RAC': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'reference_ids': {
                    'type':
                    'identifier',
                    'description':
                    'Dimensions publication ID for publications in the references list, i.e. outgoing citations (see also: :ref:`data-model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'altmetric': {
                    'type': 'float',
                    'description': 'Altmetric attention score.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funders': {
                    'type':
                    'orgs',
                    'description':
                    'The GRID organisation funding this publication.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'type': {
                    'type':
                    'label',
                    'description':
                    'Publication type (one of: article, chapter, proceeding, monograph, preprint or book).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'doi': {
                    'type': 'identifier',
                    'description': 'Digital object identifier.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'book_title': {
                    'type':
                    'text',
                    'description':
                    'The title of the book a chapter belongs to (note: this field is available only for chapters).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    False,
                    'is_facet':
                    False
                },
                'volume': {
                    'type': 'string',
                    'description': 'Publication volume.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'journal_lists': {
                    'type':
                    'string',
                    'description':
                    "Independent grouping of journals outside of Dimensions, e.g. 'ERA 2015' or 'Norwegian register level 1'.",
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'concepts': {
                    'type':
                    'text',
                    'description':
                    'Concepts describing the main topics of a publication (note: automatically derived from the publication text using machine learning).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    False,
                    'is_facet':
                    False
                },
                'HRCS_HC': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'supporting_grant_ids': {
                    'type':
                    'identifier',
                    'description':
                    'Grants supporting a publication, returned as a list of dimensions grants IDs  (see also: :ref:`data-model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
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
                    False
                },
                'book_doi': {
                    'type':
                    'identifier',
                    'description':
                    'The DOI of the book a chapter belongs to (note: this field is available only for chapters).',
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
                    'type':
                    'string',
                    'description':
                    'State name of the GRID organisations authors are affiliated to, as a string.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'researchers': {
                    'type':
                    'researchers',
                    'description':
                    "Researcher IDs matched to the publication's authors list. (note: this returns only the disambiguated authors of a publication; in order to get the full authors list, the field `author_affiliations` should be used). This field supports :ref:`filter-functions`: ``count``.",
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'issn': {
                    'type': 'string',
                    'description': 'International Standard Serial Number',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'issue': {
                    'type': 'string',
                    'description': 'The issue number of a publication.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'research_org_cities': {
                    'type':
                    'cities',
                    'description':
                    'City of the GRID organisations authors are affiliated to, expressed as GeoNames ID and name.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'research_org_state_codes': {
                    'type':
                    'states',
                    'description':
                    'State of the GRID organisations authors are affiliated to, expressed as GeoNames codes (ISO\u200c-3166-2).',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'id': {
                    'type': 'identifier',
                    'description': 'Dimensions publication ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'linkout': {
                    'type': 'text',
                    'description': 'Original URL for a publication full text.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'times_cited': {
                    'type':
                    'count',
                    'description':
                    'Number of citations (note: does not support emptiness filters).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'journal': {
                    'type': 'journals',
                    'description': 'The journal a publication belongs to.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True
                },
                'FOR_first': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , first level or 2 digit codes.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'RCDC': {
                    'type':
                    'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'pmcid': {
                    'type': 'identifier',
                    'description': 'PubMed Central ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'FOR': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , second level or 4 digit codes.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'date': {
                    'type':
                    'date',
                    'description':
                    'The publication date of a document, eg "2018-01-01" (note: dates can sometimes be incomplete and include only the month or the year).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'book_series_title': {
                    'type':
                    'text',
                    'description':
                    'The title of the book series book, belong to.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    False,
                    'is_facet':
                    False
                },
                'proceedings_title': {
                    'type':
                    'text',
                    'description':
                    'Title of the conference proceedings volume associated to a publication.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    False,
                    'is_facet':
                    False
                },
                'altmetric_id': {
                    'type': 'integer',
                    'description': 'AltMetric Publication ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
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
                    'name':
                    'rcr_avg',
                    'description':
                    'Arithmetic mean of `relative_citation_ratio` field.'
                },
                'fcr_gavg': {
                    'name':
                    'fcr_gavg',
                    'description':
                    'Geometric mean of `field_citation_ratio` field.'
                }
            },
            'search_fields': [
                'title_only', 'title_abstract_only', 'authors', 'concepts',
                'full_data'
            ]
        },
        'grants': {
            'fields': {
                'funding_org_name': {
                    'type': 'label',
                    'description': 'Name of funding organisation.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'funding_org_city': {
                    'type': 'label',
                    'description': 'City name for funding organisation.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'funding_currency': {
                    'type': 'label',
                    'description': 'Original funding currency.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'original_title': {
                    'type': 'text',
                    'description':
                    'Title of the grant in its original language.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'funder_countries': {
                    'type':
                    'countries',
                    'description':
                    'The country linked to the organisation funding the grant, expressed as GeoNames codes.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'active_year': {
                    'type': 'integer',
                    'description': 'List of active years for a grant.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'research_orgs': {
                    'type':
                    'orgs',
                    'description':
                    'GRID organisations receiving the grant (note: identifiers are automatically extracted from the source text and can be missing in some cases).',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'research_org_countries': {
                    'type':
                    'countries',
                    'description':
                    'Country of the research organisations receiving the grant, expressed as GeoNames code and name.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'funding_usd': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in USD.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'title': {
                    'type':
                    'text',
                    'description':
                    'Title of the grant in English (if the grant language is not English, this field contains a translation of the title).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    False,
                    'is_facet':
                    False
                },
                'date_inserted': {
                    'type':
                    'timestamp',
                    'description':
                    'Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=`).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'start_date': {
                    'type':
                    'timestamp',
                    'description':
                    "Date when the grant starts, in the format 'YYYY-MM-DD'.",
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'funding_cad': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in CAD.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funding_nzd': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in NZD.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'research_org_name': {
                    'type':
                    'label',
                    'description':
                    'Name of the research organisations receiving the grant.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'title_language': {
                    'type':
                    'label',
                    'description':
                    'ISO 639-1 language code for the original grant title.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'project_num': {
                    'type':
                    'identifier',
                    'description':
                    'Grant identifier, as provided by the source (e.g., funder, aggregator) the grant was derived from.',
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
                    'type':
                    'orgs',
                    'description':
                    'The organisation funding the grant. This is normally a GRID organisation, but in very few cases a Dimensions funder ID is used.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'funding_gbp': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in GBP.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funding_eur': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in EUR.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'concepts': {
                    'type':
                    'text',
                    'description':
                    'Concepts describing the main topics of a grant (note: automatically derived from the grant text using machine learning).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    False,
                    'is_facet':
                    False
                },
                'HRCS_HC': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'funding_aud': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in AUD.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'language': {
                    'type':
                    'label',
                    'description':
                    'Grant original language, as ISO 639-1 language codes.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'funding_org_acronym': {
                    'type': 'label',
                    'description': 'Acronym for funding organisation.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'researchers': {
                    'type':
                    'researchers',
                    'description':
                    'Dimensions researchers IDs associated to the grant.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'abstract': {
                    'type': 'text',
                    'description':
                    'Abstract or summary from a grant proposal.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'research_org_cities': {
                    'type':
                    'cities',
                    'description':
                    'City of the research organisations receiving the grant, expressed as GeoNames id and name.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'research_org_state_codes': {
                    'type':
                    'states',
                    'description':
                    'State of the GRID organisations receiving the grant, expressed as GeoNames codes (ISO\u200c-3166-2).',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'id': {
                    'type': 'identifier',
                    'description': 'Dimensions grant ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funding_chf': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in CHF.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'linkout': {
                    'type': 'text',
                    'description': 'Original URL for the grant.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'FOR_first': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , first level or 2 digit codes.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'RCDC': {
                    'type':
                    'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'FOR': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , second level or 4 digit codes.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'end_date': {
                    'type': 'timestamp',
                    'description': 'Date when the grant ends.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'investigator_details': {
                    'type':
                    'json',
                    'description':
                    "Additional details about investigators, including affiliations and roles e.g. 'PI' or 'Co-PI' (note: if the investigator has a Dimensions researcher ID, that is returned as well).",
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'HRCS_RAC': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'funding_jpy': {
                    'type': 'financial',
                    'description': 'Funding amount awarded in JPY.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'start_year': {
                    'type': 'integer',
                    'description': 'Year when the grant starts.',
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
                },
                'funding': {
                    'name': 'funding',
                    'description': 'Total funding amount, in USD.'
                }
            },
            'search_fields': [
                'title_only', 'title_abstract_only', 'investigators',
                'concepts', 'full_data'
            ]
        },
        'patents': {
            'fields': {
                'assignee_names': {
                    'type': 'string',
                    'description': 'Name of the GRID assignees of the patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'jurisdiction': {
                    'type':
                    'string',
                    'description':
                    "The jurisdiction where the patent was granted, e.g. 'US', 'DE', 'EP'...",
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'publication_ids': {
                    'type':
                    'identifier',
                    'description':
                    'Dimensions IDs of the publications related to this patent (see also: :ref:`data-model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'title': {
                    'type': 'text',
                    'description': 'The title of the patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'date_inserted': {
                    'type':
                    'timestamp',
                    'description':
                    'Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=`).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'current_assignees': {
                    'type':
                    'orgs',
                    'description':
                    'GRID organisations currenlty owning the patent.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'legal_status': {
                    'type':
                    'string',
                    'description':
                    "The legal status of the patent, e.g. 'Granted', 'Active', 'Abandoned' etc..",
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'associated_grant_ids': {
                    'type':
                    'identifier',
                    'description':
                    'Dimensions IDs of the grants associated to the patent (see also: :ref:`data-model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'assignee_cities': {
                    'type':
                    'cities',
                    'description':
                    'City of the GRID assignees of the patent, expressed as GeoNames ID and name.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'year': {
                    'type': 'integer',
                    'description': 'The year the patent was filed.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'reference_ids': {
                    'type':
                    'identifier',
                    'description':
                    'Dimensions IDs of the patents which are cited by this patent (see also: :ref:`data-model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'HRCS_RAC': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
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
                'original_assignees': {
                    'type':
                    'orgs',
                    'description':
                    'GRID organisations that first owned the patent.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'funders': {
                    'type': 'orgs',
                    'description': 'GRID organisations funding the patent.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True
                },
                'publication_date': {
                    'type': 'timestamp',
                    'description': 'Date of publication of a patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'current_assignee_names': {
                    'type':
                    'string',
                    'description':
                    'Names of the GRID organisations currently holding the patent.',
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
                    'type':
                    'categories',
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'funder_groups': {
                    'type':
                    'org_groups',
                    'description':
                    'Organisation group the GRID patent funder belongs to.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'cited_by_ids': {
                    'type':
                    'identifier',
                    'description':
                    'Dimensions IDs of the patents that cite this patent (see also: :ref:`data-model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'publication_year': {
                    'type': 'integer',
                    'description': 'Year of publication of a patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'original_assignee_names': {
                    'type':
                    'string',
                    'description':
                    'Name of the GRID organisation that first owned the patent.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'ipcr': {
                    'type':
                    'identifier',
                    'description':
                    'International Patent Classification Reform number for a patent.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'abstract': {
                    'type': 'text',
                    'description': 'Abstract or description of the patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'assignee_state_codes': {
                    'type':
                    'states',
                    'description':
                    'State of the GRID assignee, expressed using GeoNames (ISO\u200c-3166-2) codes.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'granted_year': {
                    'type': 'integer',
                    'description': 'Year the patent was granted.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'assignee_countries': {
                    'type':
                    'countries',
                    'description':
                    'Country of the GRID assignees of the patent, expressed as GeoNames code and name.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'id': {
                    'type': 'identifier',
                    'description': 'Dimensions patent ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'assignees': {
                    'type':
                    'orgs',
                    'description':
                    'GRID organisations who own or have owned the rights of a patent (note: this is a combination of `current_assignees` and `original_assigness` fields).',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'additional_filters': {
                    'type':
                    'string',
                    'description':
                    "Additional filters describing the patents, e.g. whether it's about a 'Research Organisation', or it is part of the 'Orange Book'.",
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'assignee_state_names': {
                    'type': 'label',
                    'description': 'State name of GRID assignee, as a string.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'times_cited': {
                    'type':
                    'count',
                    'description':
                    'The number of times the patent has been cited by other patents.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'expiration_date': {
                    'type': 'timestamp',
                    'description': 'Date when the patent expires.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'priority_date': {
                    'type':
                    'timestamp',
                    'description':
                    'The earliest filing date in a family of patent applications.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'FOR_first': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , first level or 2 digit codes.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'filing_status': {
                    'type':
                    'string',
                    'description':
                    "Filing Status of the patent e.g. 'Application' or 'Grant'.",
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
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , second level or 4 digit codes.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'RCDC': {
                    'type':
                    'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'date': {
                    'type': 'timestamp',
                    'description': 'Date when the patent was filed.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'inventor_names': {
                    'type': 'string',
                    'description':
                    'Names of the people who invented the patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
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
            ['title_only', 'title_abstract_only', 'full_data']
        },
        'clinical_trials': {
            'fields': {
                'funder_countries': {
                    'type':
                    'countries',
                    'description':
                    'The country group the GRID funding organisations.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'gender': {
                    'type':
                    'string',
                    'description':
                    "The gender of the clinical trial subjects e.g. 'Male', 'Female' or 'All'.",
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'publication_ids': {
                    'type':
                    'identifier',
                    'description':
                    'Dimensions IDs of the publications related to this clinical trial (see also: :ref:`data-model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'title': {
                    'type': 'text',
                    'description': 'The title of the clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'date_inserted': {
                    'type':
                    'timestamp',
                    'description':
                    "Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=').",
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'phase': {
                    'type': 'string',
                    'description': 'Phase of the clinical trial, as a string.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'associated_grant_ids': {
                    'type':
                    'identifier',
                    'description':
                    'Dimensions IDs of the grants associated to the clinical trial (see also: :ref:`data-model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'HRCS_RAC': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'funders': {
                    'type':
                    'orgs',
                    'description':
                    'GRID funding organisations that are involved with the clinical trial.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'HRCS_HC': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'funder_groups': {
                    'type':
                    'org_groups',
                    'description':
                    'The organisation group the GRID funding organisations.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'conditions': {
                    'type':
                    'string',
                    'description':
                    "List of medical conditions names, e.g. 'Breast cancer' or 'Obesity'.",
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'registry': {
                    'type':
                    'string',
                    'description':
                    "The platform where the clinical trial has been registered, e.g. 'ClinicalTrials.gov' or 'EU-CTR'.",
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'abstract': {
                    'type':
                    'text',
                    'description':
                    'Abstract or description of the clinical trial.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    False,
                    'is_facet':
                    False
                },
                'id': {
                    'type': 'identifier',
                    'description': 'Dimensions clinical trial ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'organizations': {
                    'type':
                    'orgs',
                    'description':
                    'GRID organizations involved, e.g. as sponsors or collaborators.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'active_years': {
                    'type': 'integer',
                    'description':
                    'List of active years for a clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'linkout': {
                    'type': 'text',
                    'description': 'Original URL for the clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'FOR_first': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , first level or 2 digit codes.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'RCDC': {
                    'type':
                    'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'FOR': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , second level or 4 digit codes.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'investigator_details': {
                    'type':
                    'json',
                    'description':
                    'Additional details about investigators, including affiliations and roles.',
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
                    'description': 'Start date of a clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                }
            },
            'fieldsets': ['all', 'basics', 'extras'],
            'metrics': {
                'count': {
                    'name': 'count',
                    'description': 'Total count'
                }
            },
            'search_fields': [
                'title_only', 'title_abstract_only', 'investigators',
                'full_data'
            ]
        },
        'policy_documents': {
            'fields': {
                'health_research_areas': {
                    'type':
                    'categories',
                    'description':
                    '`Health Research Areas categorization <https://app.dimensions.ai/browse/publication/health_research_areas>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'publication_ids': {
                    'type':
                    'identifier',
                    'description':
                    'Dimensions IDs of the publications related to this policy document (see also: :ref:`data-model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'title': {
                    'type': 'string',
                    'description': 'Title of the policy document.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'date_inserted': {
                    'type':
                    'date',
                    'description':
                    'Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=`).',
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
                    'description':
                    'Year of publication of the policy document.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'publisher_org_city': {
                    'type':
                    'cities',
                    'description':
                    'City of the GRID organization publishing the policy document.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'HRCS_HC': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'publisher_org_state': {
                    'type':
                    'states',
                    'description':
                    'State of the GRID organization publishing the policy document.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'publisher_org_country': {
                    'type':
                    'countries',
                    'description':
                    'Country of the GRID organization publishing the policy document.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'publisher_org': {
                    'type':
                    'orgs',
                    'description':
                    'GRID organization publishing the policy document.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'id': {
                    'type': 'identifier',
                    'description': 'Dimensions policy document ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'linkout': {
                    'type': 'text',
                    'description': 'Original URL for the policy document.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'broad_research_areas': {
                    'type':
                    'categories',
                    'description':
                    '`Broad Research Areas categorization <https://app.dimensions.ai/browse/publication/broad_research_areas>`_  .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'FOR_first': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , first level or 2 digit codes.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'RCDC': {
                    'type':
                    'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'FOR': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , second level or 4 digit codes.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'HRCS_RAC': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_ .',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                }
            },
            'fieldsets': ['all', 'basics', 'categories'],
            'metrics': {
                'count': {
                    'name': 'count',
                    'description': 'Total count'
                }
            },
            'search_fields': ['title_only', 'full_data']
        },
        'researchers': {
            'fields': {
                'id': {
                    'type': 'identifier',
                    'description': 'Dimensions researcher ID.',
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
                'last_grant_year': {
                    'type':
                    'integer',
                    'description':
                    'Last year the researcher was awarded a grant.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'first_grant_year': {
                    'type':
                    'integer',
                    'description':
                    'First year the researcher was awarded a grant.',
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
                    'Indicates status of a researcher ID marked as obsolete. Empty means that the researcher ID was deleted. Otherwise ID provided means that is the new ID into which the obsolete one was redirected. If multiple values are available, it means that the original researcher ID was split into multiple IDs.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'orcid_id': {
                    'type': 'text',
                    'description': '`ORCID <https://orcid.org/>`_ ID.',
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
                },
                'research_orgs': {
                    'type':
                    'orgs',
                    'description':
                    'All research organizations linked to the researcher.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'obsolete': {
                    'type':
                    'integer',
                    'description':
                    'Indicates researcher ID status. 0 means that the researcher ID is still active, 1 means that the researcher ID is no longer valid. See the `redirect` field for further information on invalid researcher IDs.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'last_name': {
                    'type': 'string',
                    'description': 'Last Name.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'first_name': {
                    'type': 'string',
                    'description': 'First Name.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'total_grants': {
                    'type': 'count',
                    'description': 'Total grants count.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'current_research_org': {
                    'type':
                    'orgs',
                    'description':
                    'The most recent research organization linked to the researcher.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'total_publications': {
                    'type': 'count',
                    'description': 'Total publications count.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
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
                    'description': 'Dimensions ID of the category.',
                    'long_description': None,
                    'is_filter': True
                },
                'name': {
                    'name':
                    'name',
                    'type':
                    'string',
                    'description':
                    "Name of the category. Note: this may include an identifier from the original source. E.g., '2.1 Biological and endogenous factors' (HRCS_RAC codes) or '1103 Clinical Sciences' (FOR codes).",
                    'long_description':
                    None,
                    'is_filter':
                    True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'cities': {
            'fields': {
                'id': {
                    'name':
                    'id',
                    'type':
                    'identifier',
                    'description':
                    "GeoNames city ID (eg '5391811' for `geonames:5391811 <http://www.geonames.org/5391811>`_ )",
                    'long_description':
                    None,
                    'is_filter':
                    True
                },
                'name': {
                    'name': 'name',
                    'type': 'string',
                    'description': 'GeoNames city name.',
                    'long_description': None,
                    'is_filter': True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'countries': {
            'fields': {
                'id': {
                    'name':
                    'id',
                    'type':
                    'string',
                    'description':
                    "GeoNames country code (eg 'US' for `geonames:6252001 <http://www.geonames.org/6252001>`_ )",
                    'long_description':
                    None,
                    'is_filter':
                    True
                },
                'name': {
                    'name': 'name',
                    'type': 'string',
                    'description': 'GeoNames country name.',
                    'long_description': None,
                    'is_filter': True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'journals': {
            'fields': {
                'id': {
                    'name':
                    'id',
                    'type':
                    'string',
                    'description':
                    'Dimensions ID of a journal. E.g., `jour.1016355 <https://app.dimensions.ai/discover/publication?and_facet_source_title=jour.1016355>`_ or `jour.1077219 <https://app.dimensions.ai/discover/publication?and_facet_source_title=jour.1077219>`_ .',
                    'long_description':
                    None,
                    'is_filter':
                    True
                },
                'title': {
                    'name':
                    'title',
                    'type':
                    'string',
                    'description':
                    "Title of a journal publication. E.g. 'Nature' or 'The Lancet'",
                    'long_description':
                    None,
                    'is_filter':
                    True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'org_groups': {
            'fields': {
                'id': {
                    'name': 'id',
                    'type': 'identifier',
                    'description': 'Dimensions ID of the organization group.',
                    'long_description': None,
                    'is_filter': True
                },
                'name': {
                    'name':
                    'name',
                    'type':
                    'string',
                    'description':
                    "Name of the organization group. E.g., 'NIH' or 'ICRP'.",
                    'long_description':
                    None,
                    'is_filter':
                    True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'orgs': {
            'fields': {
                'id': {
                    'name':
                    'id',
                    'type':
                    'identifier',
                    'description':
                    'GRID ID of the organization. E.g., "grid.26999.3d".',
                    'long_description':
                    None,
                    'is_filter':
                    True
                },
                'name': {
                    'name':
                    'name',
                    'type':
                    'string',
                    'description':
                    'GRID name of the organization. E.g., "University of Tokyo" for `grid.26999.3d <https://grid.ac/institutes/grid.26999.3d>`_',
                    'long_description':
                    None,
                    'is_filter':
                    True
                },
                'acronym': {
                    'name':
                    'acronym',
                    'type':
                    'string',
                    'description':
                    'GRID acronym of the organization. E.g., "UT" for `grid.26999.3d <https://grid.ac/institutes/grid.26999.3d>`_',
                    'long_description':
                    None,
                    'is_filter':
                    True
                },
                'country_name': {
                    'name':
                    'country_name',
                    'type':
                    'string',
                    'description':
                    'GRID name of the organization country. E.g., "Japan" for `grid.26999.3d <https://grid.ac/institutes/grid.26999.3d>`_',
                    'long_description':
                    None,
                    'is_filter':
                    True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'states': {
            'fields': {
                'id': {
                    'name':
                    'id',
                    'type':
                    'identifier',
                    'description':
                    "GeoNames state code (ISO\u200c-3166-2). E.g., 'US.CA' for `geonames:5332921 <http://www.geonames.org/5332921>`_ .",
                    'long_description':
                    None,
                    'is_filter':
                    True
                },
                'name': {
                    'name': 'name',
                    'type': 'string',
                    'description': 'GeoNames state name (ISO\u200c-3166-2).',
                    'long_description': None,
                    'is_filter': True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'open_access': {
            'fields': {
                'id': {
                    'name':
                    'id',
                    'type':
                    'identifier',
                    'description':
                    "Dimensions ID of the open access category. E.g., one of 'closed', 'oa_all', 'gold_bronze', 'gold_pure', 'green_sub', 'gold_hybrid', 'green_pub', 'green_acc'. (see also the :ref:`publications` field ``open_access``).",
                    'long_description':
                    None,
                    'is_filter':
                    True
                },
                'name': {
                    'name':
                    'name',
                    'type':
                    'string',
                    'description':
                    "Name of the open access category. E.g., 'Closed' or 'Pure Gold'.",
                    'long_description':
                    None,
                    'is_filter':
                    True
                },
                'description': {
                    'name': 'description',
                    'type': 'text',
                    'description': 'Description of the open access category.',
                    'long_description': None,
                    'is_filter': False
                }
            },
            'fieldsets': ['all', 'basics']
        }
    }
}

