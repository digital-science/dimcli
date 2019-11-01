#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..VERSION import VERSION
# from json2html import *


def html_template_interactive(query, formatted_json):
    """
    This version just uses https://highlightjs.org/ to colorize the json code
    """

    # table = json2html.convert(json = formatted_json)

    s = """
    <html>
    <head>
        <title>DSL Query Output</title>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <style>
            .query {
                font-size: 20px;
                padding: 50px;
                margin-bottom: 30px;
                color: #f0f0f0;
                background: #2a6683;
                font-family: monospace;
            }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.14.2/styles/default.min.css" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.14.2/highlight.min.js"></script>
        <script>hljs.initHighlightingOnLoad();</script>
    </head>
    <div>
        <div id="header"><h1>Dimensions DSL Results for Query:&nbsp;</h1></div>
        <div id="query">
            <p class="query">%s</p></p>
        </div>
        <h3>Results: JSON</h3>
        <a name="json">
        <div id="code"></a><pre><code>%s</code></pre>
        </div> 
        <div id="footer">
            <hr>
            <p>Generated with <a href="https://github.com/digital-science/dimcli">DimCli</a> %s</p>
        </div>
    </body>
    </html>
    
    """ % (query.replace("search", "<b><i>search</i></b>").replace("return", "<b><i>return</i></b>"), formatted_json , VERSION)
    return s


