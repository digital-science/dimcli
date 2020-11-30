import configparser
import requests
import os.path
import os
import sys
import time
import json
import click

from ..utils.misc_utils import walk_up


USER_DIR = os.path.expanduser("~/.dimensions/")

# for API credentials
USER_CONFIG_FILE_NAME = "dsl.ini"
USER_CONFIG_FILE_PATH = os.path.expanduser(USER_DIR + USER_CONFIG_FILE_NAME)
USER_HISTORY_FILE = os.path.expanduser(USER_DIR + "history.txt")

#
USER_EXPORTS_DIR = os.path.expanduser("~/dimcli-exports/")

# for other settings
USER_SETTINGS_FILE_NAME = "settings"
USER_SETTINGS_FILE_PATH = os.path.expanduser(USER_DIR + USER_SETTINGS_FILE_NAME)


# global connection object
CONNECTION = {'instance': None, 'url': None, 'username': None, 'password': None, 'key': None,  'token' : None}




def do_global_login(instance="live", username="", password="", key="", url="https://app.dimensions.ai"):
    "Login into DSL and set the connection object with token"
    
    global CONNECTION

    if not (username and password) and not key:
        # then use 'instance' shortcut to get local credentials
        fpath = get_init_file()
        config_section = read_init_file(fpath, instance)
        url = config_section['url']
        try:
            username = config_section['login']
            password = config_section['password']
        except:
            username, password = "", ""
        try:
            key = config_section['key']
        except:
            key = ""


    login_data = {'username': username, 'password': password, 'key': key}
    response = requests.post(
        '{}/api/auth.json'.format(url), json=login_data)
    response.raise_for_status()

    token = response.json()['token']

    CONNECTION['instance'] = instance
    CONNECTION['url'] = url
    CONNECTION['username'] = username
    CONNECTION['password'] = password
    CONNECTION['key'] = key
    CONNECTION['token'] = token



def refresh_login():
    """
    Method used to login again if the TOKEN has expired - using previously entered credentials
    """
    do_global_login(CONNECTION['instance'], CONNECTION['username'], CONNECTION['password'], CONNECTION['key'], CONNECTION['url'])


def reset_login():
    ""
    global CONNECTION
    CONNECTION = {'instance': None, 'url': None, 'username': None, 'password': None,  'key': None,  'token' : None}


def get_connection():
    global CONNECTION
    return CONNECTION


def is_logged_in():
    if CONNECTION['token']:
        return True
    else:
        print("Warning: you are not logged in. Please use `dimcli.login(username, password)` before querying.")
        return False


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
    key=your_key

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
        click.secho("HowTo: https://digital-science.github.io/dimcli/getting-started.html#authentication", fg="red")
        sys.exit(0)
    # we have a good config file
    try:
        section = config['instance.' + instance_name]
    except:
        click.secho(f"ERROR: Credentials file `{fpath}` does not contain settings for instance: '{instance_name}''", fg="red")
        click.secho(f"Available instances are:")
        for x in config.sections():
            click.secho("'%s'" % x)
        click.secho("---\nSee Also: https://digital-science.github.io/dimcli/getting-started.html#authentication")
        config.sections()
        sys.exit(0)
    return section







def get_settings_file():
    """Get the global settings file. 
    This does not include any authentication info, only other settings eg github keys etc..
    It'll be extended in the future as new integrations/functionalities become available.
    """
    if os.path.exists(os.getcwd() + "/" + USER_SETTINGS_FILE_NAME):
        return os.getcwd() + "/" + USER_SETTINGS_FILE_NAME
    elif os.path.exists(os.path.expanduser(USER_SETTINGS_FILE_PATH )):
        return os.path.expanduser(USER_SETTINGS_FILE_PATH )
    else:
        for c,d,f in walk_up(os.getcwd()):
            if os.path.exists(c + "/" + USER_SETTINGS_FILE_NAME):
                return c + "/" + USER_SETTINGS_FILE_NAME
    return None

def read_settings_file(fpath, section_name):
    """
    parse the settings file for sections like 'gist' key etc..
    """
    config = configparser.ConfigParser()
    try:
        config.read(fpath)
    except:
        click.secho(f"ERROR: `{USER_SETTINGS_FILE_NAME}` settings file not found." , fg="red")
        click.secho("HowTo: https://digital-science.github.io/dimcli/getting-started.html#github-gists-token", fg="red")
        sys.exit(0)
    # we have a good config file
    try:
        section = config[section_name]
    except:
        click.secho(f"ERROR: Settings file `{fpath}` does not contain settings for: '{section_name}''", fg="red")
        click.secho("---\nPlease review the file contents, or see https://digital-science.github.io/dimcli/getting-started.html#github-gists-token")
        config.sections()
        sys.exit(0)
    return section


