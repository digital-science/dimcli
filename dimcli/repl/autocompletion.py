#!/usr/bin/env python

"""
Autocompletion.

Press [Tab] to complete the current word.
- The first Tab press fills in the common part of all completions
    and shows all the completions. (In the menu)
- Any following tab press cycles through all the possible completions.
"""

from __future__ import unicode_literals

# NOTE this is compatible also with older versions of prompt-toolkit (eg < 2) so will run in Google Colab or Conda 
from prompt_toolkit.completion import Completion, Completer

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

        if not line:  # no letter, all empty
            candidates = G.allowed_starts_dsl_query()

        elif len(line_minus_current) == 0:  # single word, beginning of line
            candidates = G.allowed_starts()

        elif line_minus_current and word.endswith("."):
            entity_facet = line_last_word(line).replace(".", "")
            entity = G.entity_type_for_source_facet(source, entity_facet)
            candidates = G.fields_for_entity_from_source_facet(source, entity_facet)

        elif in_categories_search(line):
            this_category = in_categories_search(line)
            # print(this_category)
            candidates = G.categories(this_category)
 
        elif in_square_brackets(line):
            # https://docs.dimensions.ai/dsl/language.html#return-specific-fields
            # search publications for "bmw" return journal[id + title]"
            test_return_obj = line_last_return_subject(line)
            if test_return_obj == source:
                # print("*" + test_return_obj + "*")
                candidates = G.fields_for_source(test_return_obj)
            elif test_return_obj in G.facets_for_source(source):
                entity = G.entity_type_for_source_facet(source, test_return_obj)
                candidates = G.fields_for_entity_from_source_facet(source, test_return_obj)

        elif line_last_word(line_minus_current) in [".docs"]:
            candidates = G.sources() + G.entities()

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
            test_return_obj = line_last_return_subject(line)
            if test_return_obj == source:
                candidates = [x for x in G.lang_after_return() if x != 'aggregate']
            else:
                candidates = G.lang_after_return()

        elif line_last_word(line_minus_current) == "in":
            candidates = G.search_fields_for_source(source)

        elif line_last_word(line_minus_current) in ["where", "and", "or", "not"]:
            candidates = G.filters_for_source(source)

        elif line_filter_is_partial(line_minus_current):
            candidates = G.lang_filter_operators()

        elif line_for_text_search_inner(line_minus_current):
            candidates = G.lang_text_operators()

        elif line_last_two_words(line_minus_current).startswith("limit"):
            if line_last_return_subject(line) == source:
                candidates = G.lang_after_limit()

        elif line_last_word(line_minus_current) == "aggregate":
            # aggr. can be used only when returning facets!
            return_object = line_search_return(line)
            if return_object in G.facets_for_source(source):
                candidates = G.metrics_for_source(source)

        elif line_last_two_words(line_minus_current) == "sort by":  
            return_object = line_search_return(line)  
            if return_object in G.sources(): 
                # if source, can sort by fields FIXME
                candidates = G.fields_for_source(source) + ['relevance']
            elif return_object in G.facets_for_source(source):
                # if facet, can sort by aggregates metrics if available, otherwise count
                aggreg_object = line_search_aggregates(line)
                if aggreg_object:
                    candidates = [aggreg_object]   
                else:
                    candidates = ['count']          

        elif line_last_three_words(line_minus_current).startswith("sort by"): 
            candidates = G.lang_after_sort_by()

        # IMP following two must go last
        elif line_filter_is_complete(line_minus_current):  
            candidates = G.lang_after_filter()
        elif line_for_text_is_complete(line_minus_current): 
            candidates = G.lang_after_for_text()
        # finally
        else:
            candidates = [] 

        #
        # now build the candidates list
        #

        if line_minus_current and word.endswith("."):
            # print("***" + str(candidates) + "***")
            candidates = sorted([word + x for x in candidates])
            for keyword in candidates:
                yield Completion(
                    keyword, 
                    start_position=-len(word),
                    display=keyword.replace(word, ""),
                    display_meta=build_help_string(keyword.replace(word, ""), entity=entity),
                    )

        elif in_square_brackets(line):
            # print("***" + str(word) + "***")
            candidates = sorted(candidates)
            for keyword in candidates:
                if word.rfind("+") > 0:
                    word = word[word.find("+")+1:]
                else:
                    word = word[word.find("[")+1:]
                if keyword.startswith(word):
                    yield Completion(
                        keyword, 
                        start_position=-len(word),
                        display=keyword,
                        display_meta=build_help_string(keyword, source=source),
                        )      

        elif in_categories_search(line):
            candidates = sorted([word + x for x in candidates])
            for keyword in candidates:
                yield Completion(
                    keyword, 
                    start_position=-len(word),
                    display=keyword.replace(word, ""),
                    display_meta=build_help_string(keyword),
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

