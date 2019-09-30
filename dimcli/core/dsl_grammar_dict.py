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
    'entities': {
        'categories': {
            'fields': {
                'id': {
                    'description': 'Dimensions ID of the category.',
                    'is_filter': True,
                    'long_description': None,
                    'name': 'id',
                    'type': 'string'
                },
                'name': {
                    'description':
                    "Name of the category. Note: this may include an identifier from the original source. E.g., '2.1 Biological and endogenous factors' (HRCS_RAC codes) or '1103 Clinical Sciences' (FOR codes).",
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'name':
                    'name',
                    'type':
                    'string'
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'cities': {
            'fields': {
                'id': {
                    'description':
                    "GeoNames city ID (eg '5391811' for `geonames:5391811 <http://www.geonames.org/5391811>`_ )",
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'name':
                    'id',
                    'type':
                    'identifier'
                },
                'name': {
                    'description': 'GeoNames city name.',
                    'is_filter': True,
                    'long_description': None,
                    'name': 'name',
                    'type': 'string'
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'countries': {
            'fields': {
                'id': {
                    'description':
                    "GeoNames country code (eg 'US' for `geonames:6252001 <http://www.geonames.org/6252001>`_ )",
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'name':
                    'id',
                    'type':
                    'string'
                },
                'name': {
                    'description': 'GeoNames country name.',
                    'is_filter': True,
                    'long_description': None,
                    'name': 'name',
                    'type': 'string'
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'journals': {
            'fields': {
                'id': {
                    'description':
                    'Dimensions ID of a journal. E.g., `jour.1016355 <https://app.dimensions.ai/discover/publication?and_facet_source_title=jour.1016355>`_ or `jour.1077219 <https://app.dimensions.ai/discover/publication?and_facet_source_title=jour.1077219>`_ .',
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'name':
                    'id',
                    'type':
                    'string'
                },
                'title': {
                    'description':
                    "Title of a journal publication. E.g. 'Nature' or 'The Lancet'",
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'name':
                    'title',
                    'type':
                    'string'
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'open_access': {
            'fields': {
                'description': {
                    'description': 'Description of the open access category.',
                    'is_filter': False,
                    'long_description': None,
                    'name': 'description',
                    'type': 'text'
                },
                'id': {
                    'description':
                    "Dimensions ID of the open access category. E.g., one of 'closed', 'oa_all', 'gold_bronze', 'gold_pure', 'green_sub', 'gold_hybrid', 'green_pub', 'green_acc'. (see also the :ref:`publications` field ``open_access``).",
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'name':
                    'id',
                    'type':
                    'identifier'
                },
                'name': {
                    'description':
                    "Name of the open access category. E.g., 'Closed' or 'Pure Gold'.",
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'name':
                    'name',
                    'type':
                    'string'
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'org_groups': {
            'fields': {
                'id': {
                    'description': 'Dimensions ID of the organization group.',
                    'is_filter': True,
                    'long_description': None,
                    'name': 'id',
                    'type': 'identifier'
                },
                'name': {
                    'description':
                    "Name of the organization group. E.g., 'NIH' or 'ICRP'.",
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'name':
                    'name',
                    'type':
                    'string'
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'orgs': {
            'fields': {
                'acronym': {
                    'description':
                    'GRID acronym of the organization. E.g., "UT" for `grid.26999.3d <https://grid.ac/institutes/grid.26999.3d>`_',
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'name':
                    'acronym',
                    'type':
                    'string'
                },
                'country_name': {
                    'description':
                    'GRID name of the organization country. E.g., "Japan" for `grid.26999.3d <https://grid.ac/institutes/grid.26999.3d>`_',
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'name':
                    'country_name',
                    'type':
                    'string'
                },
                'id': {
                    'description':
                    'GRID ID of the organization. E.g., "grid.26999.3d".',
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'name':
                    'id',
                    'type':
                    'identifier'
                },
                'name': {
                    'description':
                    'GRID name of the organization. E.g., "University of Tokyo" for `grid.26999.3d <https://grid.ac/institutes/grid.26999.3d>`_',
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'name':
                    'name',
                    'type':
                    'string'
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'states': {
            'fields': {
                'id': {
                    'description':
                    "GeoNames state code (ISO\u200c-3166-2). E.g., 'US.CA' for `geonames:5332921 <http://www.geonames.org/5332921>`_ .",
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'name':
                    'id',
                    'type':
                    'identifier'
                },
                'name': {
                    'description': 'GeoNames state name (ISO\u200c-3166-2).',
                    'is_filter': True,
                    'long_description': None,
                    'name': 'name',
                    'type': 'string'
                }
            },
            'fieldsets': ['all', 'basics']
        }
    },
    'sources': {
        'clinical_trials': {
            'fields': {
                'FOR': {
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , second level or 4 digit codes.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'FOR_first': {
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , first level or 2 digit codes.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'abstract': {
                    'description':
                    'Abstract or description of the clinical trial.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    False,
                    'long_description':
                    None,
                    'type':
                    'text'
                },
                'active_years': {
                    'description':
                    'List of active years for a clinical trial.',
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'integer'
                },
                'associated_grant_ids': {
                    'description':
                    'Dimensions IDs of the grants associated to the clinical trial (see also: :ref:`data-model` section).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'identifier'
                },
                'category_bra': {
                    'description':
                    '`Broad Research Areas <https://app.dimensions.ai/browse/publication/broad_research_areas?redirect_path=/discover/publication>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hra': {
                    'description':
                    '`Health Research Areas <https://app.dimensions.ai/browse/publication/health_research_areas?redirect_path=/discover/publication>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hrcs_hc': {
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hrcs_rac': {
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_rcdc': {
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'conditions': {
                    'description':
                    "List of medical conditions names, e.g. 'Breast cancer' or 'Obesity'.",
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'string'
                },
                'date': {
                    'description': 'Start date of a clinical trial.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'timestamp'
                },
                'date_inserted': {
                    'description':
                    "Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=').",
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'timestamp'
                },
                'funder_countries': {
                    'description':
                    'The country group the GRID funding organisations.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'countries'
                },
                'funder_groups': {
                    'description':
                    'The organisation group the GRID funding organisations.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'org_groups'
                },
                'funders': {
                    'description':
                    'GRID funding organisations that are involved with the clinical trial.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'orgs'
                },
                'gender': {
                    'description':
                    "The gender of the clinical trial subjects e.g. 'Male', 'Female' or 'All'.",
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'string'
                },
                'id': {
                    'description': 'Dimensions clinical trial ID',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'identifier'
                },
                'investigator_details': {
                    'description':
                    'Additional details about investigators, including affiliations and roles.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'json'
                },
                'linkout': {
                    'description': 'Original URL for the clinical trial.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': False,
                    'long_description': None,
                    'type': 'text'
                },
                'organizations': {
                    'description':
                    'GRID organizations involved, e.g. as sponsors or collaborators.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'orgs'
                },
                'phase': {
                    'description': 'Phase of the clinical trial, as a string.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'string'
                },
                'publication_ids': {
                    'description':
                    'Dimensions IDs of the publications related to this clinical trial (see also: :ref:`data-model` section).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'identifier'
                },
                'registry': {
                    'description':
                    "The platform where the clinical trial has been registered, e.g. 'ClinicalTrials.gov' or 'EU-CTR'.",
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'string'
                },
                'researchers': {
                    'description':
                    'Dimensions researchers IDs associated to the clinical trial.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'researchers'
                },
                'title': {
                    'description': 'The title of the clinical trial.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': False,
                    'long_description': None,
                    'type': 'text'
                }
            },
            'fieldsets': ['all', 'basics', 'extras', 'categories'],
            'metrics': {
                'count': {
                    'description': 'Total count',
                    'name': 'count'
                }
            },
            'search_fields': [
                'title_abstract_only', 'investigators', 'full_data',
                'title_only'
            ]
        },
        'grants': {
            'fields': {
                'FOR': {
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , second level or 4 digit codes.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'FOR_first': {
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , first level or 2 digit codes.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'abstract': {
                    'description':
                    'Abstract or summary from a grant proposal.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': False,
                    'long_description': None,
                    'type': 'text'
                },
                'active_year': {
                    'description': 'List of active years for a grant.',
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'integer'
                },
                'category_bra': {
                    'description':
                    '`Broad Research Areas <https://app.dimensions.ai/browse/publication/broad_research_areas?redirect_path=/discover/publication>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hra': {
                    'description':
                    '`Health Research Areas <https://app.dimensions.ai/browse/publication/health_research_areas?redirect_path=/discover/publication>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hrcs_hc': {
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_ .',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hrcs_rac': {
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_ .',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_rcdc': {
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_ .',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'concepts': {
                    'description':
                    'Concepts describing the main topics of a grant (note: automatically derived from the grant text using machine learning).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    False,
                    'long_description':
                    None,
                    'type':
                    'text'
                },
                'date_inserted': {
                    'description':
                    'Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=`).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'timestamp'
                },
                'end_date': {
                    'description': 'Date when the grant ends.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'timestamp'
                },
                'funder_countries': {
                    'description':
                    'The country linked to the organisation funding the grant, expressed as GeoNames codes.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'countries'
                },
                'funders': {
                    'description':
                    'The organisation funding the grant. This is normally a GRID organisation, but in very few cases a Dimensions funder ID is used.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'orgs'
                },
                'funding_aud': {
                    'description': 'Funding amount awarded in AUD.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'financial'
                },
                'funding_cad': {
                    'description': 'Funding amount awarded in CAD.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'financial'
                },
                'funding_chf': {
                    'description': 'Funding amount awarded in CHF.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'financial'
                },
                'funding_currency': {
                    'description': 'Original funding currency.',
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'label'
                },
                'funding_eur': {
                    'description': 'Funding amount awarded in EUR.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'financial'
                },
                'funding_gbp': {
                    'description': 'Funding amount awarded in GBP.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'financial'
                },
                'funding_jpy': {
                    'description': 'Funding amount awarded in JPY.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'financial'
                },
                'funding_nzd': {
                    'description': 'Funding amount awarded in NZD.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'financial'
                },
                'funding_org_acronym': {
                    'description': 'Acronym for funding organisation.',
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'label'
                },
                'funding_org_city': {
                    'description': 'City name for funding organisation.',
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'label'
                },
                'funding_org_name': {
                    'description': 'Name of funding organisation.',
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'label'
                },
                'funding_usd': {
                    'description': 'Funding amount awarded in USD.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'financial'
                },
                'grant_number': {
                    'description':
                    'Grant identifier, as provided by the source (e.g., funder, aggregator) the grant was derived from.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'identifier'
                },
                'id': {
                    'description': 'Dimensions grant ID.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'identifier'
                },
                'investigator_details': {
                    'description':
                    "Additional details about investigators, including affiliations and roles e.g. 'PI' or 'Co-PI' (note: if the investigator has a Dimensions researcher ID, that is returned as well).",
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'json'
                },
                'language': {
                    'description':
                    'Grant original language, as ISO 639-1 language codes.',
                    'is_entity':
                    False,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'label'
                },
                'linkout': {
                    'description': 'Original URL for the grant.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': False,
                    'long_description': None,
                    'type': 'text'
                },
                'original_title': {
                    'description':
                    'Title of the grant in its original language.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': False,
                    'long_description': None,
                    'type': 'text'
                },
                'research_org_cities': {
                    'description':
                    'City of the research organisations receiving the grant, expressed as GeoNames id and name.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'cities'
                },
                'research_org_countries': {
                    'description':
                    'Country of the research organisations receiving the grant, expressed as GeoNames code and name.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'countries'
                },
                'research_org_state_codes': {
                    'description':
                    'State of the GRID organisations receiving the grant, expressed as GeoNames codes (ISO\u200c-3166-2).',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'states'
                },
                'research_orgs': {
                    'description':
                    'GRID organisations receiving the grant (note: identifiers are automatically extracted from the source text and can be missing in some cases).',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'orgs'
                },
                'researchers': {
                    'description':
                    'Dimensions researchers IDs associated to the grant.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'researchers'
                },
                'start_date': {
                    'description':
                    "Date when the grant starts, in the format 'YYYY-MM-DD'.",
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'timestamp'
                },
                'start_year': {
                    'description': 'Year when the grant starts.',
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'integer'
                },
                'title': {
                    'description':
                    'Title of the grant in English (if the grant language is not English, this field contains a translation of the title).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    False,
                    'long_description':
                    None,
                    'type':
                    'text'
                },
                'title_language': {
                    'description':
                    'ISO 639-1 language code for the original grant title.',
                    'is_entity':
                    False,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'label'
                }
            },
            'fieldsets': ['all', 'basics', 'extras', 'categories'],
            'metrics': {
                'count': {
                    'description': 'Total count',
                    'name': 'count'
                },
                'funding': {
                    'description': 'Total funding amount, in USD.',
                    'name': 'funding'
                }
            },
            'search_fields': [
                'title_abstract_only', 'title_only', 'noun_phrases',
                'concepts', 'investigators', 'full_data'
            ]
        },
        'patents': {
            'fields': {
                'FOR': {
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , second level or 4 digit codes.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'FOR_first': {
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , first level or 2 digit codes.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'abstract': {
                    'description': 'Abstract or description of the patent.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': False,
                    'long_description': None,
                    'type': 'text'
                },
                'additional_filters': {
                    'description':
                    "Additional filters describing the patents, e.g. whether it's about a 'Research Organisation', or it is part of the 'Orange Book'.",
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'string'
                },
                'assignee_cities': {
                    'description':
                    'City of the GRID assignees of the patent, expressed as GeoNames ID and name.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'cities'
                },
                'assignee_countries': {
                    'description':
                    'Country of the GRID assignees of the patent, expressed as GeoNames code and name.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'countries'
                },
                'assignee_names': {
                    'description': 'Name of the GRID assignees of the patent.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'string'
                },
                'assignee_state_codes': {
                    'description':
                    'State of the GRID assignee, expressed using GeoNames (ISO\u200c-3166-2) codes.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'states'
                },
                'assignee_state_names': {
                    'description': 'State name of GRID assignee, as a string.',
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'label'
                },
                'assignees': {
                    'description':
                    'GRID organisations who own or have owned the rights of a patent (note: this is a combination of `current_assignees` and `original_assigness` fields).',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'orgs'
                },
                'associated_grant_ids': {
                    'description':
                    'Dimensions IDs of the grants associated to the patent (see also: :ref:`data-model` section).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'identifier'
                },
                'category_bra': {
                    'description':
                    '`Broad Research Areas <https://app.dimensions.ai/browse/publication/broad_research_areas?redirect_path=/discover/publication>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hra': {
                    'description':
                    '`Health Research Areas <https://app.dimensions.ai/browse/publication/health_research_areas?redirect_path=/discover/publication>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hrcs_hc': {
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hrcs_rac': {
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_rcdc': {
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'cited_by_ids': {
                    'description':
                    'Dimensions IDs of the patents that cite this patent (see also: :ref:`data-model` section).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'identifier'
                },
                'cpc': {
                    'description':
                    '`Cooperative Patent Classification Categorization <https://www.epo.org/searching-for-patents/helpful-resources/first-time-here/classification/cpc.html>`_.',
                    'is_entity':
                    False,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'label'
                },
                'current_assignee_names': {
                    'description':
                    'Names of the GRID organisations currently holding the patent.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'string'
                },
                'current_assignees': {
                    'description':
                    'GRID organisations currenlty owning the patent.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'orgs'
                },
                'date': {
                    'description': 'Date when the patent was filed.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'timestamp'
                },
                'date_inserted': {
                    'description':
                    'Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=`).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'timestamp'
                },
                'expiration_date': {
                    'description': 'Date when the patent expires.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'timestamp'
                },
                'filing_status': {
                    'description':
                    "Filing Status of the patent e.g. 'Application' or 'Grant'.",
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'string'
                },
                'funder_groups': {
                    'description':
                    'Organisation group the GRID patent funder belongs to.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'org_groups'
                },
                'funders': {
                    'description': 'GRID organisations funding the patent.',
                    'is_entity': True,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'orgs'
                },
                'granted_date': {
                    'description':
                    'The date on which the official body grants the patent.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'timestamp'
                },
                'granted_year': {
                    'description':
                    'The year on which the official body grants the patent.',
                    'is_entity':
                    False,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'integer'
                },
                'id': {
                    'description': 'Dimensions patent ID',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'identifier'
                },
                'inventor_names': {
                    'description':
                    'Names of the people who invented the patent.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'string'
                },
                'ipcr': {
                    'description':
                    '`International Patent Classification Reform Categorization <https://www.wipo.int/classifications/ipc/en/faq/>`_.',
                    'is_entity':
                    False,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'label'
                },
                'jurisdiction': {
                    'description':
                    "The jurisdiction where the patent was granted, e.g. 'US', 'DE', 'EP'...",
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'string'
                },
                'legal_status': {
                    'description':
                    "The legal status of the patent, e.g. 'Granted', 'Active', 'Abandoned' etc..",
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'string'
                },
                'original_assignee_names': {
                    'description':
                    'Name of the GRID organisation that first owned the patent.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'string'
                },
                'original_assignees': {
                    'description':
                    'GRID organisations that first owned the patent.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'orgs'
                },
                'priority_date': {
                    'description':
                    'The earliest filing date in a family of patent applications.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'timestamp'
                },
                'priority_year': {
                    'description':
                    'The filing year of the earliest application of which priority is claimed.',
                    'is_entity':
                    False,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'integer'
                },
                'publication_date': {
                    'description': 'Date of publication of a patent.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'timestamp'
                },
                'publication_ids': {
                    'description':
                    'Dimensions IDs of the publications related to this patent (see also: :ref:`data-model` section).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'identifier'
                },
                'publication_year': {
                    'description': 'Year of publication of a patent.',
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'integer'
                },
                'reference_ids': {
                    'description':
                    'Dimensions IDs of the patents which are cited by this patent (see also: :ref:`data-model` section).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'identifier'
                },
                'times_cited': {
                    'description':
                    'The number of times the patent has been cited by other patents.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'count'
                },
                'title': {
                    'description': 'The title of the patent.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': False,
                    'long_description': None,
                    'type': 'text'
                },
                'year': {
                    'description': 'The year the patent was filed.',
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'integer'
                }
            },
            'fieldsets': ['all', 'basics', 'extras', 'categories'],
            'metrics': {
                'count': {
                    'description': 'Total count',
                    'name': 'count'
                }
            },
            'search_fields':
            ['title_abstract_only', 'full_data', 'inventors', 'title_only']
        },
        'policy_documents': {
            'fields': {
                'FOR': {
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , second level or 4 digit codes.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'FOR_first': {
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_ , first level or 2 digit codes.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_bra': {
                    'description':
                    '`Broad Research Areas <https://app.dimensions.ai/browse/publication/broad_research_areas?redirect_path=/discover/publication>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hra': {
                    'description':
                    '`Health Research Areas <https://app.dimensions.ai/browse/publication/health_research_areas?redirect_path=/discover/publication>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hrcs_hc': {
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hrcs_rac': {
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_rcdc': {
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'date_inserted': {
                    'description':
                    'Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=`).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'date'
                },
                'id': {
                    'description': 'Dimensions policy document ID',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'identifier'
                },
                'linkout': {
                    'description': 'Original URL for the policy document.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': False,
                    'long_description': None,
                    'type': 'text'
                },
                'publication_ids': {
                    'description':
                    'Dimensions IDs of the publications related to this policy document (see also: :ref:`data-model` section).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'identifier'
                },
                'publisher_org': {
                    'description':
                    'GRID organization publishing the policy document.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'orgs'
                },
                'publisher_org_city': {
                    'description':
                    'City of the GRID organization publishing the policy document.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'cities'
                },
                'publisher_org_country': {
                    'description':
                    'Country of the GRID organization publishing the policy document.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'countries'
                },
                'publisher_org_state': {
                    'description':
                    'State of the GRID organization publishing the policy document.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'states'
                },
                'title': {
                    'description': 'Title of the policy document.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'string'
                },
                'year': {
                    'description':
                    'Year of publication of the policy document.',
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'integer'
                }
            },
            'fieldsets': ['all', 'basics', 'categories'],
            'metrics': {
                'count': {
                    'description': 'Total count',
                    'name': 'count'
                }
            },
            'search_fields': ['full_data', 'title_only']
        },
        'publications': {
            'fields': {
                'altmetric': {
                    'description': 'Altmetric attention score.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'float'
                },
                'altmetric_id': {
                    'description': 'AltMetric Publication ID',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'integer'
                },
                'authors': {
                    'description':
                    'Ordered list of authors names and their affiliations, as they appear in the original publication. The list can include researcher and organization identifiers, when available (note: in order to search for disambiguated authors, use the `in researchers` syntax).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'json'
                },
                'book_doi': {
                    'description':
                    'The DOI of the book a chapter belongs to (note: this field is available only for chapters).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'identifier'
                },
                'book_series_title': {
                    'description':
                    'The title of the book series book, belong to.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    False,
                    'long_description':
                    None,
                    'type':
                    'text'
                },
                'book_title': {
                    'description':
                    'The title of the book a chapter belongs to (note: this field is available only for chapters).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    False,
                    'long_description':
                    None,
                    'type':
                    'text'
                },
                'category_bra': {
                    'description':
                    '`Broad Research Areas <https://app.dimensions.ai/browse/publication/broad_research_areas?redirect_path=/discover/publication>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_for': {
                    'description':
                    '`ANZSRC Fields of Research classification <https://app.dimensions.ai/browse/publication/for>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hra': {
                    'description':
                    '`Health Research Areas <https://app.dimensions.ai/browse/publication/health_research_areas?redirect_path=/discover/publication>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hrcs_hc': {
                    'description':
                    '`HRCS - Health Categories <https://app.dimensions.ai/browse/publication/hrcs_hc>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_hrcs_rac': {
                    'description':
                    '`HRCS – Research Activity Codes <https://app.dimensions.ai/browse/publication/hrcs_rac>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'category_rcdc': {
                    'description':
                    '`Research, Condition, and Disease Categorization <https://app.dimensions.ai/browse/publication/rcdc>`_',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'categories'
                },
                'concepts': {
                    'description':
                    'Concepts describing the main topics of a publication (note: automatically derived from the publication text using machine learning).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    False,
                    'long_description':
                    None,
                    'type':
                    'text'
                },
                'date': {
                    'description':
                    'The publication date of a document, eg "2018-01-01" (note: dates can sometimes be incomplete and include only the month or the year).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'date'
                },
                'date_inserted': {
                    'description':
                    "Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=').",
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'timestamp'
                },
                'doi': {
                    'description': 'Digital object identifier.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'identifier'
                },
                'field_citation_ratio': {
                    'description':
                    'Relative citation performance of article when compared to similarly aged articles in its area of research (note: does not support emptiness filters).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'float'
                },
                'funder_countries': {
                    'description':
                    'The country of the GRID organisation funding this publication.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'countries'
                },
                'funders': {
                    'description':
                    'The GRID organisation funding this publication.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'orgs'
                },
                'id': {
                    'description': 'Dimensions publication ID.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'identifier'
                },
                'issn': {
                    'description': 'International Standard Serial Number',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'string'
                },
                'issue': {
                    'description': 'The issue number of a publication.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'string'
                },
                'journal': {
                    'description': 'The journal a publication belongs to.',
                    'is_entity': True,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'journals'
                },
                'journal_lists': {
                    'description':
                    "Independent grouping of journals outside of Dimensions, e.g. 'ERA 2015' or 'Norwegian register level 1'.",
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'string'
                },
                'linkout': {
                    'description': 'Original URL for a publication full text.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': False,
                    'long_description': None,
                    'type': 'text'
                },
                'mesh_terms': {
                    'description':
                    'Medical Subject Heading terms as used in PubMed.',
                    'is_entity':
                    False,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'label'
                },
                'open_access_categories': {
                    'description':
                    'Open Access categories for publications. See below for more examples.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    'Open Access category data for publications values:\n\n        * `oa_all`: Article is freely available\n        * `gold_pure`: Version Of Record (VOR) is free under an open licence from a full OA journal\n        * `gold_hybrid`: Version Of Record (VOR) is free under an open licence in a paid-access journal\n        * `gold_bronze`: Freely available on publisher page, but without an open licence\n        * `green_pub`: Free copy of published version in an OA repository\n        * `green_acc`: Free copy of accepted version in an OA repository\n        * `green_sub`: Free copy of submitted version, or where version is unknown, in an OA repository\n        * `closed`: No freely available copy has been identified',
                    'type':
                    'open_access'
                },
                'pages': {
                    'description':
                    'The pages of the publication, as they would appear in a citation record.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'string'
                },
                'pmcid': {
                    'description': 'PubMed Central ID.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'identifier'
                },
                'pmid': {
                    'description': 'PubMed ID.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'identifier'
                },
                'proceedings_title': {
                    'description':
                    'Title of the conference proceedings volume associated to a publication.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    False,
                    'long_description':
                    None,
                    'type':
                    'text'
                },
                'publisher': {
                    'description': 'Name of the publisher as a string.',
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'label'
                },
                'recent_citations': {
                    'description':
                    'Number of citations received in the last two years. Does not support emptiness filters',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'integer'
                },
                'reference_ids': {
                    'description':
                    'Dimensions publication ID for publications in the references list, i.e. outgoing citations (see also: :ref:`data-model` section).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'identifier'
                },
                'relative_citation_ratio': {
                    'description':
                    'Relative citation performance of an article when compared to others in its area of research (note: does not support emptiness filters).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'float'
                },
                'research_org_cities': {
                    'description':
                    'City of the GRID organisations authors are affiliated to, expressed as GeoNames ID and name.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'cities'
                },
                'research_org_countries': {
                    'description':
                    'Country of the GRID organisations authors are affiliated to, identified using GeoNames codes (note: this field supports :ref:`filter-functions`: ``count``).',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'countries'
                },
                'research_org_country_names': {
                    'description':
                    'Country name of the GRID organisations authors are affiliated to, as a string.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'string'
                },
                'research_org_state_codes': {
                    'description':
                    'State of the GRID organisations authors are affiliated to, expressed as GeoNames codes (ISO\u200c-3166-2).',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'states'
                },
                'research_org_state_names': {
                    'description':
                    'State name of the GRID organisations authors are affiliated to, as a string.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'string'
                },
                'research_orgs': {
                    'description':
                    'GRID organisations associated to a publication. Identifiers are automatically extracted from author affiliations text, so they can be missing in some cases (note: this field supports :ref:`filter-functions`: ``count``).',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'orgs'
                },
                'researchers': {
                    'description':
                    "Researcher IDs matched to the publication's authors list. (note: this returns only the disambiguated authors of a publication; in order to get the full authors list, the field `author_affiliations` should be used). This field supports :ref:`filter-functions`: ``count``.",
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'researchers'
                },
                'supporting_grant_ids': {
                    'description':
                    'Grants supporting a publication, returned as a list of dimensions grants IDs  (see also: :ref:`data-model` section).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'identifier'
                },
                'times_cited': {
                    'description':
                    'Number of citations (note: does not support emptiness filters).',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'count'
                },
                'title': {
                    'description': 'Title of a publication.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': False,
                    'long_description': None,
                    'type': 'text'
                },
                'type': {
                    'description':
                    'Publication type (one of: article, chapter, proceeding, monograph, preprint or book).',
                    'is_entity':
                    False,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'label'
                },
                'volume': {
                    'description': 'Publication volume.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'string'
                },
                'year': {
                    'description':
                    'The year of publication (note: when the `date` field is available, this is equal to the year part of the full date).',
                    'is_entity':
                    False,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'integer'
                }
            },
            'fieldsets': ['all', 'basics', 'extras', 'book', 'categories'],
            'metrics': {
                'altmetric_avg': {
                    'description': 'Altmetric attention score mean',
                    'name': 'altmetric_avg'
                },
                'altmetric_median': {
                    'description': 'Median Altmetric attention score',
                    'name': 'altmetric_median'
                },
                'citations_avg': {
                    'description': 'Arithmetic mean of citations',
                    'name': 'citations_avg'
                },
                'citations_median': {
                    'description': 'Median of citations',
                    'name': 'citations_median'
                },
                'citations_total': {
                    'description': 'Aggregated number of citations',
                    'name': 'citations_total'
                },
                'count': {
                    'description': 'Total count',
                    'name': 'count'
                },
                'fcr_gavg': {
                    'description':
                    'Geometric mean of `field_citation_ratio` field (note: This field cannot be used for sorting results).',
                    'name':
                    'fcr_gavg'
                },
                'rcr_avg': {
                    'description':
                    'Arithmetic mean of `relative_citation_ratio` field.',
                    'name':
                    'rcr_avg'
                },
                'recent_citations_total': {
                    'description':
                    'For a given article, in a given year, the number of citations accrued in the last two year period. Single value stored per document, year window rolls over in July.',
                    'name':
                    'recent_citations_total'
                }
            },
            'search_fields': [
                'full_data_exact', 'title_abstract_only', 'title_only',
                'authors', 'concepts', 'full_data'
            ]
        },
        'researchers': {
            'fields': {
                'current_research_org': {
                    'description':
                    'The most recent research organization linked to the researcher.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'orgs'
                },
                'first_grant_year': {
                    'description':
                    'First year the researcher was awarded a grant.',
                    'is_entity':
                    False,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'integer'
                },
                'first_name': {
                    'description': 'First Name.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'string'
                },
                'first_publication_year': {
                    'description': None,
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'integer'
                },
                'id': {
                    'description': 'Dimensions researcher ID.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'identifier'
                },
                'last_grant_year': {
                    'description':
                    'Last year the researcher was awarded a grant.',
                    'is_entity':
                    False,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'integer'
                },
                'last_name': {
                    'description': 'Last Name.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'string'
                },
                'last_publication_year': {
                    'description': None,
                    'is_entity': False,
                    'is_facet': True,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'integer'
                },
                'obsolete': {
                    'description':
                    'Indicates researcher ID status. 0 means that the researcher ID is still active, 1 means that the researcher ID is no longer valid. See the `redirect` field for further information on invalid researcher IDs.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'integer'
                },
                'orcid_id': {
                    'description': '`ORCID <https://orcid.org/>`_ ID.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'string'
                },
                'redirect': {
                    'description':
                    'Indicates status of a researcher ID marked as obsolete. Empty means that the researcher ID was deleted. Otherwise ID provided means that is the new ID into which the obsolete one was redirected. If multiple values are available, it means that the original researcher ID was split into multiple IDs.',
                    'is_entity':
                    False,
                    'is_facet':
                    False,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'identifier'
                },
                'research_orgs': {
                    'description':
                    'All research organizations linked to the researcher.',
                    'is_entity':
                    True,
                    'is_facet':
                    True,
                    'is_filter':
                    True,
                    'long_description':
                    None,
                    'type':
                    'orgs'
                },
                'total_grants': {
                    'description': 'Total grants count.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'count'
                },
                'total_publications': {
                    'description': 'Total publications count.',
                    'is_entity': False,
                    'is_facet': False,
                    'is_filter': True,
                    'long_description': None,
                    'type': 'count'
                }
            },
            'fieldsets': ['all', 'basics', 'extras'],
            'metrics': {
                'count': {
                    'description': 'Total count',
                    'name': 'count'
                }
            },
            'search_fields': ['researcher']
        }
    }
}
