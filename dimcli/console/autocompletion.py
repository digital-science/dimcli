#!/usr/bin/env python
"""
Autocompletion.

Press [Tab] to complete the current word.
- The first Tab press fills in the common part of all completions
    and shows all the completions. (In the menu)
- Any following tab press cycles through all the possible completions.
"""
from __future__ import unicode_literals

from prompt_toolkit.completion import Completion, Completer
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.formatted_text import HTML

# from prompt_toolkit import prompt   #using session instead
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

from .dsl_grammar import *
from .utils import *

#
# AUTO COMPLETION
#


class CleverCompleter(Completer):
    """
    Goal: complete that helps with Dimensions DSL grammar and predicates 

    info: https://python-prompt-toolkit.readthedocs.io/en/master/pages/reference.html#prompt_toolkit.document.Document
    
    """

    def get_completions(self, document, complete_event):
        #
        word = document.get_word_before_cursor(WORD=True)
        line = document.current_line_before_cursor
        line_minus_current = line.replace(word, "").strip()
        # debug
        # click.secho("\nAutocomplete running..", dim=True)
        # click.secho("WORD=" + word, dim=True)
        # click.secho("LINE=" + line, dim=True)
        # click.secho("LINE_MINUS_CURRENT=" + line_minus_current, dim=True)

        # line_minus_current = line
        candidates = []

        if word.endswith("."):
            # @TODO
            candidates = []

        elif len(line_minus_current) == 0:  # remove the current stem from line
            # beginning: only main keywords
            candidates = VOCABULARY['allowed_starts']

        elif line_last_word(line_minus_current) in ["show"]:
            # beginning: only main keywords
            candidates = VOCABULARY['allowed_starts']["show"]

        elif line_last_word(line_minus_current) in ["search"]:
            # after search and return only sources
            candidates = VOCABULARY['sources'].keys()

        elif line_last_word(line_minus_current) in ["return"]:
            # after search and return only sources
            # candidates = list(VOCABULARY['sources'].keys())
            source = line_search_subject(line)  # generic solution
            if source in VOCABULARY['sources'].keys():
                fields = VOCABULARY['sources'][source]['facets']
                entities = [
                    x[0] for x in VOCABULARY['sources'][source]['entities']
                ]
                candidates = list(set(fields + entities + [source]))

        elif line_last_word(line_minus_current) == "in":
            source = line_search_subject(line)  # generic solution
            if source in VOCABULARY['sources'].keys():
                candidates = VOCABULARY['sources'][source]['search_fields']

        elif line_last_word(line_minus_current) in ["where", "and"]:
            source = line_search_subject(line)  # generic solution
            if source in VOCABULARY['sources'].keys():
                fields = VOCABULARY['sources'][source]['fields']
                entities = [
                    x[0] for x in VOCABULARY['sources'][source]['entities']
                ]
                candidates = list(set(fields + entities))

        elif line_last_word(line_minus_current) == "aggregate":
            source = line_search_subject(line)  # generic solution
            if source in VOCABULARY['sources'].keys():
                candidates = VOCABULARY['sources'][source]['metrics']

        elif line_last_two_words(line_minus_current) == "sort by":  # # https://docs.dimensions.ai/dsl/language.html#sort         
            source = line_search_subject(line) 
            return_object = line_search_return(line)  
            aggreg_object = line_search_aggregates(line)  
            if return_object in VOCABULARY['sources'].keys(): # if source, can sort by several things
                metrics = VOCABULARY['sources'][return_object]['metrics']
                fields = VOCABULARY['sources'][return_object]['fields']
                candidates = list(set(fields + metrics))
            else: # if not source, it's a facet so can only sort by count or aggregates
                candidates = ['count']
                if aggreg_object: 
                    candidates += [aggreg_object]


        else:
            candidates = [x for x in VOCABULARY['lang'] if x != "search"]

        # finally
        for keyword in candidates:
            if keyword.startswith(word):
                yield Completion(keyword, start_position=-len(word))
