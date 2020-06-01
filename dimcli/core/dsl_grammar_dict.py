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
        '.export_as_json' : [],
        '.export_as_bar_chart' : [],
        '.export_as_jupyter' : [],
        '.record_notebook' : [],
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
    },
    'dimensions_object_id_patterns' : {
        'publications' : 'pub.',
        'grants' : 'grant.',
        # 'patents' : 'not available',
        'policy_documents' : 'policy.',
        # 'clinical_trials' : 'not available',
        # 'datasets' : 'not available'
        'researchers' : 'ur.',
        'organizations' : 'grid.',
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
# last updated: v 1.19 2019-09-05
#
# how to create:
#
# In [1]: import dimcli
# In [2]: dimcli.login()
# In [3]: dsl = dimcli.Dsl()
# In [4]: dsl.query("describe schema").json
#
# then save to a py file, reformat and save the results in GRAMMAR_DICT symbol
#
#
GRAMMAR_DICT = {
    'sources': {
        'publications': {
            'fields': {
                'doi': {
                    'type': 'string',
                    'description': 'Digital object identifier.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'research_org_names': {
                    'type':
                    'string',
                    'description':
                    'Names of organizations authors are affiliated to.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
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
                'category_uoa': {
                    'type':
                    'categories',
                    'description':
                    '`Units of Assessment <https://app.dimensions.ai/browse/publication/uoa>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'resulting_publication_doi': {
                    'type':
                    'string',
                    'description':
                    'For preprints, the DOIs of the resulting full publications.',
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
                'category_for': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'research_org_state_names': {
                    'type':
                    'string',
                    'description':
                    'State name of the organisations authors are affiliated to, as a string.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'category_hrcs_hc': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_hra': {
                    'type':
                    'categories',
                    'description':
                    '`Health Research Areas <https://app.dimensions.ai/browse/publication/health_research_areas>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_rcdc': {
                    'type':
                    'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'linkout': {
                    'type': 'string',
                    'description': 'Original URL for a publication full text.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'publisher': {
                    'type': 'string',
                    'description': 'Name of the publisher as a string.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'category_sdg': {
                    'type': 'categories',
                    'description': 'SDG - Sustainable Development Goals',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True
                },
                'issue': {
                    'type': 'string',
                    'description': 'The issue number of a publication.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'pmcid': {
                    'type': 'string',
                    'description': 'PubMed Central ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'mesh_terms': {
                    'type':
                    'string',
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
                'funder_countries': {
                    'type':
                    'countries',
                    'description':
                    'The country of the organisations funding this publication.',
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
                    'State of the organisations authors are affiliated to, expressed as GeoNames codes (ISO\u200c-3166-2).',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
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
                'book_series_title': {
                    'type':
                    'string',
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
                    'string',
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
                'category_hrcs_rac': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'research_org_cities': {
                    'type':
                    'cities',
                    'description':
                    'City of the organisations authors are affiliated to, expressed as GeoNames ID and name.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'research_org_country_names': {
                    'type':
                    'string',
                    'description':
                    'Country name of the organisations authors are affiliated to, as a string.',
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
                'book_title': {
                    'type':
                    'string',
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
                'funders': {
                    'type':
                    'organizations',
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
                'date_inserted': {
                    'type':
                    'date',
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
                'research_org_countries': {
                    'type':
                    'countries',
                    'description':
                    'Country of the organisations authors are affiliated to, identified using GeoNames codes (note: this field supports :ref:`filter-functions`: ``count``).',
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
                    'string',
                    'description':
                    'Grants supporting a publication, returned as a list of dimensions grants IDs  (see also: :ref:`publications_model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
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
                },
                'book_doi': {
                    'type':
                    'string',
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
                'volume': {
                    'type': 'string',
                    'description': 'Publication volume.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'issn': {
                    'type': 'string',
                    'description': 'International Standard Serial Number',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'journal': {
                    'type': 'journals',
                    'description': 'The journal a publication belongs to.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True
                },
                'concepts': {
                    'type': 'json',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'authors': {
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
                'research_orgs': {
                    'type':
                    'organizations',
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
                'researchers': {
                    'type':
                    'researchers',
                    'description':
                    "Researcher IDs matched to the publication's authors list. (note: this returns only the disambiguated authors of a publication; in order to get the full authors list, the field `authors` should be used). This field supports :ref:`filter-functions`: ``count``.",
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
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
                'concepts_scores': {
                    'type': 'json',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'reference_ids': {
                    'type':
                    'string',
                    'description':
                    'Dimensions publication ID for publications in the references list, i.e. outgoing citations (see also: :ref:`publications_model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'category_icrp_cso': {
                    'type':
                    'categories',
                    'description':
                    '`ICRP Common Scientific Outline <https://app.dimensions.ai/browse/publication/cso>`_',
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
                    'type': 'string',
                    'description': 'Dimensions publication ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'type': {
                    'type':
                    'string',
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
                'pmid': {
                    'type': 'string',
                    'description': 'PubMed ID.',
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
                    False
                },
                'title': {
                    'type': 'string',
                    'description': 'Title of a publication.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'times_cited': {
                    'type':
                    'integer',
                    'description':
                    'Number of citations (note: does not support emptiness filters).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_icrp_ct': {
                    'type':
                    'categories',
                    'description':
                    '`ICRP Cancer Types <https://app.dimensions.ai/browse/publication/cancer_types>`_',
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
                'category_bra': {
                    'type':
                    'categories',
                    'description':
                    '`Broad Research Areas <https://app.dimensions.ai/browse/publication/broad_research_areas>`_',
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
            'fieldsets': ['all', 'basics', 'extras', 'book', 'categories'],
            'metrics': {
                'count': {
                    'name': 'count',
                    'description': 'Total count'
                },
                'altmetric_median': {
                    'name': 'altmetric_median',
                    'description': 'Median Altmetric attention score'
                },
                'altmetric_avg': {
                    'name': 'altmetric_avg',
                    'description': 'Altmetric attention score mean'
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
                    'Geometric mean of `field_citation_ratio` field (note: This field cannot be used for sorting results).'
                }
            },
            'search_fields': [
                'noun_phrases', 'authors', 'full_data_exact', 'full_data',
                'title_abstract_only', 'title_only', 'concepts'
            ]
        },
        'grants': {
            'fields': {
                'category_uoa': {
                    'type':
                    'categories',
                    'description':
                    '`Units of Assessment <https://app.dimensions.ai/browse/publication/uoa>`_',
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
                    'type': 'float',
                    'description': 'Funding amount awarded in AUD.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'category_for': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_hrcs_hc': {
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
                'category_hra': {
                    'type':
                    'categories',
                    'description':
                    '`Health Research Areas <https://app.dimensions.ai/browse/publication/health_research_areas?redirect_path=/discover/publication>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'linkout': {
                    'type': 'string',
                    'description': 'Original URL for the grant.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'category_rcdc': {
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
                'end_date': {
                    'type': 'date',
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
                'language': {
                    'type':
                    'string',
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
                'funding_gbp': {
                    'type': 'float',
                    'description': 'Funding amount awarded in GBP.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'research_org_state_codes': {
                    'type':
                    'states',
                    'description':
                    'State of the organisations receiving the grant, expressed as GeoNames codes (ISO\u200c-3166-2).',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_hrcs_rac': {
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
                'funding_jpy': {
                    'type': 'float',
                    'description': 'Funding amount awarded in JPY.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funding_nzd': {
                    'type': 'float',
                    'description': 'Funding amount awarded in NZD.',
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
                },
                'funders': {
                    'type':
                    'organizations',
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
                'funding_currency': {
                    'type': 'string',
                    'description': 'Original funding currency.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
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
                'grant_number': {
                    'type':
                    'string',
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
                'active_year': {
                    'type': 'integer',
                    'description': 'List of active years for a grant.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'funding_org_city': {
                    'type': 'string',
                    'description': 'City name for funding organisation.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'funding_chf': {
                    'type': 'float',
                    'description': 'Funding amount awarded in CHF.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funding_org_name': {
                    'type': 'string',
                    'description': 'Name of funding organisation.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'language_title': {
                    'type':
                    'string',
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
                'foa_number': {
                    'type':
                    'string',
                    'description':
                    'The funding opportunity announcement (FOA) number, where available e.g. for grants from the US National Institute of Health (NIH) or from the National Science Foundation (NSF).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'funding_eur': {
                    'type': 'float',
                    'description': 'Funding amount awarded in EUR.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'original_title': {
                    'type': 'string',
                    'description':
                    'Title of the grant in its original language.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'concepts': {
                    'type':
                    'string',
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
                'funding_org_acronym': {
                    'type': 'string',
                    'description': 'Acronym for funding organisation.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'research_orgs': {
                    'type':
                    'organizations',
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
                    'type': 'string',
                    'description':
                    'Abstract or summary from a grant proposal.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'category_icrp_cso': {
                    'type':
                    'categories',
                    'description':
                    '`ICRP Common Scientific Outline <https://app.dimensions.ai/browse/publication/cso>`_',
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
                    'type': 'string',
                    'description': 'Dimensions grant ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funding_usd': {
                    'type': 'float',
                    'description': 'Funding amount awarded in USD.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'title': {
                    'type':
                    'string',
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
                'start_date': {
                    'type':
                    'date',
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
                    'type': 'float',
                    'description': 'Funding amount awarded in CAD.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'category_icrp_ct': {
                    'type':
                    'categories',
                    'description':
                    '`ICRP Cancer Types <https://app.dimensions.ai/browse/publication/cancer_types>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_bra': {
                    'type':
                    'categories',
                    'description':
                    '`Broad Research Areas <https://app.dimensions.ai/browse/publication/broad_research_areas?redirect_path=/discover/publication>`_',
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
            'fieldsets': ['all', 'basics', 'extras', 'categories'],
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
                'noun_phrases', 'full_data', 'investigators',
                'title_abstract_only', 'title_only', 'concepts'
            ]
        },
        'patents': {
            'fields': {
                'associated_grant_ids': {
                    'type':
                    'string',
                    'description':
                    'Dimensions IDs of the grants associated to the patent (see also: :ref:`patents_model` section).',
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
                    'City of the assignees of the patent, expressed as GeoNames ID and name (note: this value is extracted independently from GRID).',
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
                    True
                },
                'assignee_countries': {
                    'type':
                    'countries',
                    'description':
                    'Country of the assignees of the patent, expressed as GeoNames code and name (note: this value is extracted independently from GRID).',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_for': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'publication_year': {
                    'type': 'integer',
                    'description': 'Year of publication of a patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'category_hrcs_hc': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_hra': {
                    'type':
                    'categories',
                    'description':
                    '`Health Research Areas <https://app.dimensions.ai/browse/publication/health_research_areas?redirect_path=/discover/publication>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_rcdc': {
                    'type':
                    'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_',
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
                    'type':
                    'integer',
                    'description':
                    'The year on which the official body grants the patent.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'assignees': {
                    'type':
                    'organizations',
                    'description':
                    'Disambiguated GRID organisations who own or have owned the rights of a patent (note: this is a combination of `current_assignees` and `original_assignees` fields).',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_hrcs_rac': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'expiration_date': {
                    'type': 'date',
                    'description': 'Date when the patent expires.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'date': {
                    'type': 'date',
                    'description': 'Date when the patent was filed.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'funders': {
                    'type': 'organizations',
                    'description': 'GRID organisations funding the patent.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True
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
                'cpc': {
                    'type':
                    'string',
                    'description':
                    '`Cooperative Patent Classification Categorization <https://www.epo.org/searching-for-patents/helpful-resources/first-time-here/classification/cpc.html>`_.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
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
                'priority_year': {
                    'type':
                    'integer',
                    'description':
                    'The filing year of the earliest application of which priority is claimed.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'publication_ids': {
                    'type':
                    'string',
                    'description':
                    'Dimensions IDs of the publications related to this patent (see also: :ref:`patents_model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'assignee_state_codes': {
                    'type':
                    'states',
                    'description':
                    'State of the assignee, expressed using GeoNames (ISO\u200c-3166-2) codes (note: this value is extracted independently from GRID).',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'original_assignees': {
                    'type':
                    'organizations',
                    'description':
                    'Disambiguated GRID organisations that first owned the patent.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'assignee_names': {
                    'type':
                    'string',
                    'description':
                    'Name of assignees of the patent, as they appear in the original document.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'current_assignee_names': {
                    'type':
                    'string',
                    'description':
                    'Names of the organisations currently holding the patent, as they appear in the original document.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'granted_date': {
                    'type':
                    'date',
                    'description':
                    'The date on which the official body grants the patent.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'original_assignee_names': {
                    'type':
                    'string',
                    'description':
                    'Name of the organisations that first owned the patent, as they appear in the original document.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'publication_date': {
                    'type': 'date',
                    'description': 'Date of publication of a patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'ipcr': {
                    'type':
                    'string',
                    'description':
                    '`International Patent Classification Reform Categorization <https://www.wipo.int/classifications/ipc/en/faq/>`_.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'inventor_names': {
                    'type': 'string',
                    'description':
                    'Names of the people who invented the patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'priority_date': {
                    'type':
                    'date',
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
                'current_assignees': {
                    'type':
                    'organizations',
                    'description':
                    'Disambiguated GRID organisations currenlty owning the patent.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'researchers': {
                    'type':
                    'researchers',
                    'description':
                    "Researcher IDs matched to the patent's inventors list. (note: this returns only the disambiguated inventors of a patent; in order to get the full list of inventors, the field `inventors` should be used).",
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
                    'type': 'string',
                    'description': 'Abstract or description of the patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'reference_ids': {
                    'type':
                    'string',
                    'description':
                    'Dimensions IDs of the patents which are cited by this patent (see also: :ref:`patents_model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'category_icrp_cso': {
                    'type':
                    'categories',
                    'description':
                    '`ICRP Common Scientific Outline <https://app.dimensions.ai/browse/publication/cso>`_',
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
                    'type': 'string',
                    'description': 'Dimensions patent ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'title': {
                    'type': 'string',
                    'description': 'The title of the patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'times_cited': {
                    'type':
                    'integer',
                    'description':
                    'The number of times the patent has been cited by other patents.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_icrp_ct': {
                    'type':
                    'categories',
                    'description':
                    '`ICRP Cancer Types <https://app.dimensions.ai/browse/publication/cancer_types>`_',
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
                'category_bra': {
                    'type':
                    'categories',
                    'description':
                    '`Broad Research Areas <https://app.dimensions.ai/browse/publication/broad_research_areas?redirect_path=/discover/publication>`_',
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
                    'string',
                    'description':
                    'Dimensions IDs of the patents that cite this patent (see also: :ref:`patents_model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                }
            },
            'fieldsets': ['all', 'basics', 'extras', 'categories'],
            'metrics': {
                'count': {
                    'name': 'count',
                    'description': 'Total count'
                }
            },
            'search_fields':
            ['inventors', 'full_data', 'title_only', 'title_abstract_only']
        },
        'clinical_trials': {
            'fields': {
                'acronym': {
                    'type': 'string',
                    'description': 'Acronym of the clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'associated_grant_ids': {
                    'type':
                    'string',
                    'description':
                    'Dimensions IDs of the grants associated to the clinical trial (see also: :ref:`clinical_trials_model` section).',
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
                'category_for': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_',
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
                'category_hrcs_hc': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_hra': {
                    'type':
                    'categories',
                    'description':
                    '`Health Research Areas <https://app.dimensions.ai/browse/publication/health_research_areas?redirect_path=/discover/publication>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'linkout': {
                    'type': 'string',
                    'description': 'Original URL for the clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'category_rcdc': {
                    'type':
                    'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_',
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
                'funder_countries': {
                    'type': 'countries',
                    'description':
                    'The country group the funding organisations.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True
                },
                'category_hrcs_rac': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_',
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
                'funders': {
                    'type':
                    'organizations',
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
                'date': {
                    'type': 'date',
                    'description': 'Start date of a clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'date_inserted': {
                    'type':
                    'date',
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
                'publication_ids': {
                    'type':
                    'string',
                    'description':
                    'Dimensions IDs of the publications related to this clinical trial (see also: :ref:`clinical_trials_model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'brief_title': {
                    'type': 'string',
                    'description': 'Brief title of the clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'interventions': {
                    'type':
                    'json',
                    'description':
                    "Structured JSON object containing information about the clinical trial's interventions according to the research plan or protocol created by the investigators.",
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
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
                'research_orgs': {
                    'type':
                    'organizations',
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
                'researchers': {
                    'type':
                    'researchers',
                    'description':
                    'Dimensions researchers IDs associated to the clinical trial.',
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
                    'type':
                    'string',
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
                'category_icrp_cso': {
                    'type':
                    'categories',
                    'description':
                    '`ICRP Common Scientific Outline <https://app.dimensions.ai/browse/publication/cso>`_',
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
                    'type': 'string',
                    'description': 'Dimensions clinical trial ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'title': {
                    'type': 'string',
                    'description': 'The title of the clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
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
                'category_icrp_ct': {
                    'type':
                    'categories',
                    'description':
                    '`ICRP Cancer Types <https://app.dimensions.ai/browse/publication/cancer_types>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_bra': {
                    'type':
                    'categories',
                    'description':
                    '`Broad Research Areas <https://app.dimensions.ai/browse/publication/broad_research_areas?redirect_path=/discover/publication>`_',
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
            'fieldsets': ['all', 'basics', 'extras', 'categories'],
            'metrics': {
                'count': {
                    'name': 'count',
                    'description': 'Total count'
                }
            },
            'search_fields': [
                'investigators', 'full_data', 'title_only',
                'title_abstract_only'
            ]
        },
        'policy_documents': {
            'fields': {
                'category_for': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_hrcs_hc': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_hra': {
                    'type':
                    'categories',
                    'description':
                    '`Health Research Areas <https://app.dimensions.ai/browse/publication/health_research_areas?redirect_path=/discover/publication>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_rcdc': {
                    'type':
                    'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'linkout': {
                    'type': 'string',
                    'description': 'Original URL for the policy document.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'publisher_org_state': {
                    'type':
                    'states',
                    'description':
                    'State of the organization publishing the policy document.',
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
                    'Country of the organization publishing the policy document.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'publisher_org_city': {
                    'type':
                    'cities',
                    'description':
                    'City of the organization publishing the policy document.',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_hrcs_rac': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
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
                'publication_ids': {
                    'type':
                    'string',
                    'description':
                    'Dimensions IDs of the publications related to this policy document (see also: :ref:`policy_documents_model` section).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'publisher_org': {
                    'type':
                    'organizations',
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
                'category_icrp_cso': {
                    'type':
                    'categories',
                    'description':
                    '`ICRP Common Scientific Outline <https://app.dimensions.ai/browse/publication/cso>`_',
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
                    'type': 'string',
                    'description': 'Dimensions policy document ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'title': {
                    'type': 'string',
                    'description': 'Title of the policy document.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'category_icrp_ct': {
                    'type':
                    'categories',
                    'description':
                    '`ICRP Cancer Types <https://app.dimensions.ai/browse/publication/cancer_types>`_',
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
                    'description':
                    'Year of publication of the policy document.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'category_bra': {
                    'type':
                    'categories',
                    'description':
                    '`Broad Research Areas <https://app.dimensions.ai/browse/publication/broad_research_areas?redirect_path=/discover/publication>`_',
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
            'search_fields': ['full_data', 'title_only']
        },
        'researchers': {
            'fields': {
                'research_orgs': {
                    'type':
                    'organizations',
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
                'total_grants': {
                    'type': 'integer',
                    'description': 'Total grants count.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'nih_ppid': {
                    'type':
                    'string',
                    'description':
                    'The PI Profile ID (i.e., ppid) is a Researcher ID from the US National Institute of Health (NIH).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'first_publication_year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'first_name': {
                    'type': 'string',
                    'description': 'First Name.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'last_name': {
                    'type': 'string',
                    'description': 'Last Name.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'id': {
                    'type': 'string',
                    'description': 'Dimensions researcher ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
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
                'redirect': {
                    'type':
                    'string',
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
                'last_publication_year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'current_research_org': {
                    'type':
                    'organizations',
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
                'total_publications': {
                    'type': 'integer',
                    'description': 'Total publications count.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'orcid_id': {
                    'type': 'string',
                    'description': '`ORCID <https://orcid.org/>`_ ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
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
                }
            },
            'fieldsets': ['all', 'basics', 'extras'],
            'metrics': {
                'count': {
                    'name': 'count',
                    'description': 'Total count'
                }
            },
            'search_fields': []
        },
        'organizations': {
            'fields': {
                'acronym': {
                    'type':
                    'string',
                    'description':
                    'GRID acronym of the organization. E.g., "UT" for `grid.26999.3d <https://grid.ac/institutes/grid.26999.3d>`_',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'wikidata_ids': {
                    'type': 'string',
                    'description': 'WikiData IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'types': {
                    'type':
                    'string',
                    'description':
                    'Type of an organization. Available types include: ``Company``, ``Education``, ``Healthcare``, ``Nonprofit``, ``Facility``, ``Other``, ``Government``, ``Archive``, ``Education,Company``, ``Education,Facility``, ``Education,Healthcare``, ``Education,Other``, ``Archive,Nonprofit``. Furhter explanation is on the `GRID <https://www.grid.ac/pages/policies>`_ website.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'established': {
                    'type': 'integer',
                    'description':
                    'Year when the organization was estabilished',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'nuts_level2_code': {
                    'type':
                    'string',
                    'description':
                    'Level 2 code for this organization, based on `Nomenclature of Territorial Units for Statistics <https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics>`_ (NUTS) codes of the European Union.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'nuts_level1_name': {
                    'type':
                    'string',
                    'description':
                    'Level 1 name for this organization, based on `Nomenclature of Territorial Units for Statistics <https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics>`_ (NUTS) codes of the European Union.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'linkout': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'latitude': {
                    'type': 'float',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'name': {
                    'type':
                    'string',
                    'description':
                    'GRID name of the organization. E.g., "University of Tokyo" for `grid.26999.3d <https://grid.ac/institutes/grid.26999.3d>`_',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'ucas_ids': {
                    'type': 'string',
                    'description': 'UCAS IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'nuts_level2_name': {
                    'type':
                    'string',
                    'description':
                    'Level 2 name for this organization, based on `Nomenclature of Territorial Units for Statistics <https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics>`_ (NUTS) codes of the European Union.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'organization_child_ids': {
                    'type': 'string',
                    'description': 'Child organization IDs',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'cnrs_ids': {
                    'type': 'string',
                    'description': 'CNRS IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'country_name': {
                    'type':
                    'string',
                    'description':
                    'GRID name of the organization country. E.g., "Japan" for `grid.26999.3d <https://grid.ac/institutes/grid.26999.3d>`_',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'ukprn_ids': {
                    'type': 'string',
                    'description': 'UKPRN IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'wikipedia_url': {
                    'type': 'string',
                    'description': 'Wikipedia URL',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'city_name': {
                    'type':
                    'string',
                    'description':
                    'GRID name of the organization country. E.g., "Bethesda" for `grid.419635.c <https://grid.ac/institutes/grid.419635.c>`_',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'hesa_ids': {
                    'type': 'string',
                    'description': 'HESA IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'longitude': {
                    'type': 'float',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'organization_related_ids': {
                    'type': 'string',
                    'description': 'Related organization IDs',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'orgref_ids': {
                    'type': 'string',
                    'description': 'OrgRef IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'organization_parent_ids': {
                    'type': 'string',
                    'description': 'Parent organization IDs',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'state_name': {
                    'type':
                    'string',
                    'description':
                    'GRID name of the organization country. E.g., "Maryland" for `grid.419635.c <https://grid.ac/institutes/grid.419635.c>`_',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'id': {
                    'type':
                    'string',
                    'description':
                    'GRID ID of the organization. E.g., "grid.26999.3d".',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'nuts_level1_code': {
                    'type':
                    'string',
                    'description':
                    'Level 1 code for this organization, based on `Nomenclature of Territorial Units for Statistics <https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics>`_ (NUTS) codes of the European Union.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'isni_ids': {
                    'type': 'string',
                    'description': 'ISNI IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'external_ids_fundref': {
                    'type': 'string',
                    'description': 'Fundref IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                }
            },
            'fieldsets': ['all', 'basics', 'nuts'],
            'metrics': {
                'count': {
                    'name': 'count',
                    'description': 'Total count'
                }
            },
            'search_fields': ['full_data']
        },
        'datasets': {
            'fields': {
                'doi': {
                    'type': 'string',
                    'description': 'Dataset DOI.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'associated_grant_ids': {
                    'type':
                    'string',
                    'description':
                    'The Dimensions IDs of the grants linked to the publication the dataset is associated with.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'date_embargo': {
                    'type': 'date',
                    'description': 'The embargo date of the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'category_for': {
                    'type':
                    'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_hrcs_hc': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_hra': {
                    'type':
                    'categories',
                    'description':
                    '`Health Research Areas <https://app.dimensions.ai/browse/publication/health_research_areas>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_rcdc': {
                    'type':
                    'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_',
                    'long_description':
                    None,
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
                'keywords': {
                    'type':
                    'string',
                    'description':
                    'Keywords used to describe the dataset (from authors).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'license': {
                    'type':
                    'json',
                    'description':
                    'The dataset licence, as a structured JSON containing the license name, URL, and value.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'category_hrcs_rac': {
                    'type':
                    'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'research_org_cities': {
                    'type':
                    'cities',
                    'description':
                    'City of the organisations the publication authors are affiliated to, expressed as GeoNames ID and name.',
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
                    'type': 'organizations',
                    'description':
                    'The GRID organisations funding the dataset.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True
                },
                'date': {
                    'type':
                    'date',
                    'description':
                    'The publication date of the dataset, eg "2018-01-01".',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'date_inserted': {
                    'type':
                    'date',
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
                'research_org_countries': {
                    'type':
                    'countries',
                    'description':
                    'Country of the organisations the publication authors are affiliated to, identified using GeoNames codes (note: this field supports count: count)..',
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
                    'string',
                    'description':
                    'The Dimensions IDs of the publications the dataset cites.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'figshare_url': {
                    'type': 'string',
                    'description': 'Figshare URL for the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'associated_publication_id': {
                    'type':
                    'string',
                    'description':
                    'The Dimensions ID of the publication linked to the dataset (single value).',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    False
                },
                'language_title': {
                    'type':
                    'string',
                    'description':
                    'Dataset title language, as ISO 639-1 language codes.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'journal': {
                    'type': 'journals',
                    'description': 'The journal a data set belongs to.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True
                },
                'authors': {
                    'type':
                    'json',
                    'description':
                    'Ordered list of the dataset authors. ORCIDs are included if available.',
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
                    'type':
                    'organizations',
                    'description':
                    'GRID organisations linked to the publication associated to the dataset (note: this field supports count: count).',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'description': {
                    'type': 'string',
                    'description': 'Description of the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'researchers': {
                    'type':
                    'researchers',
                    'description':
                    "Dimensions researchers IDs associated to the dataset's associated publication. Note: in most cases, these would be the same as the dataset authors.",
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'category_icrp_cso': {
                    'type':
                    'categories',
                    'description':
                    '`ICRP Common Scientific Outline <https://app.dimensions.ai/browse/publication/cso>`_',
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
                    'type': 'string',
                    'description': 'Dimensions dataset ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'date_modified': {
                    'type': 'date',
                    'description':
                    'The last modification date of the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'title': {
                    'type': 'string',
                    'description': 'Title of the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False
                },
                'category_icrp_ct': {
                    'type':
                    'categories',
                    'description':
                    '`ICRP Cancer Types <https://app.dimensions.ai/browse/publication/cancer_types>`_',
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
                    'description': 'Year of publication of the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True
                },
                'category_bra': {
                    'type':
                    'categories',
                    'description':
                    '`Broad Research Areas <https://app.dimensions.ai/browse/publication/broad_research_areas>`_',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'language_desc': {
                    'type':
                    'string',
                    'description':
                    'Dataset title language, as ISO 639-1 language codes.',
                    'long_description':
                    None,
                    'is_entity':
                    False,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'research_org_states': {
                    'type':
                    'states',
                    'description':
                    'State of the organisations the publication authors are affiliated to, expressed as GeoNames codes (ISO\u200c-3166-2).',
                    'long_description':
                    None,
                    'is_entity':
                    True,
                    'is_filter':
                    True,
                    'is_facet':
                    True
                },
                'date_created': {
                    'type': 'date',
                    'description': 'The creation date of the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False
                },
                'repository_id': {
                    'type': 'string',
                    'description': 'The ID of the repository of the dataset.',
                    'long_description': None,
                    'is_entity': False,
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
            'search_fields':
            ['full_data', 'title_only', 'title_abstract_only']
        }
    },
    'entities': {
        'categories': {
            'fields': {
                'id': {
                    'name': 'string',
                    'type': 'string',
                    'description': 'Dimensions ID of the category.',
                    'long_description': None,
                    'is_filter': True
                },
                'name': {
                    'name':
                    'string',
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
                    'string',
                    'type':
                    'string',
                    'description':
                    "GeoNames city ID (eg '5391811' for `geonames:5391811 <http://www.geonames.org/5391811>`_ )",
                    'long_description':
                    None,
                    'is_filter':
                    True
                },
                'name': {
                    'name': 'string',
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
                    'string',
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
                    'name': 'string',
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
                    'string',
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
                    'string',
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
                    'name': 'string',
                    'type': 'string',
                    'description': 'Dimensions ID of the organization group.',
                    'long_description': None,
                    'is_filter': True
                },
                'name': {
                    'name':
                    'string',
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
        'states': {
            'fields': {
                'id': {
                    'name':
                    'string',
                    'type':
                    'string',
                    'description':
                    "GeoNames state code (ISO\u200c-3166-2). E.g., 'US.CA' for `geonames:5332921 <http://www.geonames.org/5332921>`_ .",
                    'long_description':
                    None,
                    'is_filter':
                    True
                },
                'name': {
                    'name': 'string',
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
                    'string',
                    'type':
                    'string',
                    'description':
                    "Dimensions ID of the open access category. E.g., one of 'closed', 'oa_all', 'gold_bronze', 'gold_pure', 'green_sub', 'gold_hybrid', 'green_pub', 'green_acc'. (see also the :ref:`publications` field ``open_access``).",
                    'long_description':
                    None,
                    'is_filter':
                    True
                },
                'name': {
                    'name':
                    'string',
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
                    'name': 'string',
                    'type': 'string',
                    'description': 'Description of the open access category.',
                    'long_description': None,
                    'is_filter': False
                }
            },
            'fieldsets': ['all', 'basics']
        }
    }
}
