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

            .text-created {
                color: darkred;
            }
            .text-endpoint {
                color: crimson;
            }

        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.14.2/styles/default.min.css" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.14.2/highlight.min.js"></script>
        <script>hljs.initHighlightingOnLoad();</script>
    </head>
    <div>
        <div id="title">
            <h1>Dimensions API Export</h1>
            <hr>
            <p>Created on: <span class="text-created">%s</span> <br />
            API Endpoint: <span class="text-endpoint">%s</span></p>
            <hr>
        </div>      
        <div id="query">
            <h2>DSL Query:</h2>
            <p class="query">%s</p></API>
        </div>
        <h3>JSON Results:</h3>
        <a name="json">
        <div id="code"></a><pre><code>%s</code></pre>
        </div> 
        <div id="footer">
            <hr>
            <p>Generated with <a href="https://github.com/digital-science/dimcli">DimCli</a> %s | See also: <a href="https://docs.dimensions.ai/dsl/">https://docs.dimensions.ai/dsl/</a></p>
        </div>
    </body>
    </html>
    
    """ % ( this_time, api_endpoint,
            query.replace("search", "<b><i>search</i></b>").replace("return", "<b><i>return</i></b>"), 
            formatted_json , 
            VERSION)
    return s


