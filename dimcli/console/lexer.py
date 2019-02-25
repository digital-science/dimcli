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

        self.is_string_flag = False

        def get_class(w):
            if is_single_word_quoted(w): 
                return "orange"
            # if len(w) and w[0] == '"':
            #     if self.is_string_flag:
            #         self.is_string_flag = False
            #         return "orange"
            #     else:
            #         self.is_string_flag = True
            # elif self.is_string_flag:
            #     return "orange"
            elif w in lang:
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

        def get_line(lineno):
            # NOTE: this gets called at each single key press, so the line is re-rendered all the time
            return [(get_class(w), w + " ")
                    for w in document.lines[lineno].split()]

        return get_line
