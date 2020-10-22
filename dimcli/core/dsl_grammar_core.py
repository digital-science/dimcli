#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# GRAMMAR_DICT is a dictionary rendering of the DSL grammar JSON
# which can be obtained with the query `describe schema`
#
# how to create:
#
# ./tools/run-extract-grammar.sh
#
# then copy contents of `dsl_grammar_language_NEW.py` to this file (after formatting them)
#
#
# 
# 

GRAMMAR_DICT = {
    'sources': {
        'publications': {
            'fields': {
                'category_for': {
                    'type': 'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'research_org_countries': {
                    'type': 'countries',
                    'description':
                    'Country of the organisations authors are affiliated to, identified using GeoNames codes (note: this field supports :ref:`filter-functions`: ``count``).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'date': {
                    'type': 'date',
                    'description':
                    'The publication date of a document, eg "2018-01-01" (note: dates can sometimes be incomplete and include only the month or the year).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'recent_citations': {
                    'type': 'integer',
                    'description':
                    'Number of citations received in the last two years. Does not support emptiness filters',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'volume': {
                    'type': 'string',
                    'description': 'Publication volume.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'book_doi': {
                    'type': 'string',
                    'description':
                    'The DOI of the book a chapter belongs to (note: this field is available only for chapters).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'altmetric_id': {
                    'type': 'integer',
                    'description': 'AltMetric Publication ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'pmcid': {
                    'type': 'string',
                    'description': 'PubMed Central ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'book_series_title': {
                    'type': 'string',
                    'description':
                    'The title of the book series book, belong to.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_icrp_cso': {
                    'type': 'categories',
                    'description':
                    '`ICRP Common Scientific Outline <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'linkout': {
                    'type': 'string',
                    'description': 'Original URL for a publication full text.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'date_inserted': {
                    'type': 'date',
                    'description':
                    "Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=').",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'concepts': {
                    'type': 'json',
                    'description':
                    'Concepts describing the main topics of a publication (note: automatically derived from the publication text using machine learning).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'dimensions_url': {
                    'type': 'string',
                    'description':
                    'Link pointing to the Dimensions web application',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'id': {
                    'type': 'string',
                    'description': 'Dimensions publication ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_hrcs_rac': {
                    'type': 'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_hra': {
                    'type': 'categories',
                    'description':
                    '`Health Research Areas <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'resulting_publication_doi': {
                    'type': 'string',
                    'description':
                    'For preprints, the DOIs of the resulting full publications.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'pmid': {
                    'type': 'string',
                    'description': 'PubMed ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'referenced_pubs': {
                    'type': 'publication_links',
                    'description':
                    'Publication IDs of the publications in the references list, i.e. outgoing citations.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'publisher': {
                    'type': 'string',
                    'description': 'Name of the publisher as a string.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'researchers': {
                    'type': 'researchers',
                    'description':
                    "Researcher IDs matched to the publication's authors list. (note: this returns only the disambiguated authors of a publication; in order to get the full authors list, the field `authors` should be used). This field supports :ref:`filter-functions`: ``count``.",
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'doi': {
                    'type': 'string',
                    'description': 'Digital object identifier.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'funders': {
                    'type': 'organizations',
                    'description':
                    'The GRID organisation funding this publication.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'research_org_country_names': {
                    'type': 'string',
                    'description':
                    'Country name of the organisations authors are affiliated to, as a string.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'abstract': {
                    'type': 'string',
                    'description': 'The publication abstract.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'pages': {
                    'type': 'string',
                    'description':
                    'The pages of the publication, as they would appear in a citation record.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'supporting_grant_ids': {
                    'type': 'string',
                    'description':
                    'Grants supporting a publication, returned as a list of dimensions grants IDs  (see also: :ref:`publications_model` section).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'research_org_cities': {
                    'type': 'cities',
                    'description':
                    'City of the organisations authors are affiliated to, expressed as GeoNames ID and name.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'book_title': {
                    'type': 'string',
                    'description':
                    'The title of the book a chapter belongs to (note: this field is available only for chapters).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'relative_citation_ratio': {
                    'type': 'float',
                    'description':
                    'Relative citation performance of an article when compared to others in its area of research (note: does not support emptiness filters).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'concepts_scores': {
                    'type': 'json',
                    'description': 'Relevancy scores for `concepts`.',
                    'long_description':
                    'Returned objects contain: ``concept``, ``relevance``.\n                                            \n                                            For example:\n                                            \n    .. code-block:: json\n    \n        {\n            "concepts_scores": [\n                {\n                  "concept": "professional relations",\n                  "relevance": 0.08789352253426701\n                },\n                {\n                  "concept": "relation",\n                  "relevance": 0.062333122509877006\n                },\n                {\n                  "concept": "representation",\n                  "relevance": 0.025851134800039\n                },\n                {\n                  "concept": "skald",\n                  "relevance": 6.984149644517923e-05\n                },\n                {\n                  "concept": "Representations of Skalds",\n                  "relevance": 0.0\n                },\n                {\n                  "concept": "Sagas 1",\n                  "relevance": 0.0\n                }\n            ]\n        }',
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'clinical_trial_ids': {
                    'type': 'string',
                    'description':
                    'Clinical Trial IDs mentioned in publications full text.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'category_sdg': {
                    'type': 'categories',
                    'description': 'SDG - Sustainable Development Goals',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'research_org_state_codes': {
                    'type': 'states',
                    'description':
                    'State of the organisations authors are affiliated to, expressed as GeoNames codes (ISO\u200c-3166-2).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'research_org_names': {
                    'type': 'string',
                    'description':
                    'Names of organizations authors are affiliated to.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'field_citation_ratio': {
                    'type': 'float',
                    'description':
                    'Relative citation performance of article when compared to similarly aged articles in its area of research (note: does not support emptiness filters).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'journal_lists': {
                    'type': 'string',
                    'description':
                    "Independent grouping of journals outside of Dimensions, e.g. 'ERA 2015' or 'Norwegian register level 1'.",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'title': {
                    'type': 'string',
                    'description': 'Title of a publication.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'issue': {
                    'type': 'string',
                    'description': 'The issue number of a publication.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'research_orgs': {
                    'type': 'organizations',
                    'description':
                    'GRID organisations associated to a publication. Identifiers are automatically extracted from author affiliations text, so they can be missing in some cases (note: this field supports :ref:`filter-functions`: ``count``).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_bra': {
                    'type': 'categories',
                    'description':
                    '`Broad Research Areas <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'funder_countries': {
                    'type': 'countries',
                    'description':
                    'The country of the organisations funding this publication.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'authors': {
                    'type': 'json',
                    'description':
                    'Ordered list of authors names and their affiliations, as they appear in the original publication. The list can include researcher and organization identifiers, when available (note: in order to search for disambiguated authors, use the `in researchers` syntax).',
                    'long_description':
                    'Returned objects contain: ``first_name``, ``last_name``, ``corresponding``, ``orcid``, ``current_organization_id``, ``researcher_id``, ``affiliations`` and ``raw_affiliation``.\n\n        For example:\n        \n        .. code-block:: json\n        \n                {\n                    "raw_affiliation": [\n                        "Centre for Operational Research, International Union Against Tuberculosis and Lung Disease (The Union), Paris, France.",\n                        "Centre for Operational Research, The Union South-East Asia Office, New Delhi, India."\n                    ],\n                    "first_name": "Pruthu",\n                    "last_name": "Thekkur",\n                    "corresponding": "",\n                    "orcid": "[\'s\']",\n                    "current_organization_id": "grid.435357.3",\n                    "researcher_id": "ur.0670077515.38",\n                    "affiliations": [\n                        {\n                            "raw_affiliation": "Centre for Operational Research, International Union Against Tuberculosis and Lung Disease (The Union), Paris, France.",\n                            "id": "grid.435357.3",\n                            "name": "International Union Against Tuberculosis and Lung Disease",\n                            "city": "Paris",\n                            "city_id": 2988507,\n                            "country": "France",\n                            "country_code": "FR",\n                            "state": null,\n                            "state_code": null\n                        },\n                        {\n                            "raw_affiliation": "Centre for Operational Research, The Union South-East Asia Office, New Delhi, India.",\n                            "id": "grid.8195.5",\n                            "name": "University of Delhi",\n                            "city": "New Delhi",\n                            "city_id": 1261481,\n                            "country": "India",\n                            "country_code": "IN",\n                            "state": null,\n                            "state_code": null\n                        }\n                    ]\n                }',
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'issn': {
                    'type': 'string',
                    'description': 'International Standard Serial Number',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'category_icrp_ct': {
                    'type': 'categories',
                    'description':
                    '`ICRP Cancer Types <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'open_access_categories': {
                    'type': 'open_access',
                    'description':
                    'Open Access categories for publications. See below for more examples.',
                    'long_description':
                    'Open Access category data for publications values:\n\n        * `oa_all`: Article is freely available\n        * `gold_pure`: Version Of Record (VOR) is free under an open licence from a full OA journal\n        * `gold_hybrid`: Version Of Record (VOR) is free under an open licence in a paid-access journal\n        * `gold_bronze`: Freely available on publisher page, but without an open licence\n        * `green_pub`: Free copy of published version in an OA repository\n        * `green_acc`: Free copy of accepted version in an OA repository\n        * `green_sub`: Free copy of submitted version, or where version is unknown, in an OA repository\n        * `closed`: No freely available copy has been identified',
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'journal': {
                    'type': 'journals',
                    'description': 'The journal a publication belongs to.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'reference_ids': {
                    'type': 'string',
                    'description':
                    'Dimensions publication ID for publications in the references list, i.e. outgoing citations (see also: :ref:`publications_model` section).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'category_uoa': {
                    'type': 'categories',
                    'description':
                    '`Units of Assessment <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'proceedings_title': {
                    'type': 'string',
                    'description':
                    'Title of the conference proceedings volume associated to a publication.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'acknowledgements': {
                    'type': 'string',
                    'description':
                    'The acknowledgements section text as found in the source document.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'type': {
                    'type': 'string',
                    'description':
                    'Publication type (one of: article, chapter, proceeding, monograph, preprint or book).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'altmetric': {
                    'type': 'float',
                    'description': 'Altmetric attention score.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_rcdc': {
                    'type': 'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'research_org_state_names': {
                    'type': 'string',
                    'description':
                    'State name of the organisations authors are affiliated to, as a string.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'year': {
                    'type': 'integer',
                    'description':
                    'The year of publication (note: when the `date` field is available, this is equal to the year part of the full date).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'category_hrcs_hc': {
                    'type': 'categories',
                    'description':
                    '`HRCS - Health Categories <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'times_cited': {
                    'type': 'integer',
                    'description':
                    'Number of citations (note: does not support emptiness filters).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'mesh_terms': {
                    'type': 'string',
                    'description':
                    'Medical Subject Heading terms as used in PubMed.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
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
                'authors', 'full_data', 'title_abstract_only',
                'full_data_exact', 'concepts', 'title_only'
            ]
        },
        'grants': {
            'fields': {
                'research_org_countries': {
                    'type': 'countries',
                    'description':
                    'Country of the research organisations receiving the grant, expressed as GeoNames code and name.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_for': {
                    'type': 'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'funding_org_acronym': {
                    'type': 'string',
                    'description': 'Acronym for funding organisation.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'original_title': {
                    'type': 'string',
                    'description':
                    'Title of the grant in its original language.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'investigator_details': {
                    'type': 'json',
                    'description':
                    "Additional details about investigators, including affiliations and roles e.g. 'PI' or 'Co-PI' (note: if the investigator has a Dimensions researcher ID, that is returned as well).",
                    'long_description':
                    'Returned objects contain: ``id``, ``first_name``, ``middle_name``, ``last_name``, ``role``, ``affiliations``\n                                           \n                                           For example:\n\n    .. code-block:: json\n\n        {\n            "investigator_details":[\n                {\n                    "id":"ur.012516501745.79",\n                    "first_name":"O.",\n                    "middle_name":"",\n                    "last_name":"Mitas",\n                    "role":"PI",\n                    "affiliations":[\n                        {\n                            "id":"grid.5477.1",\n                            "name":"Breda University of Applied Sciences",\n                            "city":null,\n                            "city_id":"2745912",\n                            "state":null,\n                            "state_code":null,\n                            "country":null,\n                            "country_code":"NL"\n                        }\n                    ]\n                }\n            ]\n        }',
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'funding_org_city': {
                    'type': 'string',
                    'description': 'City name for funding organisation.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'linkout': {
                    'type': 'string',
                    'description': 'Original URL for the grant.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_icrp_cso': {
                    'type': 'categories',
                    'description':
                    '`ICRP Common Scientific Outline <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'date_inserted': {
                    'type': 'date',
                    'description':
                    'Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=`).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'funding_cad': {
                    'type': 'float',
                    'description': 'Funding amount awarded in CAD.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'concepts': {
                    'type': 'json',
                    'description':
                    'Concepts describing the main topics of a publication (note: automatically derived from the publication text using machine learning).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'dimensions_url': {
                    'type': 'string',
                    'description':
                    'Link pointing to the Dimensions web application',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'id': {
                    'type': 'string',
                    'description': 'Dimensions grant ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_hrcs_rac': {
                    'type': 'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_ .',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_hra': {
                    'type': 'categories',
                    'description':
                    '`Health Research Areas <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'researchers': {
                    'type': 'researchers',
                    'description':
                    'Dimensions researchers IDs associated to the grant.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'abstract': {
                    'type': 'string',
                    'description':
                    'Abstract or summary from a grant proposal.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'grant_number': {
                    'type': 'string',
                    'description':
                    'Grant identifier, as provided by the source (e.g., funder, aggregator) the grant was derived from.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'research_org_cities': {
                    'type': 'cities',
                    'description':
                    'City of the research organisations receiving the grant, expressed as GeoNames id and name.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'concepts_scores': {
                    'type': 'json',
                    'description': 'Relevancy scores for `concepts`.',
                    'long_description':
                    'Returned objects contain: ``concept``, ``relevance``.\n                                            \n                                            For example:\n                                            \n    .. code-block:: json\n    \n        {\n            "concepts_scores": [\n                {\n                  "concept": "professional relations",\n                  "relevance": 0.08789352253426701\n                },\n                {\n                  "concept": "relation",\n                  "relevance": 0.062333122509877006\n                },\n                {\n                  "concept": "representation",\n                  "relevance": 0.025851134800039\n                },\n                {\n                  "concept": "skald",\n                  "relevance": 6.984149644517923e-05\n                },\n                {\n                  "concept": "Representations of Skalds",\n                  "relevance": 0.0\n                },\n                {\n                  "concept": "Sagas 1",\n                  "relevance": 0.0\n                }\n            ]\n        }',
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'foa_number': {
                    'type': 'string',
                    'description':
                    'The funding opportunity announcement (FOA) number, where available e.g. for grants from the US National Institute of Health (NIH) or from the National Science Foundation (NSF).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'funding_currency': {
                    'type': 'string',
                    'description': 'Original funding currency.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'research_org_state_codes': {
                    'type': 'states',
                    'description':
                    'State of the organisations receiving the grant, expressed as GeoNames codes (ISO\u200c-3166-2).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_sdg': {
                    'type': 'categories',
                    'description': 'SDG - Sustainable Development Goals',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'research_org_names': {
                    'type': 'string',
                    'description':
                    'Names of organizations investigators are affiliated to.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'active_year': {
                    'type': 'integer',
                    'description': 'List of active years for a grant.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'title': {
                    'type': 'string',
                    'description':
                    'Title of the grant in English (if the grant language is not English, this field contains a translation of the title).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'funding_org_name': {
                    'type': 'string',
                    'description': 'Name of funding organisation.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'end_date': {
                    'type': 'date',
                    'description': 'Date when the grant ends.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'research_orgs': {
                    'type': 'organizations',
                    'description':
                    'GRID organisations receiving the grant (note: identifiers are automatically extracted from the source text and can be missing in some cases).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_bra': {
                    'type': 'categories',
                    'description':
                    '`Broad Research Areas <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'funding_eur': {
                    'type': 'float',
                    'description': 'Funding amount awarded in EUR.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'language_title': {
                    'type': 'string',
                    'description':
                    'ISO 639-1 language code for the original grant title.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'start_date': {
                    'type': 'date',
                    'description':
                    "Date when the grant starts, in the format 'YYYY-MM-DD'.",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'funder_countries': {
                    'type': 'countries',
                    'description':
                    'The country linked to the organisation funding the grant, expressed as GeoNames codes.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'funding_jpy': {
                    'type': 'float',
                    'description': 'Funding amount awarded in JPY.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_icrp_ct': {
                    'type': 'categories',
                    'description':
                    '`ICRP Cancer Types <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'funding_aud': {
                    'type': 'float',
                    'description': 'Funding amount awarded in AUD.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'language': {
                    'type': 'string',
                    'description':
                    'Grant original language, as ISO 639-1 language codes.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'category_uoa': {
                    'type': 'categories',
                    'description':
                    '`Units of Assessment <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'start_year': {
                    'type': 'integer',
                    'description': 'Year when the grant starts.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'funding_usd': {
                    'type': 'float',
                    'description': 'Funding amount awarded in USD.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'funding_gbp': {
                    'type': 'float',
                    'description': 'Funding amount awarded in GBP.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_rcdc': {
                    'type': 'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_ .',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'funding_nzd': {
                    'type': 'float',
                    'description': 'Funding amount awarded in NZD.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_hrcs_hc': {
                    'type': 'categories',
                    'description':
                    '`HRCS - Health Categories <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_ .',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'funders': {
                    'type': 'organizations',
                    'description':
                    'The organisation funding the grant. This is normally a GRID organisation, but in very few cases a Dimensions funder ID is used.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'funding_chf': {
                    'type': 'float',
                    'description': 'Funding amount awarded in CHF.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
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
                'full_data', 'title_abstract_only', 'concepts',
                'investigators', 'title_only'
            ]
        },
        'patents': {
            'fields': {
                'original_assignees': {
                    'type': 'organizations',
                    'description':
                    'Disambiguated GRID organisations that first owned the patent.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_for': {
                    'type': 'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'date': {
                    'type': 'date',
                    'description': 'Date when the patent was filed.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'filing_status': {
                    'type': 'string',
                    'description':
                    "Filing Status of the patent e.g. 'Application' or 'Grant'.",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'expiration_date': {
                    'type': 'date',
                    'description': 'Date when the patent expires.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_icrp_cso': {
                    'type': 'categories',
                    'description':
                    '`ICRP Common Scientific Outline <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'date_inserted': {
                    'type': 'date',
                    'description':
                    'Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=`).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'cpc': {
                    'type': 'string',
                    'description':
                    '`Cooperative Patent Classification Categorization <https://www.epo.org/searching-for-patents/helpful-resources/first-time-here/classification/cpc.html>`_.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'inventor_names': {
                    'type': 'string',
                    'description':
                    'Names of the people who invented the patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'current_assignee_names': {
                    'type': 'string',
                    'description':
                    'Names of the organisations currently holding the patent, as they appear in the original document.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'dimensions_url': {
                    'type': 'string',
                    'description':
                    'Link pointing to the Dimensions web application',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'original_assignee_names': {
                    'type': 'string',
                    'description':
                    'Name of the organisations that first owned the patent, as they appear in the original document.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'id': {
                    'type': 'string',
                    'description': 'Dimensions patent ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_hrcs_rac': {
                    'type': 'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'current_assignees': {
                    'type': 'organizations',
                    'description':
                    'Disambiguated GRID organisations currenlty owning the patent.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'assignees': {
                    'type': 'organizations',
                    'description':
                    'Disambiguated GRID organisations who own or have owned the rights of a patent (note: this is a combination of `current_assignees` and `original_assignees` fields).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_hra': {
                    'type': 'categories',
                    'description':
                    '`Health Research Areas <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'researchers': {
                    'type': 'researchers',
                    'description':
                    "Researcher IDs matched to the patent's inventors list. (note: this returns only the disambiguated inventors of a patent; in order to get the full list of inventors, the field `inventors` should be used).",
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'granted_year': {
                    'type': 'integer',
                    'description':
                    'The year on which the official body grants the patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'ipcr': {
                    'type': 'string',
                    'description':
                    '`International Patent Classification Reform Categorization <https://www.wipo.int/classifications/ipc/en/faq/>`_.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'abstract': {
                    'type': 'string',
                    'description': 'Abstract or description of the patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'additional_filters': {
                    'type': 'string',
                    'description':
                    "Additional filters describing the patents, e.g. whether it's about a 'Research Organisation', or it is part of the 'Orange Book'.",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'priority_date': {
                    'type': 'date',
                    'description':
                    'The earliest filing date in a family of patent applications.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'granted_date': {
                    'type': 'date',
                    'description':
                    'The date on which the official body grants the patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'assignee_state_codes': {
                    'type': 'states',
                    'description':
                    'State of the assignee, expressed using GeoNames (ISO\u200c-3166-2) codes (note: this value is extracted independently from GRID).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'assignee_countries': {
                    'type': 'countries',
                    'description':
                    'Country of the assignees of the patent, expressed as GeoNames code and name (note: this value is extracted independently from GRID).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'publication_date': {
                    'type': 'date',
                    'description': 'Date of publication of a patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'title': {
                    'type': 'string',
                    'description': 'The title of the patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'associated_grant_ids': {
                    'type': 'string',
                    'description':
                    'Dimensions IDs of the grants associated to the patent (see also: :ref:`patents_model` section).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'publication_ids': {
                    'type': 'string',
                    'description':
                    'Dimensions IDs of the publications related to this patent (see also: :ref:`patents_model` section).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'category_bra': {
                    'type': 'categories',
                    'description':
                    '`Broad Research Areas <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'jurisdiction': {
                    'type': 'string',
                    'description':
                    "The jurisdiction where the patent was granted, e.g. 'US', 'DE', 'EP'...",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'funder_countries': {
                    'type': 'countries',
                    'description':
                    'The country of the funding organisation (note: currently this information is available only for US patents).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'publication_year': {
                    'type': 'integer',
                    'description': 'Year of publication of a patent.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'category_icrp_ct': {
                    'type': 'categories',
                    'description':
                    '`ICRP Cancer Types <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'cited_by_ids': {
                    'type': 'string',
                    'description':
                    'Dimensions IDs of the patents that cite this patent (see also: :ref:`patents_model` section).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'reference_ids': {
                    'type': 'string',
                    'description':
                    'Dimensions IDs of the patents which are cited by this patent (see also: :ref:`patents_model` section).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'publications': {
                    'type': 'publication_links',
                    'description':
                    'Publication IDs of the publications related to this patent (see also: :ref:`patents_model` section).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'legal_status': {
                    'type': 'string',
                    'description':
                    "The legal status of the patent, e.g. 'Granted', 'Active', 'Abandoned' etc..",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'priority_year': {
                    'type': 'integer',
                    'description':
                    'The filing year of the earliest application of which priority is claimed.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'category_rcdc': {
                    'type': 'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'year': {
                    'type': 'integer',
                    'description': 'The year the patent was filed.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'funders': {
                    'type': 'organizations',
                    'description': 'GRID organisations funding the patent.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_hrcs_hc': {
                    'type': 'categories',
                    'description':
                    '`HRCS - Health Categories <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'assignee_names': {
                    'type': 'string',
                    'description':
                    'Name of assignees of the patent, as they appear in the original document.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'times_cited': {
                    'type': 'integer',
                    'description':
                    'The number of times the patent has been cited by other patents.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'assignee_cities': {
                    'type': 'cities',
                    'description':
                    'City of the assignees of the patent, expressed as GeoNames ID and name (note: this value is extracted independently from GRID).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
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
                'category_for': {
                    'type': 'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'date': {
                    'type': 'date',
                    'description': 'Start date of a clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'investigator_details': {
                    'type': 'json',
                    'description':
                    'Additional details about investigators, including affiliations and roles.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'registry': {
                    'type': 'string',
                    'description':
                    "The platform where the clinical trial has been registered, e.g. 'ClinicalTrials.gov' or 'EU-CTR'.",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'active_years': {
                    'type': 'integer',
                    'description':
                    'List of active years for a clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'gender': {
                    'type': 'string',
                    'description':
                    "The gender of the clinical trial subjects e.g. 'Male', 'Female' or 'All'.",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'phase': {
                    'type': 'string',
                    'description': 'Phase of the clinical trial, as a string.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'linkout': {
                    'type': 'string',
                    'description': 'Original URL for the clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_icrp_cso': {
                    'type': 'categories',
                    'description':
                    '`ICRP Common Scientific Outline <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'date_inserted': {
                    'type': 'date',
                    'description':
                    "Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=').",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'dimensions_url': {
                    'type': 'string',
                    'description':
                    'Link pointing to the Dimensions web application',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'id': {
                    'type': 'string',
                    'description': 'Dimensions clinical trial ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_hrcs_rac': {
                    'type': 'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_hra': {
                    'type': 'categories',
                    'description':
                    '`Health Research Areas <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'researchers': {
                    'type': 'researchers',
                    'description':
                    'Dimensions researchers IDs associated to the clinical trial.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'abstract': {
                    'type': 'string',
                    'description':
                    'Abstract or description of the clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'conditions': {
                    'type': 'string',
                    'description':
                    "List of medical conditions names, e.g. 'Breast cancer' or 'Obesity'.",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'title': {
                    'type': 'string',
                    'description': 'The title of the clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'associated_grant_ids': {
                    'type': 'string',
                    'description':
                    'Dimensions IDs of the grants associated to the clinical trial (see also: :ref:`clinical_trials_model` section).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'publication_ids': {
                    'type': 'string',
                    'description':
                    'Publications IDs mentioned in clinical trials (excluding resulting publications).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'research_orgs': {
                    'type': 'organizations',
                    'description':
                    'GRID organizations involved, e.g. as sponsors or collaborators.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_bra': {
                    'type': 'categories',
                    'description':
                    '`Broad Research Areas <https://app.dimensions.ai/browse/publication/broad_research_areas?redirect_path=/discover/publication>`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'interventions': {
                    'type': 'json',
                    'description':
                    "Structured JSON object containing information about the clinical trial's interventions according to the research plan or protocol created by the investigators.",
                    'long_description':
                    'Returned objects contain: ``type``, ``name``, ``description``, ``arm_group_labels``, ``other_names``.\n                                            \n                                            For example:\n                                            \n    .. code-block:: json\n                                     \n        {\n            "interventions":[\n                {\n                    "type":"Drug",\n                    "name":"INCB024360",\n                    "description":"INCB024360: Oral daily dosing",\n                    "arm_group_labels":"MEDI4736 + INCB024360",\n                    "other_names":""\n                },\n                {\n                    "type":"Drug",\n                    "name":"MEDI4736",\n                    "description":"MEDI4736 administered intravenously (IV) every two weeks (q2w)",\n                    "arm_group_labels":"MEDI4736 + INCB024360",\n                    "other_names":""\n                }\n            ]\n        }',
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'funder_countries': {
                    'type': 'countries',
                    'description':
                    'The country group the funding organisations.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_icrp_ct': {
                    'type': 'categories',
                    'description':
                    '`ICRP Cancer Types <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'publications': {
                    'type': 'publication_links',
                    'description':
                    'Publication IDs of the publications mentioned in clinical trials (excluding resulting publications).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'brief_title': {
                    'type': 'string',
                    'description': 'Brief title of the clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_rcdc': {
                    'type': 'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'acronym': {
                    'type': 'string',
                    'description': 'Acronym of the clinical trial.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_hrcs_hc': {
                    'type': 'categories',
                    'description':
                    '`HRCS - Health Categories <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'funders': {
                    'type': 'organizations',
                    'description':
                    'GRID funding organisations that are involved with the clinical trial.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'mesh_terms': {
                    'type': 'string',
                    'description':
                    'Medical Subject Heading terms as used in PubMed.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
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
                    'type': 'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'publisher_org': {
                    'type': 'organizations',
                    'description':
                    'GRID organization publishing the policy document.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'linkout': {
                    'type': 'string',
                    'description': 'Original URL for the policy document.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'publisher_org_city': {
                    'type': 'cities',
                    'description':
                    'City of the organization publishing the policy document.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'category_icrp_cso': {
                    'type': 'categories',
                    'description':
                    '`ICRP Common Scientific Outline <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'date_inserted': {
                    'type': 'date',
                    'description':
                    'Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=`).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'dimensions_url': {
                    'type': 'string',
                    'description':
                    'Link pointing to the Dimensions web application',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'publisher_org_state': {
                    'type': 'states',
                    'description':
                    'State of the organization publishing the policy document.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'id': {
                    'type': 'string',
                    'description': 'Dimensions policy document ID',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_hrcs_rac': {
                    'type': 'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_hra': {
                    'type': 'categories',
                    'description':
                    '`Health Research Areas <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'title': {
                    'type': 'string',
                    'description': 'Title of the policy document.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'publisher_org_country': {
                    'type': 'countries',
                    'description':
                    'Country of the organization publishing the policy document.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'publication_ids': {
                    'type': 'string',
                    'description':
                    'Dimensions IDs of the publications related to this policy document (see also: :ref:`policy_documents_model` section).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'category_bra': {
                    'type': 'categories',
                    'description':
                    '`Broad Research Areas <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_icrp_ct': {
                    'type': 'categories',
                    'description':
                    '`ICRP Cancer Types <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'publications': {
                    'type': 'publication_links',
                    'description':
                    'Publication IDs of the publications related to this policy document (see also: :ref:`policy_documents_model` section).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_rcdc': {
                    'type': 'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'year': {
                    'type': 'integer',
                    'description':
                    'Year of publication of the policy document.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'category_hrcs_hc': {
                    'type': 'categories',
                    'description':
                    '`HRCS - Health Categories <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
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
                'last_grant_year': {
                    'type': 'integer',
                    'description':
                    'Last year the researcher was awarded a grant.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'last_name': {
                    'type': 'string',
                    'description': 'Last Name.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'obsolete': {
                    'type': 'integer',
                    'description':
                    'Indicates researcher ID status. 0 means that the researcher ID is still active, 1 means that the researcher ID is no longer valid. See the `redirect` field for further information on invalid researcher IDs.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'research_orgs': {
                    'type': 'organizations',
                    'description':
                    'All research organizations linked to the researcher.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'redirect': {
                    'type': 'string',
                    'description':
                    'Indicates status of a researcher ID marked as obsolete. Empty means that the researcher ID was deleted. Otherwise ID provided means that is the new ID into which the obsolete one was redirected. If multiple values are available, it means that the original researcher ID was split into multiple IDs.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'dimensions_url': {
                    'type': 'string',
                    'description':
                    'Link pointing to the Dimensions web application',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'total_publications': {
                    'type': 'integer',
                    'description': 'Total publications count.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'first_name': {
                    'type': 'string',
                    'description': 'First Name.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'total_grants': {
                    'type': 'integer',
                    'description': 'Total grants count.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'nih_ppid': {
                    'type': 'string',
                    'description':
                    'The PI Profile ID (i.e., ppid) is a Researcher ID from the US National Institute of Health (NIH).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'first_publication_year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'current_research_org': {
                    'type': 'organizations',
                    'description':
                    'The most recent research organization linked to the researcher.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'first_grant_year': {
                    'type': 'integer',
                    'description':
                    'First year the researcher was awarded a grant.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'orcid_id': {
                    'type': 'string',
                    'description': '`ORCID <https://orcid.org/>`_ ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'id': {
                    'type': 'string',
                    'description': 'Dimensions researcher ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'last_publication_year': {
                    'type': 'integer',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
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
                'longitude': {
                    'type': 'float',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'redirect': {
                    'type': 'string',
                    'description':
                    'GRID ID of an organization this one was redirected to',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'state_name': {
                    'type': 'string',
                    'description':
                    'GRID name of the organization country. E.g., "Maryland" for `grid.419635.c <https://grid.ac/institutes/grid.419635.c>`_',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'established': {
                    'type': 'integer',
                    'description':
                    'Year when the organization was estabilished',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'name': {
                    'type': 'string',
                    'description':
                    'GRID name of the organization. E.g., "University of Tokyo" for `grid.26999.3d <https://grid.ac/institutes/grid.26999.3d>`_',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'nuts_level1_name': {
                    'type': 'string',
                    'description':
                    'Level 1 name for this organization, based on `Nomenclature of Territorial Units for Statistics <https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics>`_ (NUTS) codes of the European Union.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'linkout': {
                    'type': 'string',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'dimensions_url': {
                    'type': 'string',
                    'description':
                    'Link pointing to the Dimensions web application',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'id': {
                    'type': 'string',
                    'description':
                    'GRID ID of the organization. E.g., "grid.26999.3d".',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'organization_related_ids': {
                    'type': 'string',
                    'description': 'Related organization IDs',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'nuts_level3_name': {
                    'type': 'string',
                    'description':
                    'Level 3 name for this organization, based on `Nomenclature of Territorial Units for Statistics <https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics>`_ (NUTS) codes of the European Union.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'orgref_ids': {
                    'type': 'string',
                    'description': 'OrgRef IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'hesa_ids': {
                    'type': 'string',
                    'description': 'HESA IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'cnrs_ids': {
                    'type': 'string',
                    'description': 'CNRS IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'nuts_level2_name': {
                    'type': 'string',
                    'description':
                    'Level 2 name for this organization, based on `Nomenclature of Territorial Units for Statistics <https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics>`_ (NUTS) codes of the European Union.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'nuts_level1_code': {
                    'type': 'string',
                    'description':
                    'Level 1 code for this organization, based on `Nomenclature of Territorial Units for Statistics <https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics>`_ (NUTS) codes of the European Union.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'status': {
                    'type': 'string',
                    'description':
                    'Status of an organization. May be be one of:\n        \n        * `a`: active organization\n        * `o`: obsolete organization\n        * `r`: redirected organization, see field `redirect` to obtain the GRID ID of an organization this one was redirected to',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'types': {
                    'type': 'string',
                    'description':
                    'Type of an organization. Available types include: ``Company``, ``Education``, ``Healthcare``, ``Nonprofit``, ``Facility``, ``Other``, ``Government``, ``Archive``, ``Education,Company``, ``Education,Facility``, ``Education,Healthcare``, ``Education,Other``, ``Archive,Nonprofit``. Furhter explanation is on the `GRID <https://www.grid.ac/pages/policies>`_ website.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'nuts_level3_code': {
                    'type': 'string',
                    'description':
                    'Level 3 code for this organization, based on `Nomenclature of Territorial Units for Statistics <https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics>`_ (NUTS) codes of the European Union.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'organization_parent_ids': {
                    'type': 'string',
                    'description': 'Parent organization IDs',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'external_ids_fundref': {
                    'type': 'string',
                    'description': 'Fundref IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'ror_ids': {
                    'type': 'string',
                    'description': 'ROR IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'latitude': {
                    'type': 'float',
                    'description': None,
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'wikipedia_url': {
                    'type': 'string',
                    'description': 'Wikipedia URL',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'wikidata_ids': {
                    'type': 'string',
                    'description': 'WikiData IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'country_name': {
                    'type': 'string',
                    'description':
                    'GRID name of the organization country. E.g., "Japan" for `grid.26999.3d <https://grid.ac/institutes/grid.26999.3d>`_',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'nuts_level2_code': {
                    'type': 'string',
                    'description':
                    'Level 2 code for this organization, based on `Nomenclature of Territorial Units for Statistics <https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics>`_ (NUTS) codes of the European Union.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'city_name': {
                    'type': 'string',
                    'description':
                    'GRID name of the organization country. E.g., "Bethesda" for `grid.419635.c <https://grid.ac/institutes/grid.419635.c>`_',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'organization_child_ids': {
                    'type': 'string',
                    'description': 'Child organization IDs',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'acronym': {
                    'type': 'string',
                    'description':
                    'GRID acronym of the organization. E.g., "UT" for `grid.26999.3d <https://grid.ac/institutes/grid.26999.3d>`_',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'ukprn_ids': {
                    'type': 'string',
                    'description': 'UKPRN IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'isni_ids': {
                    'type': 'string',
                    'description': 'ISNI IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'ucas_ids': {
                    'type': 'string',
                    'description': 'UCAS IDs for this organization',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
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
                'research_org_countries': {
                    'type': 'countries',
                    'description':
                    'Country of the organisations the publication authors are affiliated to, identified using GeoNames codes (note: this field supports count: count)..',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'description': {
                    'type': 'string',
                    'description': 'Description of the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'date': {
                    'type': 'date',
                    'description':
                    'The publication date of the dataset, eg "2018-01-01".',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_for': {
                    'type': 'categories',
                    'description':
                    '`ANZSRC Fields of Research classification <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_icrp_cso': {
                    'type': 'categories',
                    'description':
                    '`ICRP Common Scientific Outline <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'date_inserted': {
                    'type': 'date',
                    'description':
                    "Date when the record was inserted into Dimensions (note: this field does not support exact match on the data, only range filters e.g. `<=` or `>=').",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'dimensions_url': {
                    'type': 'string',
                    'description':
                    'Link pointing to the Dimensions web application',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'id': {
                    'type': 'string',
                    'description': 'Dimensions dataset ID.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'category_hrcs_rac': {
                    'type': 'categories',
                    'description':
                    '`HRCS – Research Activity Codes <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_hra': {
                    'type': 'categories',
                    'description':
                    '`Health Research Areas <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'researchers': {
                    'type': 'researchers',
                    'description':
                    "Dimensions researchers IDs associated to the dataset's associated publication. Note: in most cases, these would be the same as the dataset authors.",
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'doi': {
                    'type': 'string',
                    'description': 'Dataset DOI.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'research_org_cities': {
                    'type': 'cities',
                    'description':
                    'City of the organisations the publication authors are affiliated to, expressed as GeoNames ID and name.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_sdg': {
                    'type': 'categories',
                    'description': 'SDG - Sustainable Development Goals',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'date_created': {
                    'type': 'date',
                    'description': 'The creation date of the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'title': {
                    'type': 'string',
                    'description': 'Title of the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'repository_id': {
                    'type': 'string',
                    'description': 'The ID of the repository of the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'associated_grant_ids': {
                    'type': 'string',
                    'description':
                    'The Dimensions IDs of the grants linked to the publication the dataset is associated with.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'associated_publication_id': {
                    'type': 'string',
                    'description':
                    'The Dimensions ID of the publication linked to the dataset (single value).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'keywords': {
                    'type': 'string',
                    'description':
                    'Keywords used to describe the dataset (from authors).',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'research_orgs': {
                    'type': 'organizations',
                    'description':
                    'GRID organisations linked to the publication associated to the dataset (note: this field supports count: count).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_bra': {
                    'type': 'categories',
                    'description':
                    '`Broad Research Areas <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'figshare_url': {
                    'type': 'string',
                    'description': 'Figshare URL for the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'date_embargo': {
                    'type': 'date',
                    'description': 'The embargo date of the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'research_org_states': {
                    'type': 'states',
                    'description':
                    'State of the organisations the publication authors are affiliated to, expressed as GeoNames codes (ISO\u200c-3166-2).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'funder_countries': {
                    'type': 'countries',
                    'description':
                    'The country linked to the organisation funding the grant, expressed as GeoNames codes.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'date_modified': {
                    'type': 'date',
                    'description':
                    'The last modification date of the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'authors': {
                    'type': 'json',
                    'description':
                    'Ordered list of the dataset authors. ORCIDs are included if available.',
                    'long_description':
                    'Returned objects contain: `name`, `orcid`\n                                            \n                                           For example:\n\n    .. code-block:: json\n    \n        {\n            "name": "Steffen Vogt",\n            "orcid": ""\n        }',
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': False,
                    'is_multivalue': True
                },
                'language_title': {
                    'type': 'string',
                    'description':
                    'Dataset title language, as ISO 639-1 language codes.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'category_icrp_ct': {
                    'type': 'categories',
                    'description':
                    '`ICRP Cancer Types <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'journal': {
                    'type': 'journals',
                    'description': 'The journal a data set belongs to.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'license_name': {
                    'type': 'string',
                    'description':
                    "The dataset licence name, e.g. 'CC BY 4.0'.",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'category_rcdc': {
                    'type': 'categories',
                    'description':
                    '`Research, Condition, and Disease Categorization <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'year': {
                    'type': 'integer',
                    'description': 'Year of publication of the dataset.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'funders': {
                    'type': 'organizations',
                    'description':
                    'The GRID organisations funding the dataset.',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'category_hrcs_hc': {
                    'type': 'categories',
                    'description':
                    '`HRCS - Health Categories <https://dimensions.freshdesk.com/support/solutions/articles/23000018820-what-are-fields-of-research-and-other-classification-systems-and-how-are-they-created->`_',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': True
                },
                'language_desc': {
                    'type': 'string',
                    'description':
                    'Dataset title language, as ISO 639-1 language codes.',
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
                },
                'license_url': {
                    'type': 'string',
                    'description':
                    "The dataset licence URL, e.g. 'https://creativecommons.org/licenses/by/4.0/'.",
                    'long_description': None,
                    'is_entity': False,
                    'is_filter': False,
                    'is_facet': False,
                    'is_multivalue': False
                },
                'associated_publication': {
                    'type': 'publication_links',
                    'description':
                    'Publication linked to the dataset (single value).',
                    'long_description': None,
                    'is_entity': True,
                    'is_filter': True,
                    'is_facet': True,
                    'is_multivalue': False
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
                    'name': 'string',
                    'type': 'string',
                    'description':
                    "Name of the category. Note: this may include an identifier from the original source. E.g., '2.1 Biological and endogenous factors' (HRCS_RAC codes) or '1103 Clinical Sciences' (FOR codes).",
                    'long_description': None,
                    'is_filter': True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'cities': {
            'fields': {
                'id': {
                    'name': 'string',
                    'type': 'string',
                    'description':
                    "GeoNames city ID (eg '5391811' for `geonames:5391811 <http://www.geonames.org/5391811>`_ )",
                    'long_description': None,
                    'is_filter': True
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
                    'name': 'string',
                    'type': 'string',
                    'description':
                    "GeoNames country code (eg 'US' for `geonames:6252001 <http://www.geonames.org/6252001>`_ )",
                    'long_description': None,
                    'is_filter': True
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
                    'name': 'string',
                    'type': 'string',
                    'description':
                    'Dimensions ID of a journal. E.g., `jour.1016355 <https://app.dimensions.ai/discover/publication?and_facet_source_title=jour.1016355>`_ or `jour.1077219 <https://app.dimensions.ai/discover/publication?and_facet_source_title=jour.1077219>`_ .',
                    'long_description': None,
                    'is_filter': True
                },
                'title': {
                    'name': 'string',
                    'type': 'string',
                    'description':
                    "Title of a journal publication. E.g. 'Nature' or 'The Lancet'",
                    'long_description': None,
                    'is_filter': True
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
                    'name': 'string',
                    'type': 'string',
                    'description':
                    "Name of the organization group. E.g., 'NIH' or 'ICRP'.",
                    'long_description': None,
                    'is_filter': True
                }
            },
            'fieldsets': ['all', 'basics']
        },
        'states': {
            'fields': {
                'id': {
                    'name': 'string',
                    'type': 'string',
                    'description':
                    "GeoNames state code (ISO\u200c-3166-2). E.g., 'US.CA' for `geonames:5332921 <http://www.geonames.org/5332921>`_ .",
                    'long_description': None,
                    'is_filter': True
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
        'publication_links': {
            'fields': {
                'id': {
                    'name': 'string',
                    'type': 'string',
                    'description': 'Dimensions publication id',
                    'long_description': None,
                    'is_filter': True
                },
                'doi': {
                    'name': 'string',
                    'type': 'string',
                    'description': 'Digital object identifier',
                    'long_description': None,
                    'is_filter': True
                },
                'pmid': {
                    'name': 'string',
                    'type': 'string',
                    'description': 'PubMed ID',
                    'long_description': None,
                    'is_filter': True
                },
                'pmcid': {
                    'name': 'string',
                    'type': 'string',
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
                    'name': 'string',
                    'type': 'string',
                    'description':
                    "Dimensions ID of the open access category. E.g., one of 'closed', 'oa_all', 'gold_bronze', 'gold_pure', 'green_sub', 'gold_hybrid', 'green_pub', 'green_acc'. (see also the :ref:`publications` field ``open_access``).",
                    'long_description': None,
                    'is_filter': True
                },
                'name': {
                    'name': 'string',
                    'type': 'string',
                    'description':
                    "Name of the open access category. E.g., 'Closed' or 'Pure Gold'.",
                    'long_description': None,
                    'is_filter': True
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
