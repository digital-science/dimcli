#!/usr/bin/python
# -*- coding: utf-8 -*-

import click
import json
import sys
import subprocess
import os

from .dsl_grammar import *
from .html import *


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
        return False


def line_last_two_words(line):
    "return last two words"
    if len(line.split()) > 1:
        return " ".join([line.split()[-2], line.split()[-1]])
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

def line_search_return(line):
    """get the source/facet in the return statement
        TODO: return multiple return values not just one
    """
    l = line.split()
    if "return" in l:
        i = l.index("return")
        if len(l) > i + 1: # cause index is zero based
            return l[i + 1]
    else:
        return None

def line_search_aggregates(line):
    """get the aggregrates statement eg in `search publications return funders aggregate altmetric_median sort by rcr_avg`
        TODO: return multiple return values not just one
    """
    l = line.split()
    if "aggregate" in l:
        i = l.index("aggregate")
        if len(l) > i + 2: # cause index is zero based
            return l[i + 1]
    else:
        return None

def line_add_lazy_return(text):
    "if return statement not included, add it lazily"
    if "return" not in text:
        source = line_search_subject(text)
        if source in VOCABULARY['sources'].keys():
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
    if obj_type in VOCABULARY['dimensions_urls'].keys():
        return VOCABULARY['dimensions_urls'][obj_type] + obj_id
    else:
        return None


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
