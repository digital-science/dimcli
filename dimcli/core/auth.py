import configparser
import requests
import os.path
import os
import sys
import time
import json
import click

from ..utils.misc_utils import walk_up, printDebug


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



###
#
# class that encapsulates the login/token logic for the API
#
#
###



class APISession():

    """Dimensions API Authentication logic
    """

    def __init__(self, verbose=True):
        """Initialises a Dsl Authentication Session object.

        Normally it is not needed to instantiate directly this object, instead it's 
        quicker to use the `dimcli.login()` utility method, which create a global
        authentication session. 

        In some situations though, you'd want to query two separate Dimensions instances 
        in parallel. To that end, pass an APISession instance to the Dsl() constructor
        using the `auth_session` parameter, IE:  

        ```
        from dimcli.core.auth import APISession

        mysession1 = APISession()
        mysession1.login(instance="key-test")
        d1 = Dsl(auth_session=mysession1)
        d1.query("search publications return research_orgs")
        
        mysession2 = APISession()
        mysession2.login(instance="live")
        d2 = Dsl(auth_session=mysession2)
        d2.query("search publications return research_orgs")
        ```

        """
        self.instance = None
        self.url = None
        self.url_auth = None
        self.url_query = None
        self.username = None
        self.password = None
        self.key = None
        self.verify_ssl = None
        self.token = None
        # self._verbose = verbose


    def login(self, 
                instance="", 
                username="", 
                password="", 
                key="", 
                endpoint="",
                verify_ssl=True,
                verbose=True):
        """Login into Dimensions API endpoint and get a query token.

        INSTANCE => used to reference the local configuration file
        ENDPOINT => explicity set the endpoint URL to use. If not provided, it will be inferred from the instance name.
        
        """

        if False:
            # FOR INTERNAL QA ONLY
            click.secho(f"""instance="{instance}", 
                            username="{username}", 
                            password="{password}", 
                            key="{key}", 
                            endpoint="{endpoint}",
                            verify_ssl="{verify_ssl}")""", fg="red")

        if (username or password) and not (username and password):
            raise Exception("Authentication error: you provided only one value for username and password. Both are required.")

        if instance and endpoint:
            if verbose: printDebug(f"Warning: you provided both instance and endpoint values. Endpoint will be ignored." , "comment")
            endpoint = ""

        if (key or (username and password)):
            # explicit credentials, no need to look for config file
            if not endpoint:
                if verbose: printDebug("Using default endpoint: 'https://app.dimensions.ai'", "comment")
                endpoint="https://app.dimensions.ai"
            instance = ""

        else:
            # no key, no usr/pwd => use the config file
            fpath = get_init_file()

            if not instance and not endpoint:
                if verbose: printDebug("Searching config file credentials for default 'live' instance..", "comment")
                instance="live"
                config_section = read_init_file(fpath, instance_name=instance)
            elif endpoint:
                if verbose: printDebug(f"Searching config file credentials for '{endpoint}' endpoint..", "comment")
                config_section = read_init_file(fpath, endpoint=endpoint)
            else:
                if verbose: printDebug(f"Searching config file credentials for '{instance}' instance..", "comment")
                config_section = read_init_file(fpath, instance_name=instance)

            endpoint = config_section['url'] # OVERRIDE URL USING LOCAL CONFIG
            
            try:
                username = config_section['login']
                password = config_section['password']
            except:
                username, password = "", ""
            try:
                key = config_section['key']
            except:
                key = ""
            try:
                verify_ssl = config_section.getboolean('verify_ssl')
            except:
                verify_ssl = True

        URL_AUTH, URL_QUERY = self._get_endpoint_urls(endpoint)
        # printDebug(URL_AUTH, URL_QUERY )

        login_data = {'username': username, 'password': password, 'key': key}
        
        # POST AUTH REQUEST
        response = requests.post(URL_AUTH, json=login_data, verify=verify_ssl)
        response.raise_for_status()

        token = response.json()['token']

        self.instance = instance
        self.url = URL_QUERY
        self.username = username
        self.password = password
        self.key = key
        self.verify_ssl = verify_ssl
        self.token = token


    def _get_endpoint_urls(self, user_url):
        """Infer the proper API endpoints URLs from the (possibly incomplete) URL the use is sending. 
        
        CASE 1
        User provides a domain URL eg https://app.dimensions.ai. 
        => Then the Query URL defaults to `/api/dsl`

        CASE 1
        User provides a full query URL eg https://app.dimensions.ai/api/dsl/v2. 
        => Then no action is needed

        Query Endpoints:
        * /api/dsl/v1
        * /api/dsl/v2
        * /api/dsl
        * /api/dsl.json

        Auth endpoint (always inferred)
        * /api/auth.json

        https://docs.dimensions.ai/dsl/2.0.0/api.html#endpoints

        NOTE 
        We never try to validate URLs provided by users.

        """
        url_auth, url_query = None, None
        if "/api/" in user_url:
            # savy user passing the full QUERY URL
            domain = user_url.split("/api/")[0]
            url_auth = domain + "/api/auth.json"
            url_query = user_url
        else:
            domain = user_url
            url_auth = domain + "/api/auth.json"
            url_query = domain + "/api/dsl"
        self.url_auth, self.url_query = url_auth, url_query
        return url_auth, url_query



    def refresh_login(self):
        """
        Method used to login again if the TOKEN has expired - using previously entered credentials
        """
        self.login(  instance=self.instance, 
                        username=self.username, 
                        password=self.password, 
                        key=self.key, 
                        endpoint=self.url,
                        verify_ssl=self.verify_ssl,
                        verbose=False
                        )


    def reset_login(self):
        ""
        self.instance = None
        self.url = None
        self.username = None
        self.password = None
        self.key = None
        self.token = None
        self.verify_ssl = True


    def is_logged_in(self):
        if self.token:
            return True
        else:
            printDebug("Warning: you are not logged in. Please use `dimcli.login()` before querying.")
            return False



