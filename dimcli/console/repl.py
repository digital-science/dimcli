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
from .autocompletion import *
from .history import *
from .key_bindings import *
from .lexer import *
from ..dimensions import Dsl, USER_HISTORY_FILE, USER_JSON_OUTPUTS_DIR

#
#
# DIMENSIONS QUERY AND DATA HANDLING
#
#


class DslResultsBuffer(object):
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


def preview_content(jsondata, maxitems=10):
    """
    Preview items in console
    If it's one of the main sources, try to show title/id. Otherwise show json in one line
    """
    counter = 0
    for key in jsondata.keys():
        if key == "_stats":
            pass
        else:
            for row in jsondata[key]:
                counter += 1
                if counter <= maxitems:
                    try:  # title and url/id if object has them
                        url = get_dimensions_url(row['id'], key) or row['id']
                        click.echo(
                            click.style("[" + str(counter) + "] ", dim=True) +
                            click.style(row['title'].strip(), bold=True) +
                            click.style(" (id: " + url + " )", fg='blue'))

                    except:  # fallback: full row
                        click.echo(
                            click.style("[" + str(counter) + "] ", dim=True) +
                            click.style(str(row), bold=True))


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
        click.secho("Showing first 10 records from latest query..", dim=True)
        preview_content(jsondata, maxitems=10)


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
            if "query" in res["errors"]:
                print(res["errors"]["query"]["header"])
                for key in res["errors"]["query"]["details"]:
                    print(key)
            else:
                print(res["errors"])

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

    click.secho("Welcome! Please enter your query below.")
    click.secho(
        "Tab = suggest , Ctrl-c = abort query , Ctrl-d = exit , Ctrl-o = search docs",
        dim=True)

    # history
    session = PromptSession(history=SelectiveFileHistory(USER_HISTORY_FILE))

    databuffer = DslResultsBuffer()

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
