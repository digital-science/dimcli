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


class DataBuffer(object):
    current_json = ""

    def load(self, _json):
        self.current_json = _json

    def return_json(self):
        return self.current_json


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


def handle_query(CLIENT, text, databuffer):
    # @TODO query dimensions and open up a webpage

    if text.replace("\n", "").strip() == "show":
        res = databuffer.return_json()
        if res:
            formatted_json = json.dumps(res, indent=4, sort_keys=True)
            # print(formatted_json)
            # import webbrowser
            # webbrowser.open("http://jsoneditoronline.org?json=%s" % res)
            from pygments import highlight, lexers, formatters
            colorful_json = highlight(formatted_json, lexers.JsonLexer(),
                                      formatters.TerminalFormatter())
            print(colorful_json)
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
            databuffer.load(res)


#
#
# MAIN CLI
#
#


def main(credentials):
    click.secho(
        "Enter your query (TAB = suggest / Ctrl-C = abort query / Ctrl-D = exit / Ctrl-] = search docs) API: https://docs.dimensions.ai/dsl",
        dim=True)

    CLIENT = DimensionsClient(**credentials)

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
    credentials = get_credentials()
    main(credentials)
