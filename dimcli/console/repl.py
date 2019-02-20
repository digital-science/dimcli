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
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.formatted_text import HTML

# from prompt_toolkit import prompt   #using session instead
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

import click
import json
import sys
import os
import time
import webbrowser
import requests

from .dsl_grammar import *
from .utils import *
from .keys import *
from .lexer import *
from ..dimensions import Dsl, USER_JSON_OUTPUTS_DIR

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


class DataBuffer(object):
    current_json = ""
    current_query = ""

    def load(self, json_data, query):
        self.current_json = json_data
        self.current_query = query

    def retrieve(self):
        return (self.current_json, self.current_query)


def show_json(jjson, query, terminal=False):
    "print out json to the user"
    formatted_json = json.dumps(jjson, indent=4, sort_keys=True)
    if terminal:
        from pygments import highlight, lexers, formatters
        colorful_json = highlight(formatted_json, lexers.JsonLexer(),
                                  formatters.TerminalFormatter())
        print(colorful_json)
    else:
        contents = html_template_interactive(query, formatted_json)

        filename = time.strftime("%Y%m%d-%H%M%S.html")

        url = save2File(contents, filename, USER_JSON_OUTPUTS_DIR)

        webbrowser.open(url)


def handle_query(CLIENT, text, databuffer):
    """main procedure after user input"""

    if text.replace("\n", "").strip() == "nice_html":
        jsondata, query = databuffer.retrieve()
        if jsondata:
            show_json(jsondata, query, terminal=False)
        else:
            print("Nothing to show - please run a search first.")
    elif text.replace("\n", "").strip() == "show":
        jsondata, query = databuffer.retrieve()
        if jsondata:
            show_json(jsondata, query, terminal=True)
        else:
            print("Nothing to show - please run a search first.")
    else:
        # lazy complete
        text = line_lazy_return(text)
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
            databuffer.load(res, text)


#
#
# MAIN CLI
#
#


def run(instance="live"):
    """
    run the repl
    """

    try:
        CLIENT = Dsl(instance=instance, show_results=False, rich_display=False)
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)
        # if err.response.status_code == 401:
        #     print("here")

    click.secho("Welcome!")
    click.secho("Please enter your query below.")
    click.secho(
        "TAB = suggest | Ctrl-C = abort query | Ctrl-D = exit | Ctrl-] = search docs (https://docs.dimensions.ai/dsl)",
        dim=True)

    our_history = ThreadedHistory(SlowHistory())
    # The history needs to be passed to the `PromptSession`. It can't be passed
    # to the `prompt` call because only one history can be used during a
    # session.
    session = PromptSession(history=our_history)

    databuffer = DataBuffer()

    # REPL loop.
    while True:
        try:
            text = session.prompt(
                "\n> ",
                default="",  # you can pass a default text to begin with
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
            handle_query(CLIENT, text, databuffer)
    print("GoodBye!")


if __name__ == "__main__":
    run()
