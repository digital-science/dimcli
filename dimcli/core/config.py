import configparser
import requests
import os.path
import os
import sys
import time
import json
import click

from .walkup import *


USER_DIR = os.path.expanduser("~/.dimensions/")
USER_CONFIG_FILE_NAME = "dsl.ini"
USER_CONFIG_FILE_PATH = os.path.expanduser(USER_DIR + USER_CONFIG_FILE_NAME)
USER_JSON_OUTPUTS_DIR = os.path.expanduser(USER_DIR + "json/")
USER_HISTORY_FILE = os.path.expanduser(USER_DIR + "history.txt")



CONNECTION = {'instance': None, 'url': None, 'username': None, 'password': None,  'token' : None}



def get_init_file():
    """
    LOGIC

    a) if dsl.ini credentials file in WD that overrides everything
    b) try user level credentials ("~/.dimensions/") 
    c) try navigating up directory tree for dsl.ini

    => a) and c) are useful for jup notebooks without system wide installation
    => b) is the usual case for CLI

    ===================
    BACKGROUND 

    Authentication details can be stored in a `dsl.ini` file
    File contents need to have this structure:

    [instance.live]
    url=https://app.dimensions.ai
    login=your_username
    password=your_password

    The section name has to start with "instance."
    Keyword "live" is the default name for most installations.

    If you have access to other Dimensions APIs just add an entry for them with a suitable name.
    ===================
    """
    if os.path.exists(os.getcwd() + "/" + USER_CONFIG_FILE_NAME):
        return os.getcwd() + "/" + USER_CONFIG_FILE_NAME
    elif os.path.exists(os.path.expanduser(USER_CONFIG_FILE_PATH )):
        return os.path.expanduser(USER_CONFIG_FILE_PATH )
    else:
        for c,d,f in walk_up(os.getcwd()):
            if os.path.exists(c + "/" + USER_CONFIG_FILE_NAME):
                return c + "/" + USER_CONFIG_FILE_NAME
    return None

def read_init_file(fpath, instance_name):
    """
    parse the credentials file
    """
    config = configparser.ConfigParser()
    try:
        config.read(fpath)
    except:
        click.secho(f"ERROR: `{USER_CONFIG_FILE_NAME}` credentials file not found." , fg="red")
        click.secho("HowTo: https://github.com/lambdamusic/dimcli#credentials-file", fg="red")
        sys.exit(0)
    # we have a good config file
    try:
        section = config['instance.' + instance_name]
    except:
        click.secho(f"ERROR: Credentials file `{fpath}` does contain settings for instance: '{instance_name}''", fg="red")
        click.secho(f"Available instances are:")
        for x in config.sections():
            click.secho("'%s'" % x)
        click.secho("---\nSee Also: https://github.com/lambdamusic/dimcli#credentials-file")
        config.sections()
        sys.exit(0)
    return section



def do_global_login(instance="live", username="", password="", url="https://app.dimensions.ai"):
    "Login into DSL and set the connection object with token"
    
    global CONNECTION

    if not (username and password):
        fpath = get_init_file()
        config_section = read_init_file(fpath, instance)
        url = config_section['url']
        username = config_section['login']
        password = config_section['password']


    login_data = {'username': username, 'password': password}
    response = requests.post(
        '{}/api/auth.json'.format(url), json=login_data)
    response.raise_for_status()

    token = response.json()['token']

    CONNECTION['instance'] = instance
    CONNECTION['url'] = url
    CONNECTION['username'] = username
    CONNECTION['password'] = password
    CONNECTION['token'] = token



def refresh_login():
    "login again using previously used details"
    do_global_login(CONNECTION['instance'], CONNECTION['username'], CONNECTION['password'], CONNECTION['url'])