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


class BasicLexer(Lexer):
    def lex_document(self, document):
        def get_class(w):
            # if w in dim_lang_1:
            #     return "green bold"
            if w in VOCABULARY['lang']:
                return "green"
            elif w in VOCABULARY['sources'].keys():
                return "blue bold"
            elif w in VOCABULARY['sources']['publications']['fields']:
                return "blue"  # @TODO generalize
            # elif w in dim_entities_after_dot:
            #     return "violet"
            elif is_quoted(w):
                return "orange"
            elif w in VOCABULARY['allowed_starts'].keys():
                return "red"
            else:
                return "black"

        def get_line(lineno):

            return [(get_class(w), w + " ")
                    for w in document.lines[lineno].split()]

        return get_line
