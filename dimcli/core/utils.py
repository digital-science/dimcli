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


def print_json_stats(res, query=""):
    """
    from a dimcli.Result object, print out basic stats
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
    if not os.path.exists(path):
        os.makedirs(path)
    filename = os.path.join(path, filename)
    f = open(filename, 'wb')
    f.write(contents.encode())  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it
    url = "file://" + filename
    return url



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


def get_dimensions_url(obj_id, obj_type):
    url = G.url_for_source(obj_type)
    if url:
        return url + obj_id


def init_config_folder(user_dir, user_config_file):
    """
    Create the config folder/file unless existing. If it exists, backup and create new one.
    """
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
        # click.secho("Created %s" % user_dir, dim=True)
    if os.path.exists(user_config_file):
        click.secho("The config file `%s` already exists." % user_config_file, fg="red")
        if click.confirm("Overwrite?"):
            pass
        else:
            click.secho("Goodbye")
            return False

    instance = "[instance.live]" # default for main instance
    url = click.prompt('Please enter the API URL or leave blank for default', default="https://app.dimensions.ai")
    login = click.prompt('Please enter your username')
    password = click.prompt('Please enter your password', hide_input=True, confirmation_prompt=True)

    f= open(user_config_file,"w+")
    f.write(instance + "\n")
    f.write("url=" + url + "\n")
    f.write("login=" + login + "\n")
    f.write("password=" + password + "\n")
    f.close()
    click.secho(
        "Created %s" % user_config_file, dim=True
    )



def chunks_of(data, size):
    it = iter(data)
    chunk = list(islice(it, size))
    while chunk:
        yield chunk
        chunk = list(islice(it, size))


def normalize_key(key_name, dict_list):
    """
    Ensures the key always appear in a JSON dict/objects list, by adding it when missing 

    EG

    for x in pubs_details.publications:
        if not 'FOR' in x:
            x['FOR'] = ""

    becomes

    normalize_key("FOR", pubs_details.publications)

    Changes happen in-place.
    TODO add third argument to pass a lambda function for modifying key
    """
    for x in dict_list:
        if not key_name in x:
            x[key_name] = ""



# {'name' : x['name'][5:]}


def export_json_csv(jjson, query, USER_JSON_OUTPUTS_DIR):
    """
    requires the pandas library which is not installed by default

    """
    try:
        from pandas.io.json import json_normalize
    except:
        click.secho("This feature requires the pandas library (`pip install pandas` from the terminal)", fg="red")
        return
    return_object = line_search_return(query)
    try:
        df =  json_normalize(jjson[return_object])
    except:
        df =  json_normalize(jjson)
    filename = time.strftime("dsl_export_%Y%m%d-%H%M%S.csv")
    url = save2File(df.to_csv(), filename, USER_JSON_OUTPUTS_DIR)
    webbrowser.open(url)
    # df.to_csv(USER_JSON_OUTPUTS_DIR + filename)
    print("Exported: ", "%s%s" % (USER_JSON_OUTPUTS_DIR, filename))



def export_json_html(jjson, query, USER_JSON_OUTPUTS_DIR):
    "print out full json either as pretty_json or within an html template"
    formatted_json = json.dumps(jjson, indent=4, sort_keys=True)
    contents = html_template_interactive(query, formatted_json)
    filename = time.strftime("%Y%m%d-%H%M%S.html")
    url = save2File(contents, filename, USER_JSON_OUTPUTS_DIR)
    webbrowser.open(url)
    print("Exported: ", "%s%s" % (USER_JSON_OUTPUTS_DIR, filename))


def export_json_json(jjson, query, USER_JSON_OUTPUTS_DIR):
    """
    requires the pandas library which is not installed by default

    """
    formatted_json = json.dumps(jjson, indent=4, sort_keys=True)
    filename = time.strftime("dsl_export_%Y%m%d-%H%M%S.json")
    url = save2File(formatted_json, filename, USER_JSON_OUTPUTS_DIR)
    webbrowser.open(url)
    # df.to_csv(USER_JSON_OUTPUTS_DIR + filename)
    print("Exported: ", "%s%s" % (USER_JSON_OUTPUTS_DIR, filename))



def preview_results(jsondata, maxitems=10):
    """
    Preview items in console
    If it's one of the main sources, try to show title/id. Otherwise show json in one line
    """
    # click.secho("Showing first %d records from latest query.." % maxitems, dim=True)
    # click.secho("")
    counter = 0
    for key in jsondata.keys():
        if key not in ["_stats", "_warnings"]:
            for row in jsondata[key]:
                counter += 1
                if counter <= maxitems:
                    try:  # title and url/id if object has them
                        url = get_dimensions_url(row['id'], key) or row['id']
                        if 'title' in row.keys():
                            name_or_title = row['title'].strip()
                        else:
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
                    click.style(str(row)))



def print_json_full(jsondata):
    """
    pretty print json 
    """
    formatted_json = json.dumps(jsondata, indent=4, sort_keys=True)
    from pygments import highlight, lexers, formatters
    colorful_json = highlight(formatted_json, lexers.JsonLexer(),
                                formatters.TerminalFormatter())
    print(colorful_json)



