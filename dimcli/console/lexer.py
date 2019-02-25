#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# LEXER AND SYNTAX HIGHLIGHTING
#
# https://python-prompt-toolkit.readthedocs.io/en/master/pages/reference.html#prompt_toolkit.lexers.Lexer
#
#

from prompt_toolkit.lexers import Lexer
from .dsl_grammar import *
from .utils import *



#
allowed_starts = VOCABULARY['allowed_starts'].keys()
lang = split_multi_words(VOCABULARY['lang'])
#
sources = list(VOCABULARY['sources'].keys())
#
fields = list_flatten([VOCABULARY['sources'][source]['fields'] for source in sources])
facets = list_flatten([VOCABULARY['sources'][source]['facets'] for source in sources])
entities = list_flatten([VOCABULARY['sources'][source]['entities'] for source in sources])
fieldsets = list_flatten([VOCABULARY['sources'][source]['fieldsets'] for source in sources])
metrics = list_flatten([VOCABULARY['sources'][source]['metrics'] for source in sources])
search_fields = list_flatten([VOCABULARY['sources'][source]['search_fields'] for source in sources])
#

class BasicLexer(Lexer):
    """
    note: lexer is single word based, so multi word DSL operands need to split first 
    """
    def lex_document(self, document):
        def get_class(w):
            # if w in dim_lang_1:
            #     return "green bold"
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
            elif is_quoted(w): # @TODO improve for multi word strings
                return "orange"
            elif w in allowed_starts:
                return "red"
            else:
                return "black"

        def get_line(lineno):

            return [(get_class(w), w + " ")
                    for w in document.lines[lineno].split()]

        return get_line
