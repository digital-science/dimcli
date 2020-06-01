#!/usr/bin/python
# -*- coding: utf-8 -*-

import click
import time
import json
import sys
import subprocess
import os
import webbrowser
from itertools import islice

from .dsl_grammar import *
from .html import html_template_interactive



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
    "get the source one searches for"
    l = line.split()
    if len(l) > 1 and "search" in l:
        i = l.index("search")
        return l[i + 1]
    else:
        return ""

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


def save2File(contents, filename, path):
    """Save string contents to a file.

    Not generalized much, so use at your own risk.

    Args:
        contents: string
        filename: string
        path: full valid path

    Returns:
        File location in URL format eg "file://..."
    """
    if not os.path.exists(path):
        os.makedirs(path)
    filename = os.path.join(path, filename)
    f = open(filename, 'wb')
    f.write(contents.encode())  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it
    url = "file://" + filename
    return url


def print_warning_prompt_version():
    try:
        from prompt_toolkit import __version__ as prompt_toolkit_version
    except:
        prompt_toolkit_version = "unknown"
    click.secho("WARNING: Dimcli console requires prompt-toolkit version >=2. You are running version '%s'.\nYou can still use Dimcli as Python library. Or upgrade the dependencies with `pip install ipython prompt-toolkit -U" % prompt_toolkit_version,  fg="red")




def open_multi_platform(fpath):
    """
    util to open a file on any platform (i hope)
    """
    click.secho("Opening `%s` ..." % fpath)
    if sys.platform == 'win32':
        subprocess.Popen(['start', fpath], shell=True)

    elif sys.platform == 'darwin':
        subprocess.Popen(['open', fpath])

    else:
        try:
            subprocess.Popen(['xdg-open', fpath])
        except OSError:
            print("Couldnt find suitable opener for %s" % fpath)


def preview_contents(fpath):
    click.secho("File: {}".format(fpath), bold=True)
    try:
        with open(fpath) as f:
            print(f.read())
    except:
        print("An unknown error occured..")


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


def chunks_of(data, size):
    """Splits up a list or sequence in to chunks of selected size. 

    Args:
        data: A sequence eg a list
        size: A number

    Returns:
        An iterable
    """
    it = iter(data)
    chunk = list(islice(it, size))
    while chunk:
        yield chunk
        chunk = list(islice(it, size))



def exists_key_in_dicts_list(dict_list, key):
    """From a list of dicts, checks if a certain key is in one of the dicts in the list.

    See also https://stackoverflow.com/questions/14790980/how-can-i-check-if-key-exists-in-list-of-dicts-in-python

    Args:
        dict_list: A list of dictionaries
        key: a string to be found in dict keys

    Returns:
        Dictionary or None
    """
    # return next((i for i,d in enumerate(dict_list) if key in d), None)
    return next((d for i,d in enumerate(dict_list) if key in d), None)



def normalize_key(key_name, dict_list, new_val=None):
    """Ensures the key always appear in a JSON dict/objects list, by adding it when missing 
    
    EG
    ```
    for x in pubs_details.publications:
        if not 'FOR' in x:
            x['FOR'] = []
    ```
    becomes
    
    ```
    normalize_key("FOR", pubs_details.publications)
    ```
    Changes happen in-place.

    TIP If `new_val` is not passed, it is inferred from first available non-empty value

    TODO add third argument to pass a lambda function for modifying key
    UPDATE 2019-11-28
    v0.6.1.2: normalizes also 'None' values (to address 1.21 DSL change)
    """
    if new_val == None:
        for x in dict_list:
            if key_name in x:
                new_val = type(x[key_name])() # create empty object eg `list()`
                # print(new_val)
                break 
    for x in dict_list:
        if (not key_name in x) or (x[key_name] == None):
            x[key_name] = new_val



def export_json_csv(jjson, query, USER_EXPORTS_DIR):
    """
    requires the pandas library which is not installed by default

    """
    try:
        from pandas import json_normalize
    except:
        click.secho("This feature requires the pandas library (`pip install pandas` from the terminal)", fg="red")
        return
    return_object = line_search_return(query)
    try:
        df =  json_normalize(jjson[return_object])
    except:
        df =  json_normalize(jjson)
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
    """
    requires the pandas library which is not installed by default

    """
    formatted_json = json.dumps(jjson, indent=4, sort_keys=True)
    filename = time.strftime("dsl_export_%Y%m%d-%H%M%S.json")
    url = save2File(formatted_json, filename, USER_EXPORTS_DIR)
    webbrowser.open(url)
    # df.to_csv(USER_EXPORTS_DIR + filename)
    print("Exported: ", "%s%s" % (USER_EXPORTS_DIR, filename))



def export_as_bar_chart(jjson, query, USER_EXPORTS_DIR):
    """
    requires the pandas and plotly libraries, which are not installed by default

    """

    try:
        from pandas import json_normalize
        import plotly.express as px
        from plotly.offline import plot
    except:
        click.secho("This feature requires the pandas and plotly library (`pip install pandas plotly` from the terminal)", fg="red")
        return

    return_object = line_search_return(query)
    
    try:
        df =  json_normalize(jjson[return_object])
    except:
        df =  json_normalize(jjson)

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




