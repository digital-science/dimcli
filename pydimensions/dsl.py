#!/usr/bin/env python
"""
Autocompletion example.

Press [Tab] to complete the current word.
- The first Tab press fills in the common part of all completions
    and shows all the completions. (In the menu)
- Any following tab press cycles through all the possible completions.
"""
from __future__ import unicode_literals

from prompt_toolkit.completion import Completion, Completer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.formatted_text import HTML
# from prompt_toolkit import prompt   #using session instead
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

#
# AUTO COMPLETION
#

# @TODO: smarter completer should keep into account previous words

meta_keywords = [
    # here go the main gramma words without the dot notation
    'quit',
    'show',
]

dim_keywords = [
    # here go the main gramma words without the dot notation
    'search',
    'for',
    'where',
    'return',
]

dim_entities = [
    # here go the main gramma words without the dot notation
    'publications',
    'year',
    'research_orgs',
    'funders'
]

main_completions = meta_keywords + dim_keywords + dim_entities

dim_entities_after_dot = [
    'research_orgs.name',  # trying to add DOT notation
    # @TODO programmatically add all variations based on docs
]


class CleverCompleter(Completer):
    """
    Goal: complete that helps with Dimensions DSL grammar and predicates 

    info: https://python-prompt-toolkit.readthedocs.io/en/master/pages/reference.html#prompt_toolkit.document.Document
    
    """

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor(WORD=True)
        # line = document.current_line_before_cursor()
        # print("\n" + word)
        if word.endswith('.'):
            for keyword in dim_entities_after_dot:
                if keyword.startswith(word):
                    yield Completion(keyword, start_position=-len(word))
        else:
            for keyword in main_completions:
                if keyword.startswith(word):
                    yield Completion(keyword, start_position=-len(word))


#
# KEY BINDINGS OVERRIDE
#

kb = KeyBindings()


@kb.add('c-space')
def _(event):
    """
    Start auto completion. If the menu is showing already, select the next
    completion.
    """
    b = event.app.current_buffer
    if b.complete_state:
        b.complete_next()
    else:
        b.start_completion(select_first=False)


#
# VALIDATOR
#
#


class BasicValidator(Validator):
    def validate(self, document):
        text = document.text

        if text and "return" not in text:

            raise ValidationError(
                message='A query must include a return statement',
                # cursor_position=i
            )


#
# LEXER AND SYNTAX HIGHLIGHTING
#
# https://python-prompt-toolkit.readthedocs.io/en/master/pages/reference.html#prompt_toolkit.lexers.Lexer
#
#

from prompt_toolkit.lexers import Lexer


def is_quoted(w):
    if w[0] == "\"" and w[-1] == "\"":
        return True
    if w[0] == "'" and w[-1] == "'":
        return True
    return False


class BasicLexer(Lexer):
    def lex_document(self, document):
        def get_class(w):
            if w in dim_keywords:
                return 'green bold'
            elif w in dim_entities:
                return 'blue bold'
            elif w in dim_entities_after_dot:
                return 'violet'
            elif is_quoted(w):
                return 'orange'
            elif w in meta_keywords:
                return "red"
            else:
                return 'black'

        def get_line(lineno):

            return [(get_class(w), w + " ")
                    for w in document.lines[lineno].split()]

        return get_line


#
#
# HISTORY
#
#

from prompt_toolkit.history import History, ThreadedHistory
import time


class SlowHistory(History):
    """
    Example class that loads the history very slowly...
    """

    def load_history_strings(self):
        for i in range(1000):
            time.sleep(1)  # Emulate slowness.
            yield 'item-%s' % (i, )

    def store_string(self, string):
        pass  # Don't store strings.


#
#
# DIMENSIONS QUERY AND DATA HANDLING
#
#


class Buffer(object):
    current_json = ""

    def load(self, _json):
        self.current_json = _json

    def yeald(self):
        return self.current_json


def handle_query(text, buffer):
    # @TODO query dimensions and open up a webpage

    if text.replace("\n", "").strip() == "show":
        res = buffer.yeald()
        jj = json.dumps(res, indent=4, sort_keys=True)
        print(jj)
    else:
        print('You said: %s' % text)
        res = client.query(text)
        if 'errors' in res.keys():
            print(res['errors']['query']['header'])
            for x in res['errors']['query']['details']:
                print(x)
        else:
            print("Tot Results: ", res['_stats']['total_count'])
            for k in res.keys():
                if k != '_stats':
                    print(k.capitalize() + ":", len(res[k]))
            buffer.load(res)


#
#
# MAIN CLI
#
#
import json, sys
import lib as dimlib
account_details = dimlib.get_init()
client = dimlib.DimensionsClient(**account_details)


def main():
    print("Enter your query (Esc+Enter=run / Control-C=stop / Control-D=exit)")

    our_history = ThreadedHistory(SlowHistory())
    # The history needs to be passed to the `PromptSession`. It can't be passed
    # to the `prompt` call because only one history can be used during a
    # session.
    session = PromptSession(history=our_history)

    buffer = Buffer()

    # REPL loop.
    while True:
        try:
            text = session.prompt(
                '\n> ',
                default="",  # you can pass a default text to begin with
                # completer=dim_completer,
                completer=CleverCompleter(),
                complete_style=CompleteStyle.READLINE_LIKE,
                # validator=BasicValidator(),
                # validate_while_typing=False,
                multiline=True,
                complete_while_typing=True,
                lexer=BasicLexer(),
                key_bindings=kb)
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.
        else:
            if text == "quit":
                break
            handle_query(text, buffer)
    print('GoodBye!')


if __name__ == '__main__':
    main()
