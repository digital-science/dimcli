#!/usr/bin/python
# -*- coding: utf-8 -*-

from prompt_toolkit.history import FileHistory

#
#
# HISTORY
#
#


class SelectiveFileHistory(FileHistory):
    """
    :class:`.SelectiveFileHistory` class that extends history but stores only queries 
     - strings starting with 'search' 
    NOTE This approach can be refined in the future
    """

    def __init__(self, filename):
        self.filename = filename
        super(SelectiveFileHistory, self).__init__(filename)

    def append_string(self, string):
        " Add string to the history only if it is a DSL search statement "
        if string.startswith("search"):
            self._loaded_strings.append(string)
            self.store_string(string)
