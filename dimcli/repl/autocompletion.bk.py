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

from ..core.dsl_grammar import *
from ..core.utils import *

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
        # DEBUG
        # click.secho("\nAutocomplete running..", dim=True)
        # click.secho("WORD=" + word, dim=True)
        # click.secho("LINE=" + line, dim=True)
        # click.secho("LINE_MINUS_CURRENT=" + line_minus_current, dim=True)

        # line_minus_current = line
        candidates = []

        if word.endswith("."):
            # @TODO
            source = line_search_subject(line)
            entity = line_last_word(line).replace(".", "")
            # print("***" + entity_test + "***")
            candidates = []
            for x in ENTITIES:
                if entity == x[0]:
                    entity_type = x[1]
                    # print("***" + entity_type + "***")
                    if entity_type in ENTITY_TYPES.keys():
                        candidates = listify_and_unify(ENTITY_TYPES[entity_type]['fields'].keys())
                        # print("***" + str(candidates) + "***")

        elif len(line_minus_current) == 0:  # remove the current stem from line
            candidates = VOCABULARY['allowed_starts']

        elif line_last_word(line_minus_current) in ["show"]:
            candidates = VOCABULARY['allowed_starts']["show"]

        elif line_last_word(line_minus_current) in ["describe"]:
            candidates = VOCABULARY['allowed_starts']["describe"]

        elif line_last_word(line_minus_current) in ["search"]:
            # after search and return only sources
            candidates = listify_and_unify(VOCABULARY['sources'].keys())

        elif line_last_word(line_minus_current) in ["return"]:
            source = line_search_subject(line)  # generic solution
            if source in VOCABULARY['sources'].keys():
                facets = VOCABULARY['sources'][source]['facets'].keys()
                candidates = listify_and_unify(facets, [source])

        elif line_last_word(line_minus_current) == "in":
            source = line_search_subject(line)  # generic solution
            if source in VOCABULARY['sources'].keys():
                # candidates = VOCABULARY['sources'][source]['search_fields']
                candidates = listify_and_unify(VOCABULARY['sources'][source]['search_fields'])

        elif line_last_word(line_minus_current) in ["where", "and"]:
            source = line_search_subject(line)  # generic solution
            if source in VOCABULARY['sources'].keys():
                fields = VOCABULARY['sources'][source]['fields'].keys()
                facets = VOCABULARY['sources'][source]['facets'].keys()
                candidates = listify_and_unify(fields, facets)

        elif line_last_word(line_minus_current) == "aggregate":
            source = line_search_subject(line)  # generic solution
            if source in VOCABULARY['sources'].keys():
                candidates = listify_and_unify(VOCABULARY['sources'][source]['metrics'].keys())

        elif line_last_two_words(line_minus_current) == "sort by":  # # https://docs.dimensions.ai/dsl/language.html#sort         
            source = line_search_subject(line) 
            return_object = line_search_return(line)  
            aggreg_object = line_search_aggregates(line)  
            if return_object in VOCABULARY['sources'].keys(): # if source, can sort by several things
                metrics = VOCABULARY['sources'][return_object]['metrics'].keys()
                fields = VOCABULARY['sources'][return_object]['fields'].keys()
                candidates = listify_and_unify(fields, metrics)
            else: # if not source, it's a facet so can only sort by count or aggregates
                candidates = ['count']
                if aggreg_object: 
                    candidates += [aggreg_object]


        else:
            candidates = [x for x in VOCABULARY['lang'] if x != "search"]

        # finally
        if word.endswith("."):
            # print("***" + str(candidates) + "***")
            candidates = [word + x for x in candidates]
            for keyword in candidates:
                yield Completion(
                    keyword, 
                    start_position=-len(word),
                    display=keyword.replace(word, ""),
                    display_meta=build_display_meta(keyword.replace(word, "")),
                    )
        else:
            for keyword in candidates:
                if keyword.startswith(word):
                    yield Completion(
                        keyword, 
                        start_position=-len(word),
                        display=keyword,
                        display_meta=build_display_meta(keyword),
                        )




# TODO handle fields with same name across different sources/entities!
def build_display_meta(keyword):
    for group,vals in VOCABULARY.items(): 
        if type(vals) == dict: # ==> dict_keys(['clinical_trials', 'grants', etc..])
            for name,section in vals.items(): 
                if type(section) == dict: # ==> {'fields': {'acronym': {'description': None, 'is_filter': True, 'long_description': None, 'name': 'acronym', 'type': 'string'}, etc...
                    for field, field_desc in section.items():
                        if type(field_desc) == dict:
                            if keyword in field_desc.keys():
                                return field_desc[keyword]['description']
    return None

