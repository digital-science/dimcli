#
# https://docs.dimensions.ai/dsl/data.html
#

# need a structure that contains desc / and possibly other lang metadata
# then maybe we can have 'children' as a key for nested objects

from .dsl_grammar_extras import *
from .dsl_grammar_core import *
from .dsl_grammar_categories import *

if True:
    vocab_data = GRAMMAR_DICT 
    syntax_data = SYNTAX_DICT 
    categories_data = CATEGORIES_DICT 
else:
    # @TODO get in real time from DSL
    pass 


# simple util that must stay here to avoid circular imports with utils.py
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


class DslGrammar():
    """
    Wrapper for the DSL Grammar dict

    """
    def __init__(self, grammar_dict, extra_syntax, categories_dict=None):
        self.grammar = grammar_dict
        self.syntax = extra_syntax
        self.categories_names = list(categories_dict.keys())
        self.categories_data = categories_dict
        # DslGrammar.__init__(self, data)

    def __getitem__(self, key):
        "return dict key as slice"
        if key in self.grammar:
            return self.grammar[key]
        else:
            return False

    def __repr__(self):
        stats = [(x, len(self.grammar[x])) for x in self.grammar.keys()]
        return "<Dsl Grammar object #%s. %s>" % (str(id(self)), str(stats))

    # 
    # SYNTAX METHODS
    # 

    def allowed_starts(self, word=""):
        "Get a the allowed starts dict for Dimcli"
        allowed_starts = merge_two_dicts(self.allowed_starts_dsl_query(), self.allowed_starts_special_commands())
        if not word:
            return allowed_starts
        else:
            try:
                return allowed_starts[word]
            except:
                return []
    def allowed_starts_dsl_query(self):
        "Get a the allowed starts dict specific to he DSL syntax"
        return self.syntax['allowed_starts_dsl_query']
    def allowed_starts_special_commands(self):
        "Get a the allowed starts dict specific to he DIMCLI special syntax"
        return self.syntax['allowed_starts_special_commands']

    def lang(self):
        "Get a list of all lang operators"
        return self.syntax['lang_all']
    def lang_after_search(self):
        "Get a list of all lang operators after a valid search -source- statement"
        return self.syntax['lang_after_search']
    def lang_filter_operators(self):
        "Get a list of all lang operators for a filter statement eg  `search -source- where -filter-` statement"
        return self.syntax['lang_filter_operators']
    def lang_text_operators(self):
        "Get a list of all lang operators for a text search eg  `search -source- for 'x AND y'`"
        return self.syntax['lang_text_operators']
    def lang_after_for_text(self):
        "Get a list of all lang operators after a valid `for 'text'` statement"
        return self.syntax['lang_after_for_text']
    def lang_after_filter(self):
        "Get a list of all lang operators after a valid `search -source- where -filter=?-` statement"
        return self.syntax['lang_after_filter']
    def lang_after_sort_by(self):
        "Get a list of all lang operators after a valid `return -source- sort by -field-` statement"
        return self.syntax['lang_after_sort_by']
    def lang_after_return(self):
        "Get a list of all lang operators after a valid `return -source-` statement"
        return self.syntax['lang_after_return']
    def lang_after_limit(self):
        "Get a list of all lang operators after a valid `limit -N-` statement - ie skip"
        return self.syntax['lang_after_limit']

    def url_for_source(self, source):
        "Get a the Dimensions URL for a specific source"
        try:
            return self.syntax['dimensions_urls'][source]
        except:
            return []

    def object_id_patterns(self):
        """Return a dictionary representing known string-prefixes for object IDs
        Note: in some cases eg patents this is missing.
        """
        return self.syntax['dimensions_object_id_patterns']           
    # 
    # GRAMMAR METHODS IE the dsl sources / fields
    # 

    # generic

    def get_field_json(self, field, source=None, entity=None):
        "Get the raw json for a field"
        if source:
            try:
                return self.grammar['sources'][source]['fields'][field]
            except:
                return None
        elif entity:
            try:
                return self.grammar['entities'][entity]['fields'][field]
            except:
                return None            

    # sources 

    def sources(self):
        "Get a list of all sources available"
        return [x for x in self.grammar['sources'].keys()]

    def fields_for_source(self, source, filters=False, facets=False, fieldtype=False):
        "Get a list of all fields available"
        out= []
        if source not in self.sources():
            return []
        for field,specs in self.grammar['sources'][source]['fields'].items():
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

    def entity_type_for_source_facet(self, source, facet):
        "from a facet, return the entity name EG object link to entities"
        if not facet in self.facets_for_source(source):
            return []
        return self.grammar['sources'][source]['fields'][facet]['type']

    def desc_for_source_field(self, source, field):
        "from a source-field combination, return the description"
        if not field in self.fields_for_source(source):
            return ""
        return self.grammar['sources'][source]['fields'][field]['description']
    def desc_for_source_field_enriched(self, source, field):
        "A decription prefixed by extra info for a field eg if it is a facet"
        # desc = self.desc_for_source_field(source, field)
        json = self.get_field_json(field=field, source=source)
        try:
            desc = json['description'] or  ""
            if json['is_entity']:
                return "[ENTITY:%s] " % json['type'] + desc
            else:
                return "[LITERAL:%s] " % json['type'] + desc
        except:
            pass

    def fieldsets_for_source(self, source):
        "Get a list of all fieldsets available"
        try:
            return self.grammar['sources'][source]['fieldsets']
        except:
            return []

    def metrics_for_source(self, source):
        "Get a list of all metrics available"
        try:
            return [x for x in self.grammar['sources'][source]['metrics']]
        except:
            return []

    def search_fields_for_source(self, source):
        "Get a list of all search fields available"
        try:
            return self.grammar['sources'][source]['search_fields']
        except:
            return []

    # entity

    def entities(self):
        "Get a list of all entities available"
        return [x for x in self.grammar['entities'].keys()]

    def fields_for_entity(self, entity, filters=False, fieldtype=None):
        "Get a list of all fields available for an entity"
        out= []
        if entity not in self.entities():
            return []
        for field,specs in self.grammar['entities'][entity]['fields'].items():
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

    def fields_for_entity_from_source_facet(self, source, facet):
        "From entity field-name used in a source, get the list of fields for that entity has."
        if facet not in self.facets_for_source(source):
            return []
        entity = self.entity_type_for_source_facet(source, facet)
        if entity == "researchers":
            # SPECIAL CASE / hardwired
            # researchers is used as an entity, but it's actually a source
            return self.filters_for_source('researchers')
        else:
            return self.filters_for_entity(entity)  # only filters as used in 'where' context
        
    def desc_for_entity_field(self, entity, field):
        "from a entity-field combination, return the description"
        if not field in self.fields_for_entity(entity):
            return ""
        return self.grammar['entities'][entity]['fields'][field]['description']
    def desc_for_entity_field_enriched(self, entity, field):
        "A decription prefixed by extra info for a field eg if it a string or number"
        # @TODO similar to desc_for_source_field_enriched // consider refactoring
        json = self.get_field_json(field=field, entity=entity)
        try:
            desc = json['description'] or  ""
            return "[LITERAL:%s] " % json['type'] + desc
        except:
            pass

    # research categories

    def categories(self, name=None):
        "Get a list of all research categories available"
        if not name:
            return self.categories_names
        else:
            if self.categories_data.get(name, ""):
                return [x['name'] for x in self.categories_data[name]]            


# init grammar object from data
G = DslGrammar(vocab_data, syntax_data, categories_data)


