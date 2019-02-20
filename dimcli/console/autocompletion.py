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

        elif line_last_word(line_minus_current) in ["search", "return"]:
            # after search and return only sources
            candidates = VOCABULARY['sources'].keys()

        elif line_last_word(line_minus_current) == "in":
            source = line_search_subject(line)  # generic solution
            if source in VOCABULARY['sources'].keys():
                candidates = VOCABULARY['sources'][source]['fields']
            else:
                pass

        elif line_last_word(line_minus_current) == "where":
            source = line_search_subject(line)  # generic solution
            if source in VOCABULARY['sources'].keys():
                fields = VOCABULARY['sources'][source]['fields']
                entities = [
                    x[0] for x in VOCABULARY['sources'][source]['entities']
                ]
                candidates = list(set(fields + entities))
            else:
                pass

        else:
            candidates = [x for x in VOCABULARY['lang'] if x != "search"]

        # finally
        for keyword in candidates:
            if keyword.startswith(word):
                yield Completion(keyword, start_position=-len(word))
