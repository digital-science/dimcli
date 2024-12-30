#!/usr/bin/python
# -*- coding: utf-8 -*-

from prompt_toolkit.history import FileHistory

from ..core.dsl_grammar import *

#
#
# HISTORY
#
#


class SelectiveFileHistory(FileHistory):
    """This class extends FileHistory, but stores only valid DSL queries 
     (dsl_grammar_extras.py > allowed_starts_dsl_query)
     
    NOTE This approach can be refined in the future
    """

    def __init__(self, filename):
        self.filename = filename
        # print("HISTORY: ", filename)
        super(SelectiveFileHistory, self).__init__(filename)

    def append_string(self, string: str) -> None:
        "DIMCLI override: add string to the history only if it is a valid DSL query"
        l = G.allowed_starts_dsl_query()
        if string.startswith(tuple(l)):
            self._loaded_strings.insert(0, string)
            self.store_string(string)

