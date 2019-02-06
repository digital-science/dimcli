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

import click
import json
import sys
import os
import time
import webbrowser

from .dsl_grammar import *
from ..dimensions import Dsl, USER_JSON_OUTPUTS_DIR

#
# utils
#


def line_last_word(line):
    if len(line) > 0:
        return line.split()[-1]
    else:
        return False


def line_search_subject(line):
    "get the source one searches for"
    l = line.split()
    if "search" in l:
        i = l.index("search")
        return l[i + 1]
    else:
        return None


def line_lazy_return(text):
    "if return statement not included, add it lazily"
    if "return" not in text:
        source = line_search_subject(text)
        if source in VOCABULARY['sources'].keys():
            # click.secho("..inferring result statement", dim=True)
            return text.strip() + " return " + source
    return text


def _save2File(contents, filename, path):
    if not os.path.exists(path):
        os.makedirs(path)
    filename = os.path.join(path, filename)
    f = open(filename, 'wb')
    f.write(contents.encode())  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it
    url = "file://" + filename
    return url


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
            print('here')
            candidates = [x for x in VOCABULARY['lang'] if x != "search"]

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
            # if w in dim_lang_1:
            #     return "green bold"
            if w in VOCABULARY['lang']:
                return "green"
            elif w in VOCABULARY['sources'].keys():
                return "blue bold"
            elif w in VOCABULARY['sources']['publications']['fields']:
                return "blue"  # @TODO generalize
            # elif w in dim_entities_after_dot:
            #     return "violet"
            elif is_quoted(w):
                return "orange"
            elif w in VOCABULARY['allowed_starts']:
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
    b = event.app.current_DataBuffer
    if b.complete_state:
        b.complete_next()
    else:
        b.start_completion(select_first=False)


@bindings.add("c-]")
def _(event):
    """
    Look up in docs
    """
    line = event.app.current_DataBuffer.text
    if line:
        line_last_word = line.split()[-1]
        import webbrowser
        webbrowser.open("https://docs.dimensions.ai/dsl/search.html?q=" +
                        line_last_word)
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


class DataBuffer(object):
    current_json = ""
    current_query = ""

    def load(self, json_data, query):
        self.current_json = json_data
        self.current_query = query

    def retrieve(self):
        return (self.current_json, self.current_query)


def show_json(jjson, terminal=False):
    "print out json to the user"
    formatted_json = json.dumps(jjson, indent=4, sort_keys=True)
    if terminal:
        from pygments import highlight, lexers, formatters
        colorful_json = highlight(formatted_json, lexers.JsonLexer(),
                                  formatters.TerminalFormatter())
        print(colorful_json)
    else:
        contents = "<html><body><pre>%s</pre></body></html>" % formatted_json

        filename = time.strftime("%Y%m%d-%H%M%S.html")

        url = _save2File(contents, filename, USER_JSON_OUTPUTS_DIR)

        webbrowser.open(url)

        pass
    # print(formatted_json)
    # import webbrowser
    # webbrowser.open("http://jsoneditoronline.org?json=%s" % res)


def handle_query(CLIENT, text, databuffer):
    """main procedure after user input"""

    if text.replace("\n", "").strip() == "show":
        jsondata, query = databuffer.retrieve()
        if jsondata:
            show_json(jsondata)
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
    click.secho("Welcome!")
    click.secho("Please enter your query below.")
    click.secho(
        "TAB = suggest | Ctrl-C = abort query | Ctrl-D = exit | Ctrl-] = search docs (https://docs.dimensions.ai/dsl)",
        dim=True)

    CLIENT = Dsl(instance=instance, show_results=False, rich_display=False)

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
            handle_query(CLIENT, text, databuffer)
    print("GoodBye!")


if __name__ == "__main__":
    run()
