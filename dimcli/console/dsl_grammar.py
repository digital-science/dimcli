#
# https://docs.dimensions.ai/dsl/data.html
#

# need a structure that contains desc / and possibly other lang metadata
# then maybe we can have 'children' as a key for nested objects

from .dsl_describe_bk import DESCRIBE_DATA_BK

if True:
    vocab_data = DESCRIBE_DATA_BK 
else:
    # @TODO get in real time from DSL
    pass 

SOURCES = vocab_data['sources']
ENTITY_TYPES = vocab_data['entities']

# note: attrs of entities are defined only at the entity_type level
ENTITIES = [] 
for x in SOURCES:
    for val in SOURCES[x]['facets']:
        if SOURCES[x]['facets'][val]['is_entity']:
            ENTITIES += [(val, SOURCES[x]['facets'][val]['type'])]
    for val in SOURCES[x]['fields']:
        if SOURCES[x]['fields'][val]['is_entity']:
            ENTITIES += [(val, SOURCES[x]['fields'][val]['type'])]
ENTITIES = sorted(list(set(ENTITIES))) # => [('FOR', 'category'), ('FOR_first', 'category') etc...]





GRAMMAR = {
    'allowed_starts': {
        'help' : [],
        'quit' : [],
        'show' : [ 'json_compact', 'json_pretty', 'json_html'],
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
    ]
}




VOCABULARY = { **{'sources' : SOURCES}, **{'entities' : ENTITY_TYPES}, **GRAMMAR }





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
                



