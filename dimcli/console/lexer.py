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




allowed_starts = VOCABULARY['allowed_starts'].keys()
lang = split_multi_words(VOCABULARY['lang'])
sources = VOCABULARY['sources'].keys()
fields = split_multi_words(VOCABULARY['sources']['publications']['fields']) # @TODO generalize

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
            elif w in sources:
                return "blue bold"
            elif w in fields:
                return "blue"  # @TODO generalize
            # elif w in dim_entities_after_dot:
            #     return "violet"
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
