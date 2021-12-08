#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Dimcli utilities for the REPL feature and for parsing DSL queries. 
"""

import click
import time
import json
import sys
import subprocess
import os
import re
import webbrowser
import textwrap
from itertools import islice
from pandas import DataFrame
try:
    from pandas import json_normalize
except:
    from pandas.io.json import json_normalize

from ..core.dsl_grammar import *
from ..core.auth import USER_HISTORY_FILE
from ..VERSION import VERSION
from .html import html_template_interactive
from .dim_utils import *
from .misc_utils import *
from .gists_utils import GistsHelper
from ..repl.history import *

def listify_and_unify(*args):
    "util to handle listing together dict.keys() sequences"
    out = []
    for x in args:
        if type(x) == list:
            out += x
        else:
            out += list(x)
    return sorted(list(set(out)))


def split_multi_words(llist):
    "break down a list of strings so that it is composed of only 1-word elements"
    broken = [x.split() for x in llist] 
    return list_flatten(broken)

def list_flatten(llist):
    return [item for sublist in llist for item in sublist]

def is_single_word_quoted(w):
    if w[0] == '"' and w[-1] == '"':
        return True
    if w[0] == "'" and w[-1] == "'":
        return True
    return False


def line_last_word(line):
    "return last word"
    if len(line.split()) > 0:
        return line.split()[-1]
    else:
        return ""


def line_last_two_words(line):
    "return last two words"
    if len(line.split()) > 1:
        return " ".join([line.split()[-2], line.split()[-1]])
    else:
        return ""

def line_last_three_words(line):
    "return last three words"
    if len(line.split()) > 2:
        return " ".join([line.split()[-3], line.split()[-2], line.split()[-1]])
    else:
        return ""

def in_square_brackets(line):
    "if we are within the square brackets eg we have a valid 'return <source>[this+that - that' statement"
    if line:
        if line[-1] == "[":
            return True
        else:
            found_opening = False
            for el in reversed(line.split()):
                if "]" in el: 
                    return False
                if "[" in el:
                    found_opening = True
                if el == "return" and found_opening:
                    return True
    return False

def in_categories_search(line):
    """if we are within the `category.name="` bit... """
    pattern = ".name=\""
    if line:
        if line.endswith(pattern):
            for x in G.categories():
                # print("\ntesting", x, "**"+test)
                if line.endswith(x+pattern):
                    # print("found", x)
                    return x
    return False


def remove_fulltext_search_clause(line):
    """Strips out the content in quotes in a DSL query.

    Helper to avoid situations when full-text contents interfere with DSL keywords (eg limit or return)

    TODO dbcheck where to use this method in `line_..` helpers.
    
    Example
    --------

        a = 'search grants in title_abstract_only for "Heisenberg limit " return grants[id]'
        re.sub(r'\"(.+?)\"', "", a)
        # => 'search grants in title_abstract_only for return grants[id]'

    TODO fails with inner escaped quotes 
        a = 'search grants in title_abstract_only for "Heisenberg limit " and for "\"b\" return c" return grants[id]'
        re.sub(r'\"(.+?)\"', "", a)
        # => 'search grants in title_abstract_only for  and for  return c" return grants[id]'

    """
    return re.sub(r'\"(.+?)\"', "", line)


def line_count_returns(line):
    "check how many returns we have in the query"
    text = remove_fulltext_search_clause(line)
    return text.split().count('return')


def line_has_limit_or_skip(line):
    "check if there is a limit or skip statement"
    if "return" in line:
        pos = line.rindex("return") # last position right side
        if "limit" in line[pos:] or "skip" in line[pos:]:
            return True


def line_last_return_subject(line):
    "get the last 'return <object>' statement "
    lista = list(reversed(line.split()))
    # print(lista)
    if len(lista) > 1:
        for el in lista:
            if "return" in el:
                s = lista[lista.index('return') - 1]
                # print(s)
                return s.split("[")[0]


def line_search_subject_is_valid(line):
    "if we have a valid 'search <source>' statement"
    if len(line.split()) == 2 and line.split()[1] in G.sources():
        return True
    else:
        return False

def line_return_subject_is_valid(line):
    "if we have a valid 'return <object>' statement PS not checking if object is semantically valid"
    l = line.split()
    if len(l) > 1:
        if l[-2] == "return":
            return True 

def line_filter_is_partial(line):
    "return one of the valid filter operators after a partial `where -filter-` statement"
    l = line.split()
    if len(l) > 1:
        if l[-2] == "where":
            return True     


def line_filter_is_complete(line):
    "if the filter statement (after where) is fully specified eg `where FOR = '123'` or `where doi!='123'` "
    # @TODO REVIEW
    l = line.split('where')
    if len(l) > 1 and l[-1].strip():
        if 'is empty' in l[-1] or 'is not empty' in l[-1]:
            return True
        else:
            for x in G.lang_filter_operators():
                if x in l[-1]:
                    after_filter = l[-1].split(x) # => [' doi ', ' 123  '] from ' doi = 123  '
                    if len(after_filter) > 1 and after_filter[-1].strip():
                        return True


def line_for_text_search_inner(line):
    "return one of the valid text search operators if inside a `for '...'` statement"
    l = line.split("for")
    if len(l) > 1 and l[-1].strip():
        if l[-1].count("\"") == 1:
            return True

def line_for_text_is_complete(line):
    "if the 'for' text search statement is complete"
    l = line.split("for")
    if len(l) > 1 and l[-1].strip():
        if l[-1].count("\"") > 1 and l[-1].strip()[-1] == "\"":
            return True

def line_is_search_query(line):
    "checks if it is a `search` query"
    l = line.strip().split()
    if len(l) > 1 and l[0] ==  "search":
        return True
    else:
        return False 


def line_search_subject(line):
    "get the source name being searched for"
    l = line.split()
    if len(l) > 1 and "search" in l[:4]:
        i = l.index("search")
        return l[i + 1]
    else:
        return ""


def line_search_unnest(line):
    "verify if query contains an unnest statement"
    if "unnest" in line:
        return True

def line_search_return(line):
    """
    get the source/facet in the return statement
    """
    l = line.split()
    n = l.count("return")
    if n == 1:
        i = l.index("return")
        if len(l) > i + 1: # cause index is zero based
            return_obj = l[i + 1]
            if "[" in return_obj:
                return return_obj.split('[')[0]
            else:
                return return_obj
    else: # if multiple return values, fail
        return None

def line_search_aggregates(line):
    """get the aggregrates statement eg in 
        `search publications return funders aggregate altmetric_median sort by altmetric_median`
        @TODO handle multiple aggregrate statements eg
        `return research_orgs aggregate altmetric_median, rcr_avg sort by rcr_avg`
    """
    l = line.split()
    n = l.count("aggregate")
    if n == 1:
        i = l.index("aggregate")
        if len(l) > i + 2: # cause index is zero based
            return l[i + 1]
    else:
        return None

def line_add_lazy_return(text):
    "if return statement not included, add it lazily"
    if "return" not in text:
        source = line_search_subject(text)
        if source in G.sources():
            # click.secho("..inferring result statement", dim=True)
            return text.strip() + " return " + source
    return text

def line_add_lazy_describe(line):
    "if describe has no arguments, default silently to <describe version>"
    l = line.split()
    if "describe" in line and len(l) == 1:
        return "describe version"
    return line



def print_warning_prompt_version():
    try:
        from prompt_toolkit import __version__ as prompt_toolkit_version
    except:
        prompt_toolkit_version = "unknown"
    click.secho("WARNING: Dimcli console requires prompt-toolkit version >=2. You are running version '%s'.\nYou can still use Dimcli as Python library. Or upgrade the dependencies with `pip install ipython prompt-toolkit -U" % prompt_toolkit_version,  fg="red")



def preview_contents(fpath):
    """print out the contents of the local settings file in the terminal """
    try:
        with open(fpath) as f:
            print(f.read())
    except:
        print("An unknown error occured..")
    click.secho("---\nFile: {}".format(fpath), bold=True)


def init_config_folder(user_dir, user_config_file):
    """
    Create the config folder/file unless existing. If it exists, backup and create new one.
    # TODO: update so that it can take KEY based authentication too. 
    # For now it has to be edited manually. 
    """
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
        # click.secho("Created %s" % user_dir, dim=True)
    if os.path.exists(user_config_file):
        click.secho("Looks like you have already setup a config file: `%s`." % user_config_file, fg="red")
        if click.confirm("Overwrite?"):
            pass
        else:
            click.secho("Goodbye")
            return False

    instance = "[instance.live]" # default for main instance
    url = click.prompt('Please enter the API URL or leave blank for default', default="https://app.dimensions.ai")
    login, password, key = "", "", ""
    if click.confirm('Do you have an API key?'):
        key = click.prompt('Please enter your key', hide_input=True, confirmation_prompt=True)
    else:
        login = click.prompt('Please enter your username')
        password = click.prompt('Please enter your password', hide_input=True, confirmation_prompt=True)
        

    f= open(user_config_file,"w+")
    f.write(instance + "\n")
    f.write("url=" + url + "\n")
    f.write("login=" + login + "\n")
    f.write("password=" + password + "\n")
    f.write("key=" + key + "\n")
    f.close()
    click.secho(
        "Created %s" % user_config_file, dim=True
    )



def init_exports_folder(export_dir):
    """
    Create the folder where json and csv exports are stored
    """
    if not os.path.exists(export_dir):
        os.mkdir(export_dir)




def export_json_csv(jjson, query, USER_EXPORTS_DIR):
    """Export to a CSV"""
    return_object = line_search_return(query)
    try:
        df =  json_normalize(jjson[return_object], errors="ignore")
    except:
        df =  json_normalize(jjson, errors="ignore")
    filename = time.strftime("dsl_export_%Y%m%d-%H%M%S.csv")
    url = save2File(df.to_csv(), filename, USER_EXPORTS_DIR)
    webbrowser.open(url)
    # df.to_csv(USER_EXPORTS_DIR + filename)
    print("Exported: ", "%s%s" % (USER_EXPORTS_DIR, filename))



def export_json_html(jjson, query, api_endpoint, USER_EXPORTS_DIR):
    "print out full json either as pretty_json or within an html template"
    formatted_json = json.dumps(jjson, indent=4, sort_keys=True)
    contents = html_template_interactive(query, formatted_json, api_endpoint)
    filename = time.strftime("%Y%m%d-%H%M%S.html")
    url = save2File(contents, filename, USER_EXPORTS_DIR)
    webbrowser.open(url)
    print("Exported: ", "%s%s" % (USER_EXPORTS_DIR, filename))


def export_json_json(jjson, query, USER_EXPORTS_DIR):
    """Export to a json file
    """
    formatted_json = json.dumps(jjson, indent=4, sort_keys=True)
    filename = time.strftime("dsl_export_%Y%m%d-%H%M%S.json")
    url = save2File(formatted_json, filename, USER_EXPORTS_DIR)
    webbrowser.open(url)
    # df.to_csv(USER_EXPORTS_DIR + filename)
    print("Exported: ", "%s%s" % (USER_EXPORTS_DIR, filename))


def export_as_gsheets_wrapper(jjson, query):
    """Export to a json file
    """
    try:
        url = export_as_gsheets(jjson, query)
        print("Exported: ", "%s" % (url))
    except:
        print("Export failed")



def export_gist(jjson, query, api_endpoint):
    """Export as a github gist

    This generated a header file in markdown, a JSON file and also a CSV export.
    """


    nicetime = time.strftime("%Y-%m-%d %H:%M:%S")
    f1 = time.strftime("dimcli_export_%Y%m%d-%H%M%S")
    f2 = time.strftime("dimcli_results_%Y%m%d-%H%M%S")

    gist_desc = time.strftime(f"Dimensions API export {nicetime}")

    gist_readme_filename = "1-"+f1+".md"
    csv_filename = "2-"+f2+".csv"
    formatted_json_filename = "3-"+f2+".json"

    return_object = line_search_return(query)
    try:
        df =  json_normalize(jjson[return_object], errors="ignore")
        df_size = f"""=> records returned: {len(df)}"""
    except:
        df =  json_normalize(jjson, errors="ignore")
        df_size = ""  # fail silently if multiple return statemets

    gist_readme_contents = f"""## DSL: {textwrap.shorten(query, 70)}
    \nFull [DSL](https://docs.dimensions.ai/dsl) query:
    \n```
    \n{query}
    \n```
    \n 
    \n{df_size}
    \n
    \n
    \n---
    \nExport created on `{nicetime}` with [Dimcli](https://digital-science.github.io/dimcli/index.html) `{VERSION}`. 
    \nDimensions [API](https://www.dimensions.ai/dimensions-apis/) endpoint: `{api_endpoint}`.
    """

    # create JSON
    formatted_json_contents = json.dumps(jjson, indent=4, sort_keys=True)

    # create CSV
    return_object = line_search_return(query)
    try:
        df =  json_normalize(jjson[return_object], errors="ignore")
    except:
        df =  json_normalize(jjson, errors="ignore")
    csv_contents = df.to_csv()


    files_details =  {gist_readme_filename: {
                        "content": gist_readme_contents   
                        },
                      formatted_json_filename : {
                        "content": formatted_json_contents   
                        },
                      csv_filename : {
                        "content": csv_contents   
                        }
                      }  

    g = GistsHelper()
    url = g.save_gist(gist_desc, files_details)

    webbrowser.open(url)

    print("Exported: " + url)








def export_as_bar_chart(jjson, query, USER_EXPORTS_DIR):
    """
    requires the plotly library, which is not installed by default

    """

    try:
        import plotly.express as px
        from plotly.offline import plot
    except:
        click.secho("This feature requires the plotly library (`pip install plotly` from the terminal)", fg="red")
        return

    return_object = line_search_return(query)
    
    try:
        df =  json_normalize(jjson[return_object], errors="ignore")
    except:
        df =  json_normalize(jjson, errors="ignore")

    REQUIRED = ["id", "count"]
    for x in REQUIRED:
        if x not in df.columns:
            raise Exception(f"This method requires records to have the keys: {REQUIRED}. It is normally used with facets. Key [{x}] not found.")

    if "title" in df.columns:
        df["value"] = df["id"].astype(str) + df["title"]
    elif "name" in df.columns:
        df["value"] = df["id"].astype(str) + df["name"]
    elif "first_name" in df.columns and "last_name" in df.columns:
        df["value"] = df["id"].astype(str) + df["first_name"] + df["last_name"]
    else: 
        df["value"] = df["id"].astype(str)

    if "country_name" in df.columns:
        color_field = "country_name"
    # if "current_research_org" in df.columns:
    #     color_field = "current_research_org" 
    else:
        color_field = "count"
    
    newplot = px.bar(df, x="value", y="count", title=query, color=color_field)

    filename = time.strftime("dsl_plot_export_%Y%m%d-%H%M%S.html")
    plot(newplot, filename = USER_EXPORTS_DIR+filename, auto_open=True)

    print("Exported: ", "%s%s" % (USER_EXPORTS_DIR, filename))




def export_as_jupyter(jjson, query, USER_EXPORTS_DIR, num_rows_history=5):
    """EXPERIMENTAL FEATURE
    Take the last 5 rows from the history, and create a new python notebook with them. 
    Saves in usual location.

    For the most recent query, the data results are also saved as a static JSON cell.

    Based on https://gist.github.com/fperez/9716279

    TODO: expand so that more than one row is taken
    """

    try:
        from itertools import islice
        import subprocess
        import nbformat as nbf
    except:
        click.secho("This feature requires the nbformat library (`pip install nbformat` from the terminal)", fg="red")
        return

    history=SelectiveFileHistory(USER_HISTORY_FILE)

    rows_data = []
    try:
        for item in islice(history.load_history_strings(), num_rows_history+1):
            # remove latest query cause we deal with it below
            if item != query:
                rows_data += [item]
        rows_data.reverse()
    except:
        # if history is not available, fail silently
        pass
    
    nb = nbf.v4.new_notebook()
    this_time = time.strftime("%Y.%m.%d h%H:%M:%S")

    text = f"""# Dimensions API Queries Export\n### {this_time} \nThis notebook was generated using [Dimcli](https://github.com/digital-science/dimcli/) - the Dimensions API CLI."""

    nb['cells'] = [nbf.v4.new_markdown_cell(text)]

    setup = """!pip install dimcli -U --quiet\nimport dimcli\ndimcli.login()"""
    nb['cells'] += [nbf.v4.new_code_cell(setup)]

    # add history
    for code in rows_data:
        nb['cells'] += [nbf.v4.new_code_cell("%%dsl\n" + code)]

    # the very last query
    nb['cells'] += [nbf.v4.new_code_cell("%%dsl\n" + query)]
    formatted_json = json.dumps(jjson, indent=4, sort_keys=True)
    results_preview = f"""### Precomputed Query Results: \n```\n{formatted_json}\n```"""
    nb['cells'] += [nbf.v4.new_markdown_cell(results_preview)]

    # save file now
    filename = time.strftime(f"dsl_export_%Y-%m-%d_%H-%M-%S.ipynb")
    nbf.write(nb, USER_EXPORTS_DIR + filename)
    
    subprocess.run(['open', USER_EXPORTS_DIR + filename], check=True)
    print("Exported: ", "%s%s" % (USER_EXPORTS_DIR, filename))





def print_json_stats(res, query="", elapsed=""):
    """
    from a dimcli.DslDataset object, print out basic stats
    * works only for 'search' types of query
    """
    # what is searched for
    source, tot = line_search_subject(query), None
    unnest_query = line_search_unnest(query)
    if source:
        if res['stats']:
            tot = res['stats']["total_count"]
        for k in res.good_data_keys():
            if tot and source == k:
                if not unnest_query:
                    print(f"Returned {source.capitalize()}: {len(res[source])} (total = {tot})")
                else:
                    print(f"Returned objects: {len(res[source])} (total {source}= {tot})")
            else:
                print(f"Returned {k.capitalize()}: {len(res[k])}")
        if elapsed:
            t = "%.2f" % elapsed
            click.secho(f"Time: {t}s", dim=True)



def print_json_errors(res):
    """
    from a dimcli.DslDataset object, print out an errors summary
    """
    if "errors" in res.json.keys():
        if "query" in res.json["errors"]:
            print(res.json["errors"]["query"]["header"].strip("\n"))
            for key in res.json["errors"]["query"]["details"]:
                print(key)
        else:
            print(res.json["errors"])

def print_json_warnings(res):
    """
    from a dimcli.DslDataset object, print out a warnings
    """
    if "_warnings" in res.json.keys():
        print("WARNINGS [{}]".format(len(res.json["_warnings"])))
        print("\n".join([s for s in res.json["_warnings"]]))



def preview_results(jsondata, maxitems=10):
    """
    Preview items in console
    If it's one of the main sources, try to show title/id. Otherwise show json in one line
    """
    # click.secho("Showing first %d records from latest query.." % maxitems, dim=True)
    # click.secho("")
    counter = 0
    for key in jsondata.keys():
        if key not in ["_stats", "_warnings", "_notes",  "_version", "_copyright"]:
            for row in jsondata[key]:
                counter += 1
                if counter <= maxitems:
                    try:  # title and url/id if object has them
                        url = dimensions_url(row['id'], key, verbose=False) or row['id']
                        if 'title' in row.keys(): # for docs
                            name_or_title = row['title'].strip()
                        elif 'name' in row.keys():  # for orgs
                            name_or_title = row['name'].strip()
                        else: # for researchers
                            name_or_title = row['first_name'] + " " + row['last_name']
                        click.echo(
                            click.style("[" + str(counter) + "] ", dim=True) +
                            click.style(name_or_title , bold=True) +
                            click.style(" (id: " + url + " )", fg='blue'))

                    except:  # fallback: full row
                        click.echo(
                            click.style("[" + str(counter) + "] ", dim=True) +
                            click.style(str(row)))
            if len(jsondata[key]) > maxitems:
                click.secho("---", dim=True)
                click.secho(f"Note: {maxitems} of {len(jsondata[key])} results shown. Use '.show <number>' to view more.", dim=True)



def print_json_compact(jsondata):
    """
    Show json in one line
    NOTE: the logic is the same as the except clause in print_json_preview. Maybe some refactoring could be beneficial here..
    """
    from pygments import highlight, lexers, formatters
    lexer = lexers.JsonLexer()
    formatter = formatters.TerminalFormatter()
    
    counter = 0
    skips = ["_warnings", "_notes", "_stats", "_version", "_copyright"]
    for key in jsondata.keys():
        if key in skips:
            pass
        else:
            for row in jsondata[key]:
                counter += 1
                # full row
                click.echo(
                    click.style("[" + str(counter) + "] ", dim=True) +
                    click.style(highlight(json.dumps(row, sort_keys=True).strip(), lexer, formatter).strip()))



def print_json_full(jsondata):
    """
    pretty print json 
    """
    formatted_json = json.dumps(jsondata, indent=4, sort_keys=True)
    from pygments import highlight, lexers, formatters
    colorful_json = highlight(formatted_json, lexers.JsonLexer(),
                                formatters.TerminalFormatter())
    print(colorful_json)



def print_dimensions_url(obj_id):
    "wrapper dimensions_url() - for use within the cli"
    url = dimensions_url(obj_id)
    if url:
        print("Got a match:")
        print(url)
    else:
        # in this case, it's a cltrial or patent
        print("Cannot resolve automatically. Maybe:")
        print(dimensions_url(obj_id, "patents"))
        print(dimensions_url(obj_id, "clinical_trials"))


