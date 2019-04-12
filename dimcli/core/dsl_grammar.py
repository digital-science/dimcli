#
# https://docs.dimensions.ai/dsl/data.html
#

# need a structure that contains desc / and possibly other lang metadata
# then maybe we can have 'children' as a key for nested objects

from .dsl_grammar_dict import GRAMMAR_DICT

if True:
    vocab_data = GRAMMAR_DICT 
else:
    # @TODO get in real time from DSL
    pass 

SOURCES = vocab_data['sources']
ENTITY_TYPES = vocab_data['entities']




class DslGrammar():
    """
    Wrapper for the DSL Grammar dict

    """
    def __init__(self, data):
        self.data = data
        # DslGrammar.__init__(self, data)

    def __getitem__(self, key):
        "return dict key as slice"
        if key in self.data:
            return self.data[key]
        else:
            return False

    def __repr__(self):
        return "<Dsl Grammar object #%s. %s>" % (str(id(self)), str(self.keys_and_count()))

    def keys(self,):
        return list(self.data.keys())

    def keys_and_count(self,):
        return [(x, len(self.data[x])) for x in self.data.keys()]

    def sources(self):
        "Get a list of all sources available"
        return [x for x in self.data['sources'].keys()]

    def entities(self):
        "Get a list of all entities available"
        return [x for x in self.data['entities'].keys()]

    def fields_for_source(self, source, filters=False, facets=False, fieldtype=False):
        "Get a list of all fields available"
        out= []
        for field,specs in self.data['sources'][source]['fields'].items():
            if filters:
                if specs['is_filter']:
                    out.append(field)
            elif facets:
                if specs['is_facet']:
                    out.append(field)
            elif fieldtype:
                if specs['type'] == fieldtype:
                    out.append(field)
            else:
                out.append(field)
        return out
    
    def filters_for_source(self, source):
        "Get a list of all fields-filters available"
        return self.fields_for_source(source, filters=True)

    def facets_for_source(self, source):
        "Get a list of all fields-facets available"
        return self.fields_for_source(source, facets=True)

    def fieldsets_for_source(self, source):
        "Get a list of all fieldsets available"
        return self.data['sources'][source]['fieldsets']

    def metrics_for_source(self, source):
        "Get a list of all metrics available"
        return [x for x in self.data['sources'][source]['metrics']]

    def search_fields_for_source(self, source):
        "Get a list of all search fields available"
        return self.data['sources'][source]['search_fields']

    def fields_for_entity(self, entity, filters=False, fieldtype=None):
        "Get a list of all fields available for an entity"
        out= []
        for field,specs in self.data['entities'][entity]['fields'].items():
            if filters:
                if specs['is_filter']:
                    out.append(field)
            elif fieldtype:
                if specs['type'] == fieldtype:
                    out.append(field)
            else:
                out.append(field)
        return out

    def filters_for_entity(self, source):
        "Get a list of all fields-filters available for an entity"
        return self.fields_for_entity(source, filters=True)



NEW_GRAMMAR = DslGrammar(vocab_data)


# note: attrs of entities are defined only at the entity_type level
ENTITIES = [] 
# for x in SOURCES:
#     for val in SOURCES[x]['facets']:
#         if SOURCES[x]['facets'][val]['is_entity']:
#             ENTITIES += [(val, SOURCES[x]['facets'][val]['type'])]
#     for val in SOURCES[x]['fields']:
#         if SOURCES[x]['fields'][val]['is_entity']:
#             ENTITIES += [(val, SOURCES[x]['fields'][val]['type'])]
# ENTITIES = sorted(list(set(ENTITIES))) # => [('FOR', 'category'), ('FOR_first', 'category') etc...]





GRAMMAR = {
    'allowed_starts': {
        'help' : [],
        'quit' : [],
        'show' : [ 'json_compact', 'json_pretty'],
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
                



