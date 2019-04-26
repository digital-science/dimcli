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
import requests

from ..core.api import Dsl, USER_HISTORY_FILE, USER_JSON_OUTPUTS_DIR
from ..core.dsl_grammar import *
from ..core.utils import *

from .autocompletion import *
from .history import *
from .key_bindings import *
from .lexer import *




HELP_MESSAGE =  """DIMCLI COMMANDS HELP \n>>> Tab:  autocomplete command. \n>>> Ctrl-o: search docs online. \n>>> show: pretty-print results from recent query. Number of results can be customized by adding a number e.g. `show 10`.\n>>> show json_compact: print our results of recent query as single-line JSON. \n>>> export_html: saves results from recent query as HTML page. \n>>> export_csv: saves results from recent query as CSV file.  \n>>> Ctrl-c: abort query.\n>>> Ctrl-d or quit: exit console."""


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


def show_command(text, databuffer):
    """
    show results of a query
    """
    text = text.replace("show", "").strip()

    if databuffer: 
        jsondata, query = databuffer.retrieve()
    else:
        jsondata, query = None, None
    if not jsondata:
        print("Nothing to show - please run a search first.")
        return
    # cases
    if text == "json_compact":
        print_json_compact(jsondata)

    else:
        try:
            slice_no = int(text)
        except ValueError:
            slice_no = 10
            
        print_smart_preview(jsondata, maxitems=slice_no)



def export_command(text, databuffer):
    """
    save results of a query to a file
    """
    if databuffer: 
        jsondata, query = databuffer.retrieve()
    else:
        jsondata, query = None, None
    if not jsondata:
        print("Nothing to export - please run a search first.")
        return
    # cases
    if text == "export_html":
        export_json_html(jsondata, query, USER_JSON_OUTPUTS_DIR)

    elif text == "export_csv":
        export_json_csv(jsondata, query, USER_JSON_OUTPUTS_DIR)




def handle_query(CLIENT, text, databuffer):
    """main procedure after user input"""

    if text.replace("\n", "").strip().startswith("show"):
        show_command(text.replace("\n", "").strip(), databuffer)

    elif text.replace("\n", "").strip().startswith("export"):
        export_command(text.replace("\n", "").strip(), databuffer)

    else:
        # lazy complete
        text = line_add_lazy_return(text)
        text = line_add_lazy_describe(text)
        click.secho("You said: %s" % text, fg="black", dim=True)
        # RUN QUERY
        res = CLIENT.query(text)
        # #
        if "errors" in res.data.keys():
            if "query" in res.data["errors"]:
                print(res.data["errors"]["query"]["header"])
                for key in res.data["errors"]["query"]["details"]:
                    print(key)
            else:
                print(res.data["errors"])
        elif text.strip().startswith("describe"):
            if databuffer: databuffer.load(res.data, text)
            click.secho("---", dim=True)
            print_json_full(res.data, text, terminal=True)
        else:
            print_json_summary(res, text)
            # if res['stats']:
            #     print("Tot Results: ", res['stats']["total_count"])
            # for k in res.data.keys():
            #     if k != "_stats":
            #         print(k.capitalize() + ":", len(res.data[k]))
            if databuffer: databuffer.load(res.data, text)
            if True:
                click.secho("---", dim=True)
                print_smart_preview(res.data, maxitems=5)
            return res  # 2019-03-31


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
        CLIENT = Dsl(instance=instance, show_results=False)
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)
        # if err.response.status_code == 401:
        #     print("here")

    click.secho("Welcome! Type 'help' for more info. Ready to query endpoint: %s" % CLIENT._url)

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
                complete_style=CompleteStyle.MULTI_COLUMN,
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
        except Exception as e:
            print(e)
            sys.exit(0)  
        else:
            if text.strip() == "":
                continue
            elif text == "quit":
                break
            elif text == "help":
                click.secho(HELP_MESSAGE, dim=True)
                continue
            try:
                handle_query(CLIENT, text, databuffer)
            except Exception as e:
                print(e)
                continue
    print("GoodBye!")


if __name__ == "__main__":
    run()
