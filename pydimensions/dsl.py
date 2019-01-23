#!/usr/bin/env python
"""
Autocompletion example.

Press [Tab] to complete the current word.
- The first Tab press fills in the common part of all completions
    and shows all the completions. (In the menu)
- Any following tab press cycles through all the possible completions.
"""
from __future__ import unicode_literals

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import Completion, Completer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt

#
# AUTO COMPLETION
#

# @TODO: smarter completer should keep into account previous words

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
            for keyword in dim_keywords + dim_entities:
                if keyword.startswith(word):
                    yield Completion(
                        keyword,
                        start_position=-len(word),
                        style='bg:ansiyellow fg:ansiblack')


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


class BasicValidator(Validator):
    def validate(self, document):
        text = document.text

        if text and "return" not in text:
            # i = 0
            # # Get index of fist non numeric character.
            # # We want to move the cursor here.
            # for i, c in enumerate(text):
            #     if not c.isdigit():
            #         break

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
                return 'red'
            else:
                return 'black'

        def get_line(lineno):

            return [(get_class(w), w + " ")
                    for w in document.lines[lineno].split()]

        return get_line


#
#
# MAIN CLI
#
#


def main():
    text = prompt(
        'Enter your query (esc+enter=run):\n>',
        default="",  # you can pass a default text to begin with
        # completer=dim_completer,
        completer=CleverCompleter(),
        validator=BasicValidator(),
        validate_while_typing=False,
        multiline=True,
        complete_while_typing=False,
        lexer=BasicLexer(),
        key_bindings=kb)
    handle_query(text)


def handle_query(q):
    # @TODO query dimensions and open up a webpage
    print('You said: %s' % q)


if __name__ == '__main__':
    main()
