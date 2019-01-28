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

import json, sys

from .dsl_grammar import *
from .credentials import *
from .lib import DimensionsClient

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

        def last_word(line):
            if len(line) > 0:
                return line.split()[-1]
            else:
                return False

        def is_search_for(line, source_name):
            if "search " + source_name in line:
                return True
            else:
                return False

        candidates = []

        if word.endswith("."):
            # properties @TODO
            candidates = dim_entities_after_dot

        elif len(line_minus_current) == 0:
            # beginning: only main keywords
            # PS ensure you remove the current stem from line
            candidates = Allowed_Starts

        elif last_word(line_minus_current) in dim_lang_1:
            # after search and return only sources
            candidates = Sources_All

        elif last_word(line_minus_current) == "in":
            if is_search_for(line, "publications"):
                candidates = Publications_Search_Fields
            else:
                pass

        elif last_word(line_minus_current) == "where":
            if is_search_for(line, "publications"):
                candidates = Publication_Literal_Fields + Publications_Entity_Fields
            else:
                pass

        else:
            candidates = [x for x in dim_all_completions if x != "search"]

        # finally
        for keyword in candidates:
            if keyword.startswith(word):
                yield Completion(keyword, start_position=-len(word))


#
# LEXER AND SYNTAX HIGHLIGHTING
#
# https://python-prompt-toolkit.readthedocs.io/en/master/pages/reference.html#prompt_toolkit.lexers.Lexer
#
#

from prompt_toolkit.lexers import Lexer


def is_quoted(w):
    if w[0] == '"' and w[-1] == '"':
        return True
    if w[0] == "'" and w[-1] == "'":
        return True
    return False


class BasicLexer(Lexer):
    def lex_document(self, document):
        def get_class(w):
            if w in dim_lang_1:
                return "green bold"
            if w in dim_lang_2 + dim_lang_3:
                return "green"
            elif w in Sources_All:
                return "blue bold"
            elif w in Publications_Facet_Fields:
                # with Publication_Literal_Fields Lexer FAILS @TODO
                return "blue"
            elif w in dim_entities_after_dot:
                return "violet"
            elif is_quoted(w):
                return "orange"
            elif w in Allowed_Starts:
                return "red"
            else:
                return "black"

        def get_line(lineno):

            return [(get_class(w), w + " ")
                    for w in document.lines[lineno].split()]

        return get_line


#
# KEY BINDINGS OVERRIDE
#

bindings = KeyBindings()


@bindings.add("c-space")
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


@bindings.add("c-]")
def _(event):
    """
    Look up in docs
    """
    line = event.app.current_buffer.text
    if line:
        last_word = line.split()[-1]
        import webbrowser
        webbrowser.open("https://docs.dimensions.ai/dsl/search.html?q=" +
                        last_word)
    return


# @bindings.add("c-x")
# def _(event):
#     " Exit when `c-x` is pressed. "
#     event.app.exit()

#
# VALIDATOR
#
#


class BasicValidator(Validator):
    def validate(self, document):
        text = document.text

        if text and "return" not in text:

            raise ValidationError(
                message="A query must include a return statement",
                # cursor_position=i
            )


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
            yield "item-%s" % (i, )

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


def handle_query(CLIENT, text, buffer):
    # @TODO query dimensions and open up a webpage

    if text.replace("\n", "").strip() == "show":
        res = buffer.yeald()
        if res:
            jj = json.dumps(res, indent=4, sort_keys=True)
            print(jj)
        else:
            print("Nothing to show - please run a search first.")
    else:
        print("You said: %s" % text)
        # RUN QUERY
        res = CLIENT.query(text)
        # #
        if "errors" in res.keys():
            print(res["errors"]["query"]["header"])
            for x in res["errors"]["query"]["details"]:
                print(x)
        else:
            print("Tot Results: ", res["_stats"]["total_count"])
            for k in res.keys():
                if k != "_stats":
                    print(k.capitalize() + ":", len(res[k]))
            buffer.load(res)


#
#
# MAIN CLI
#
#


def main(credentials):
    click.secho(
        "Enter your query (Tab=suggest / Ctrl-C = stop / Ctrl-D = exit / Ctrl-] = search docs) API: https://docs.dimensions.ai/dsl",
        dim=True)

    CLIENT = DimensionsClient(**credentials)

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
                "\n> ",
                default="",  # you can pass a default text to begin with
                # completer=dim_completer,
                completer=CleverCompleter(),
                complete_style=CompleteStyle.READLINE_LIKE,
                # validator=BasicValidator(),
                # validate_while_typing=False,
                multiline=False,
                complete_while_typing=True,
                lexer=BasicLexer(),
                key_bindings=bindings,
            )
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.
        else:
            if text.strip() == "":
                continue
            elif text == "quit":
                break
            handle_query(CLIENT, text, buffer)
    print("GoodBye!")


if __name__ == "__main__":
    credentials = get_credentials()
    main(credentials)
