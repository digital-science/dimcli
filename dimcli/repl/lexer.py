#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# LEXER AND SYNTAX HIGHLIGHTING
#
# https://python-prompt-toolkit.readthedocs.io/en/master/pages/reference.html#prompt_toolkit.lexers.Lexer
#
#

from prompt_toolkit.lexers import Lexer
from ..core.dsl_grammar import *
from ..core.utils import *



# ====
#
allowed_starts = G.allowed_starts()
lang = split_multi_words(G.lang())
#
sources = G.sources()
entities = G.entities()
#
fields = list_flatten([G.fields_for_source(source) for source in sources])
facets = list_flatten([G.facets_for_source(source) for source in sources])
fieldsets = list_flatten([G.fieldsets_for_source(source) for source in sources])
metrics = list_flatten([G.metrics_for_source(source) for source in sources])
search_fields = list_flatten([G.search_fields_for_source(source) for source in sources])
#
# ====

class BasicLexer(Lexer):
    """
    note: lexer is single word based, so multi word DSL operands need to split first 
    """
    def lex_document(self, document):

        def get_class(w):
            "color classes for main objects - color-safe"
            if w in lang:
                return "bold"
            elif w in sources + entities:
                return "bold"
            elif w in fields:
                return "italic"
            elif w in facets:
                return "italic" 
            elif w in metrics:
                return "italic" 
            elif w in fieldsets + search_fields:
                return "italic" 
            elif w in allowed_starts:
                return "bold"
            else:
                return "nobold"

        def previous_get_class(w):
            "DEPRECATED DUE TO UNREADABILITY ON SOME TERMINALS - color classes for main objects"
            if w in lang:
                return "green"
            elif w in sources + entities:
                return "blue bold"
            elif w in fields:
                return "blue"
            elif w in facets:
                return "blue" 
            elif w in metrics:
                return "brown" 
            elif w in fieldsets + search_fields:
                return "black" 
            elif w in allowed_starts:
                return "red"
            else:
                return "black"

        def _spot_strings_bits(data):
            "note: this is run after the whole sentence has been parsed and marked up, so to be able to spot multi-word strings"
            STRING_COLOR = "red"
            is_string_flag = False
            for x in data:
                if is_string_flag:
                    x[0] = STRING_COLOR
                    if x[1].strip()[-1] == '"':
                        is_string_flag = False
                elif x[1].strip()[0] == '"' and x[1].strip()[-1] == '"':
                    x[0] = STRING_COLOR
                elif x[1].strip()[0] == '"':
                    x[0] = STRING_COLOR
                    is_string_flag = True
            return data

        def get_line(lineno):
            "NOTE: this gets called at each single key press, i.e. line is re-rendered all the time"
            data = [[get_class(w), w + " "]
                    for w in document.lines[lineno].split()]
            # add on to mark up multi-word strings post-process
            data = _spot_strings_bits(data)
            return data

        return get_line