###
#
# global connection object and helper methods
#
#
###


CONNECTION = APISession()



def do_global_login(instance="", username="", password="", key="", url="", verify_ssl=True):
    "Login into DSL and set the connection object with token"
    global CONNECTION
    CONNECTION.login(instance, username, password, key, url, verify_ssl)
    


def get_global_connection():
    global CONNECTION
    return CONNECTION


def is_logged_in_globally():
    "used only internally for magic commands and function wrappers, which always expect a global login"
    global CONNECTION
    if CONNECTION.token:
        return True
    else:
        printDebug("Warning: you are not logged in. Please use `dimcli.login(username, password)` before querying.")
        return False



###
#
# INIT file helpers 
#
#
###

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

def read_init_file(fpath, instance_name="", endpoint=""):
    """
    parse the credentials file
    """
    config = configparser.ConfigParser()
    try:
        config.read(fpath)
    except:
        printDebug(f"ERROR: `{USER_CONFIG_FILE_NAME}` credentials file not found." , fg="red")
        printDebug("HowTo: https://digital-science.github.io/dimcli/getting-started.html#authentication", fg="red")
        sys.exit(0)
    # we have a good config file

    if instance_name:
        try:
            section = config['instance.' + instance_name]
        except:
            printDebug(f"ERROR: Credentials file `{fpath}` does not contain settings for instance: '{instance_name}''", fg="red")
            printDebug(f"Available instances are:")
            for x in config.sections():
                printDebug("'%s'" % x)
            printDebug("---\nSee Also: https://digital-science.github.io/dimcli/getting-started.html#authentication")
            config.sections()
            sys.exit(0)
        return section

    elif endpoint:
        # try all stored configurations
        for instance_name in config.sections():
            try:
                # print(instance_name, config[instance_name]['url'])
                if endpoint == config[instance_name]['url']:
                    return config[instance_name]
            except:
                pass
        printDebug(f"ERROR: Credentials file `{fpath}` does not contain settings for endpoint: '{endpoint}''", fg="red")        
        sys.exit(0)




###
#
# settings file helper eg gists key etcc
#
#
###


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
        printDebug(f"ERROR: `{USER_SETTINGS_FILE_NAME}` settings file not found." , fg="red")
        printDebug("HowTo: https://digital-science.github.io/dimcli/getting-started.html#github-gists-token", fg="red")
        sys.exit(0)
    # we have a good config file
    try:
        section = config[section_name]
    except:
        printDebug(f"ERROR: Settings file `{fpath}` does not contain settings for: '{section_name}''", fg="red")
        printDebug("---\nPlease review the file contents, or see https://digital-science.github.io/dimcli/getting-started.html#github-gists-token")
        config.sections()
        sys.exit(0)
    return section


