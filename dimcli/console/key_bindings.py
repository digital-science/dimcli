#!/usr/bin/python
# -*- coding: utf-8 -*-

from prompt_toolkit.key_binding import KeyBindings

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
        line_last_word = line.split()[-1]
        import webbrowser
        webbrowser.open("https://docs.dimensions.ai/dsl/search.html?q=" +
                        line_last_word)
    return