def export_as_jupyter(jjson, query, USER_EXPORTS_DIR):
    """
    Take the last 10 (default) rows from the history, and create a new python notebook with them. 
    Saves in usual location.

    Based on https://gist.github.com/fperez/9716279
    """

    try:
        from itertools import islice
        import subprocess
        import nbformat as nbf
    except:
        click.secho("This feature requires the nbformat library (`pip install nbformat` from the terminal)", fg="red")
        return

    nb = nbf.v4.new_notebook()
    this_time = time.strftime("%Y.%m.%d h%H:%M:%S")

    text = f"""# Dimensions API Queries Export\n### {this_time} \nThis notebook was generated using [Dimcli](https://github.com/digital-science/dimcli/) - the Dimensions API CLI."""

    nb['cells'] = [nbf.v4.new_markdown_cell(text)]

    setup = """!pip install dimcli -U --quiet\nimport dimcli\ndimcli.login()"""
    nb['cells'] += [nbf.v4.new_code_cell(setup)]

    nb['cells'] += [nbf.v4.new_code_cell("%%dsl\n" + query)]

    formatted_json = json.dumps(jjson, indent=4, sort_keys=True)
    results_preview = f"""### Precomputed Query Results: \n```\n{formatted_json}\n```"""
    nb['cells'] += [nbf.v4.new_markdown_cell(results_preview)]

    filename = time.strftime(f"dsl_export_%Y-%m-%d_%H-%M-%S.ipynb")
    nbf.write(nb, USER_EXPORTS_DIR + filename)
    
    subprocess.run(['open', USER_EXPORTS_DIR + filename], check=True)
    print("Exported: ", "%s%s" % (USER_EXPORTS_DIR, filename))





def print_json_stats(res, query=""):
    """
    from a dimcli.DslDataset object, print out basic stats
    * works primarily for 'search' types of query
    """
    # what is searched for
    source, tot = line_search_subject(query), None
    if source:
        if res['stats']:
            tot = res['stats']["total_count"]
        for k in res.good_data_keys():
            if tot and source == k:
                print(f"Returned {source.capitalize()}: {len(res[source])} (total = {tot})")
            else:
                print(f"Returned {k.capitalize()}: {len(res[k])}")



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
        if key not in ["_stats", "_warnings", "_notes",  "_version"]:
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
            if False:
                click.secho("---", dim=True)
                click.secho("Tip: use 'show <number>' or show+Tab to see more options", dim=True)



def print_json_compact(jsondata):
    """
    Show json in one line
    NOTE: the logic is the same as the except clause in print_json_preview. Maybe some refactoring could be beneficial here..
    """
    from pygments import highlight, lexers, formatters
    lexer = lexers.JsonLexer()
    formatter = formatters.TerminalFormatter()
    
    counter = 0
    for key in jsondata.keys():
        if key == "_stats":
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




def dimensions_url(obj_id, obj_type="", verbose=True):
    """
    Generate a valid Dimensions URL for one of the available sources.
    obj_id: the dimensions ID of the object
    obj_type: one of 'publications', 'grants', 'patents', 'policy_documents', 'clinical_trials', 'researchers'
    """
    
    if obj_type and obj_type not in G.sources():
        raise ValueError("ERROR: valid sources are: " + " ".join([x for x in G.sources()]))
    if not obj_type:
        for source, prefix in G.object_id_patterns().items():
            if obj_id.startswith(prefix):
                obj_type = source
    if obj_type:
        url = G.url_for_source(obj_type)
        if url:
            return url + obj_id


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



def dimensions_url_search(keywords_list_as_string):
    "Returns a valid keyword search URL for Dimensions"
    q = """https://app.dimensions.ai/discover/publication?search_text={}&search_type=kws&search_field=full_search"""
    from urllib.parse import quote   
    s = quote(keywords_list_as_string)  
    return q.format(s)


def google_url(stringa):
    """
    Generate a valid google search URL from a string (URL quoting is applied)
    """
    from urllib.parse import quote   
    s = quote(stringa)    
    return f"https://www.google.com/search?q={s}"
 


def dsl_escape(stringa, all=False):   
    """
    Helper for escaping the full-text inner query string, when it includes quotes. Usage:

    `search publications for "{dsl_escape(complex_q)}" return publications`

    EG imagine the query string:
    '"2019-nCoV" OR "COVID-19" OR "SARS-CoV-2" OR (("coronavirus"  OR "corona virus") AND (Wuhan OR China))'
    
    In Python, if you want to embed it into a DSL query, it has to become:
    '\\"2019-nCoV\\" OR \\"COVID-19\\" OR \\"SARS-CoV-2\\" OR ((\\"coronavirus\\"  OR \\"corona virus\\") AND (Wuhan OR China))'

    NOTE by default only quotes as escaped. If you want to escape all special chars, pass all=True, eg

    > dsl_escape('Solar cells: a new technology?', True)
    > 'Solar cells\\: a new technology?'

    See also: https://docs.dimensions.ai/dsl/language.html#for-search-term
    """
    
    if all:
        escaped = stringa.translate(str.maketrans({"^":  r"\^",
                                                    '"':  r'\"',
                                                    "\\": r"\\",
                                                    ":":  r"\:",
                                                    "~":  r"\~",
                                                    "[":  r"\[",
                                                    "]":  r"\]",
                                                    "{":  r"\{",
                                                    "}":  r"\}",
                                                    "(":  r"\(",
                                                    ")":  r"\)",
                                                    "!":  r"\!",
                                                    "|":  r"\|",
                                                    "&":  r"\&",
                                                    "+":  r"\+",
                                                    }))
    else:
        escaped = stringa.translate(str.maketrans({'"':  r'\"'}))        
    return escaped
