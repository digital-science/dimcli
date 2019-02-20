#!/usr/bin/python
# -*- coding: utf-8 -*-

import click
import json
import sys
import subprocess
import os

from .dsl_grammar import *


def is_quoted(w):
    if w[0] == '"' and w[-1] == '"':
        return True
    if w[0] == "'" and w[-1] == "'":
        return True
    return False


def line_last_word(line):
    if len(line) > 0:
        return line.split()[-1]
    else:
        return False


def line_search_subject(line):
    "get the source one searches for"
    l = line.split()
    if len(l) > 1 and "search" in l:
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


def save2File(contents, filename, path):
    if not os.path.exists(path):
        os.makedirs(path)
    filename = os.path.join(path, filename)
    f = open(filename, 'wb')
    f.write(contents.encode())  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it
    url = "file://" + filename
    return url


def html_template_interactive(query, formatted_json):
    """
    version that uses to open/close the json tree
    * https://github.com/caldwell/renderjson
    """
    s = """
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        .query {
            font-size: 20px;
            color: blue;
            font-family: monospace;
        }

        .renderjson {
                font-family: Monaco, "Bitstream Vera Sans Mono", "Lucida Console", Terminal;
                background: black;
                font-size: 14px;
        }

        .renderjson a              { text-decoration: none; }
        .renderjson .disclosure    { color: crimson;
                                    font-size: 150%%; }
        .renderjson .syntax        { color: grey; }
        .renderjson .string        { color: darkkhaki; }
        .renderjson .number        { color: cyan; }
        .renderjson .boolean       { color: plum; }
        .renderjson .key           { color: lightblue; }
        .renderjson .keyword       { color: lightgoldenrodyellow; }
        .renderjson .object.syntax { color: lightseagreen; }
        .renderjson .array.syntax  { color: lightsalmon; }
    </style>
    <script type="text/javascript" src="http://static.michelepasin.org/thirdparty/renderjson.js"></script>
    <script>    
    var data = %s;
    </script>
    </head>
    <body>Query:
        <p class="query">%s</p><hr>
        <code id="json_data"></code>
    
        <script> 
        renderjson.set_show_to_level(3);
        renderjson.set_sort_objects(true);
        document.getElementById("json_data").appendChild(renderjson(data)); 
        </script>
    </body>
    </html>
    
    """ % (formatted_json, query)
    return s


def html_template_version1(query, formatted_json):
    """
    this version just uses https://highlightjs.org/ to colorize the json code
    * 2019-02-07: 
    deprecated in favor of the interactive one above
    """

    s = """
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        .query {
            font-size: 20px;
            color: red;
            background: beige;
            font-family: monospace;
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.14.2/styles/default.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.14.2/highlight.min.js"></script>
    <script>hljs.initHighlightingOnLoad();</script>
    </head>
    <body>Query:<p class="query">%s</p><hr><pre><code>%s</code></pre></body>
    </html>
    
    """ % (query, formatted_json)
    return s


def open_multi_platform(fpath):
    """
    util to open a file on any platform (i hope)
    """
    if sys.platform == 'win32':
        subprocess.Popen(['start', fpath], shell=True)

    elif sys.platform == 'darwin':
        subprocess.Popen(['open', fpath])

    else:
        try:
            subprocess.Popen(['xdg-open', fpath])
        except OSError:
            print("Couldnt find suitable opener for %s" % fpath)