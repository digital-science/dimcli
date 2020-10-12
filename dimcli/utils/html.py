#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..VERSION import VERSION
import time
# from json2html import *


def html_template_interactive(query, formatted_json, api_endpoint):
    """
    This version just uses https://highlightjs.org/ to colorize the json code
    """

    this_time = time.strftime("%Y-%m-%d  at %H:%M:%S")

    s = """
    <html>
    <head>
        <title>Dimensions API Query Output</title>
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

            .export-created {
                font-size: 14px;
                font-weight: normal;
                color: gray;
            }


        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.14.2/styles/default.min.css" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.14.2/highlight.min.js"></script>
        <script>hljs.initHighlightingOnLoad();</script>
    </head>
    <div>
        <div id="title">
            <h1>Dimensions API Export
                <span class="export-created">Created on: %s using the API endpoint: <a href="%s" target="_blank">%s</a></span>
            </h1>
            <hr>
        </div>      
        <div id="query">
            <h2>DSL Query:</h2>
            <p class="query">%s</p></API>
            
        </div>
        <hr>
        <h3>JSON Results:</h3>
        <a name="json">
        <div id="code"></a><pre><code>%s</code></pre>
        </div> 
        <div id="footer">
            <hr>
            <p>Generated with <a href="https://github.com/digital-science/dimcli">Dimcli</a> %s | See also: <a href="https://docs.dimensions.ai/dsl/">https://docs.dimensions.ai/dsl/</a></p>
        </div>
    </body>
    </html>
    
    """ % ( this_time, api_endpoint, api_endpoint,
            query.replace("search", "<b><i>search</i></b>").replace("return", "<b><i>return</i></b>"), 
            formatted_json , 
            VERSION)
    return s


