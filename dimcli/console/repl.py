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
from prompt_toolkit.history import FileHistory

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
from .autocompletion import *
from .key_bindings import *
from .lexer import *
from ..dimensions import Dsl, USER_DIR, USER_JSON_OUTPUTS_DIR

#
#
# PARAMETERS
#
#

HISTORY_FILE = os.path.expanduser(USER_DIR + "history")

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


def print_json(jjson, query, terminal=False):
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


def show_command(text, databuffer):
    """
    show results of a query
    """
    DEFAULT = "preview"
    text = text.replace("show", "").strip()
    if not text: text = DEFAULT
    # no data
    jsondata, query = databuffer.retrieve()
    if not jsondata:
        print("Nothing to show - please run a search first.")
        return
    # cases
    if text == "html":
        print_json(jsondata, query, terminal=False)

    elif text == "json":
        print_json(jsondata, query, terminal=True)

    elif text == "preview":
        # simple way to get some useful data HACK
        for x in jsondata.keys():
            if x == "_stats":
                pass
            elif x in VOCABULARY['sources'].keys():
                for row in jsondata[x]:
                    try:
                        print(row['title'], row['id'])
                    except:
                        print(row)
            else:
                print("Preview for result type *%s* not implemented" % x)


def handle_query(CLIENT, text, databuffer):
    """main procedure after user input"""

    if text.replace("\n", "").strip().startswith("show"):
        show_command(text.replace("\n", "").strip(), databuffer)

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

    # history
    session = PromptSession(history=FileHistory(HISTORY_FILE))

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
