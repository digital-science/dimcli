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
        source = line_search_subject(line)
        # DEBUG
        # click.secho("\nAutocomplete running..", dim=True)
        # click.secho("WORD=" + word, dim=True)
        # click.secho("LINE=" + line, dim=True)
        # click.secho("LINE_MINUS_CURRENT=" + line_minus_current, dim=True)

        # line_minus_current = line
        candidates = []

        if word.endswith("."):
            entity_facet = line_last_word(line).replace(".", "")
            entity = G.entity_type_for_source_facet(source, entity_facet)
            candidates = G.fields_for_entity_from_source_facet(source, entity_facet)

        elif len(line_minus_current) == 0:  # remove the current stem from line
            candidates = G.allowed_starts()

        elif line_last_word(line_minus_current) in ["show"]:
            candidates = G.allowed_starts("show")

        elif line_last_word(line_minus_current) in ["describe"]:
            candidates = G.allowed_starts("describe")

        elif line_last_word(line_minus_current) in ["search"]:
            candidates = G.sources()

        elif line_last_word(line_minus_current) in ["return"]:
            if source in G.sources():
                candidates = G.facets_for_source(source) + [source]

        elif line_search_subject_is_valid(line_minus_current):
            candidates = G.lang_after_search()

        elif line_return_subject_is_valid(line_minus_current):
            candidates = G.lang_after_return()

        elif line_last_word(line_minus_current) == "in":
            candidates = G.search_fields_for_source(source)

        elif line_last_word(line_minus_current) in ["where", "and", "or", "not"]:
            candidates = G.filters_for_source(source)

        elif line_filter_is_partial(line_minus_current):
            candidates = G.lang_filter_operators()

        elif line_filter_is_complete(line_minus_current):  # IMP this must to go after previous case
            candidates = G.lang_after_filter()

        elif line_for_text_is_complete(line_minus_current):  # IMP this must to go after previous case
            candidates = G.lang_after_for_text()

        elif line_for_text_search_inner(line_minus_current):
            candidates = G.lang_text_operators()

        elif line_last_word(line_minus_current) == "aggregate":
            # aggr. can be used only when returning facets!
            return_object = line_search_return(line)
            if return_object in G.facets_for_source(source):
                candidates = G.metrics_for_source(source)

        elif line_last_two_words(line_minus_current) == "sort by":  
            return_object = line_search_return(line)  
            if return_object in G.sources(): 
                # if source, can sort by fields
                candidates = G.fields_for_source(source) + ['relevance']
            elif return_object in G.facets_for_source(source):
                # if facet, can sort by aggregrates metrics if available, otherwise count
                aggreg_object = line_search_aggregates(line)
                if aggreg_object:
                    candidates = ['aggreg_object']   
                else:
                    candidates = ['count']          

        else:
            candidates = [] # 2019-04-15
            # candidates = [x for x in G.lang() if x != "search"] # not destructive

        # finally
        if word.endswith("."):
            # print("***" + str(candidates) + "***")
            candidates = sorted([word + x for x in candidates])
            for keyword in candidates:
                yield Completion(
                    keyword, 
                    start_position=-len(word),
                    display=keyword.replace(word, ""),
                    display_meta=build_help_string(keyword.replace(word, ""), entity=entity),
                    )
        else:
            candidates = sorted(candidates)
            for keyword in candidates:
                if keyword.startswith(word):
                    yield Completion(
                        keyword, 
                        start_position=-len(word),
                        display=keyword,
                        display_meta=build_help_string(keyword, source=source),
                        )


def build_help_string(field, source="", entity=""):
    if source:
        return G.desc_for_source_field_enriched(source, field)
    elif entity:
        return G.desc_for_entity_field_enriched(entity, field)
    else:
        return ""

