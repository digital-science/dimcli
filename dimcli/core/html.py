#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..VERSION import VERSION

def html_template_interactive(query, formatted_json):
    """
    version that uses to open/close the json tree
    * https://github.com/caldwell/renderjson

    TIP: '%' chars need to be escaped as '%%'
    """
    s = """

        <html>
        <head>
        <title>DSL Query Output</title>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <style type="text/css">
            html,body{margin:0;padding:0}
            body{font: 76%% arial,sans-serif}
            a{color: lightgray;}
            p{margin:0 10px 10px}
            div#header h1{height:80px;line-height:80px;margin:0;
                padding-left:10px;background: #EEE;color: #79B30B}
            div#content p{line-height:1.4}
            div#navigation{background:#B9CAFF}
            div#extra{background:#FF8539}
            div#footer{background: #333;color: #FFF}
            div#footer p{margin:0;padding:5px 10px}
            div#wrapper{float:left;width:100%%}
            div#content{margin-left:300px}
            div#navigation{float:left;width:300px;margin-left:-100%%}
            div#extra{clear:left;width:100%%}
            
            .query {color: black; font-family: monospace; font-size: 15px;}
            .renderjson {
                    // font-family: Monaco, "Bitstream Vera Sans Mono", "Lucida Console", Terminal;
                    font-family: monospace;
                    background: midnightblue;
                    margin: 0px;
                    font-size: 12px;
            }
            .renderjson a              { text-decoration: none; }
            .renderjson .disclosure    { color: crimson; font-size: 150%%; }
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
        <script>var data = %s;</script>
        </head>
        <body>
            <div id="container">
            <div id="header"><h1>Dimensions DSL Query Results</h1></div>
            <div id="wrapper">
            <div id="content">
                <code id="json_data"></code>
            </div>
            </div>
            <div id="navigation">
                <p><strong>Query:</strong></p>
                <p class="query">$ %s</p></p>
            </div>
            <div id="extra">
            </div>
            <div id="footer"><p>Generated with <a href="https://github.com/lambdamusic/dimcli">DimCli</a> %s</p></div>
            </div>
            <script> 
            renderjson.set_show_to_level(3);
            renderjson.set_sort_objects(true);
            document.getElementById("json_data").appendChild(renderjson(data)); 
            </script>
        </body>
        </html>
    
    """ % (formatted_json, query, VERSION)
    return s



def _html_template_interactive(query, formatted_json):
    """
    version that uses to open/close the json tree
    * https://github.com/caldwell/renderjson

    TIP: '%' chars need to be escaped as '%%'
    """
    s = """
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        body {
            background: antiquewhite;
        }
        .left {
            width: 30%%;
         }
        .right {
            width: 70%%;
         }
        .title {
            color: grey;
        }
        .query {
            font-size: 19px;
            color: black;
            font-family: monospace;
        }

        .renderjson {
                // font-family: Monaco, "Bitstream Vera Sans Mono", "Lucida Console", Terminal;
                font-family: monospace;
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
    <body>
        <div class="left">
         <span class="title">Dimensions DSL query:</span>
        <p class="query">$ %s</p><hr>
        </div>
        
        <div class="right">
            <code id="json_data">%s</code>
        </div>
        <script> 
        //renderjson.set_show_to_level(3);
        //renderjson.set_sort_objects(true);
        //document.getElementById("json_data").appendChild(renderjson(data)); 
        </script>
    </body>
    </html>
    
    """ % (formatted_json, query, formatted_json)
    return s


def xxx_html_template_interactive(query, formatted_json):
    """
    version that uses to open/close the json tree
    * https://github.com/caldwell/renderjson
    """
    s = """
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        body {
            background: antiquewhite;
        }
        .title {
            color: grey;
        }
        .query {
            font-size: 19px;
            color: darkgoldenrod;
            font-family: monospace;
        }

        .renderjson {
                // font-family: Monaco, "Bitstream Vera Sans Mono", "Lucida Console", Terminal;
                font-family: monospace;
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
    <body><span class="title">Dimensions DSL query:</span>
        <p class="query">$ %s</p><hr>
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
    * 2019-02-07: deprecated in favor of the interactive one above
    
    This version just uses https://highlightjs.org/ to colorize the json code
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

