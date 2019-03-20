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



HELP_MESSAGE =  "HELP >>> Tab = suggest , Ctrl-c = abort query , Ctrl-d = exit , Ctrl-o = open online docs"


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


def print_json_full(jjson, query, terminal=False):
    "print out full json either as pretty_json or within an html template"
    formatted_json = json.dumps(jjson, indent=4, sort_keys=True)
    if terminal: # json_pretty
        from pygments import highlight, lexers, formatters
        colorful_json = highlight(formatted_json, lexers.JsonLexer(),
                                  formatters.TerminalFormatter())
        print(colorful_json)
    else: # json_html
        contents = html_template_interactive(query, formatted_json)

        filename = time.strftime("%Y%m%d-%H%M%S.html")

        url = save2File(contents, filename, USER_JSON_OUTPUTS_DIR)

        webbrowser.open(url)


def print_json_compact(jsondata):
    """
    Show json in one line
    NOTE: the logic is the same as the except clause in print_json_preview. Maybe some refactoring could be beneficial here..
    """
    counter = 0
    for key in jsondata.keys():
        if key == "_stats":
            pass
        else:
            for row in jsondata[key]:
                counter += 1
                # full row
                click.echo(
                    click.style("[" + str(counter) + "] ", dim=True) +
                    click.style(str(row)))

def print_smart_preview(jsondata, maxitems=10):
    """
    Preview items in console
    If it's one of the main sources, try to show title/id. Otherwise show json in one line
    """
    # click.secho("Showing first %d records from latest query.." % maxitems, dim=True)
    # click.secho("")
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
                        if 'title' in row.keys():
                            name_or_title = row['title'].strip()
                        else:
                            name_or_title = row['first_name'] + " " + row['last_name']
                        click.echo(
                            click.style("[" + str(counter) + "] ", dim=True) +
                            click.style(name_or_title , bold=True) +
                            click.style(" (id: " + url + " )", fg='blue'))

                    except:  # fallback: full row
                        click.echo(
                            click.style("[" + str(counter) + "] ", dim=True) +
                            click.style(str(row)))
            click.secho("---", dim=True)
            click.secho("Tip: use 'show <number>' or show+Tab to see more options", dim=True)



def show_command(text, databuffer):
    """
    show results of a query
    """
    text = text.replace("show", "").strip()

    jsondata, query = databuffer.retrieve()
    if not jsondata:
        print("Nothing to show - please run a search first.")
        return
    # cases
    if text == "json_html":
        print_json_full(jsondata, query, terminal=False)

    elif text == "json_pretty":
        print_json_full(jsondata, query, terminal=True)

    elif text == "json_compact":
        print_json_compact(jsondata)

    else:
        try:
            slice_no = int(text)
        except ValueError:
            slice_no = 10
            
        print_smart_preview(jsondata, maxitems=slice_no)



def handle_query(CLIENT, text, databuffer):
    """main procedure after user input"""

    if text.replace("\n", "").strip().startswith("show"):
        show_command(text.replace("\n", "").strip(), databuffer)

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
            databuffer.load(res.data, text)
            click.secho("---", dim=True)
            print_json_full(res.data, text, terminal=True)
        else:
            if res['stats']:
                print("Tot Results: ", res['stats']["total_count"])
            for k in res.data.keys():
                if k != "_stats":
                    print(k.capitalize() + ":", len(res.data[k]))
            databuffer.load(res.data, text)
            if True:
                click.secho("---", dim=True)
                print_smart_preview(res.data, maxitems=5)


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
