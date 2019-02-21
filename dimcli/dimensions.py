import configparser
import requests
import os.path
import time
import json
import IPython.display
from itertools import islice

# Authentication
# Authentication is read from a config file. Create a dsl.ini in ~/.dimensions/ which has to look like this:

# [instance.live]
# url=https://app.dimensions.ai
# login=your_username
# password=your_password

# The section name has to start with "instance.". "live" is the default name for most installations.
#
# If you have access to other Dimensions DBs just add an entry for them with a suitable name.

USER_DIR = "~/.dimensions/"
USER_CONFIG_FILE = os.path.expanduser(USER_DIR + "dsl.ini")
USER_JSON_OUTPUTS_DIR = os.path.expanduser(USER_DIR + "json/")
USER_HISTORY_FILE = os.path.expanduser(USER_DIR + "history.txt")


class Result(IPython.display.JSON):
    def __init__(self, data):
        IPython.display.JSON.__init__(self, data)

    def __getitem__(self, key):
        return self.data[key]


class Dsl:
    def __init__(self, instance="live", show_results=False, rich_display=True):
        config = configparser.ConfigParser()
        config.read(os.path.expanduser(USER_CONFIG_FILE))
        section = config['instance.' + instance]

        self._url = section['url']
        self._show_results = show_results
        self._rich_display = rich_display  # whether to iPython renderers

        self._username = section['login']
        self._password = section['password']

        self._login()

    def _login(self):
        login = {'username': self._username, 'password': self._password}
        response = requests.post(
            '{}/api/auth.json'.format(self._url), json=login)
        response.raise_for_status()

        token = response.json()['token']
        self._headers = {'Authorization': "JWT " + token}

    def query(self, q, show_result=None, rich_display=None, retry=0):
        """
        Execute DSL query.
        By default it doesn't show results, but it uses the iPython rich widgets for it, optimized for Jupyter Notebooks.
        """
        #   Execute DSL query.
        resp = requests.post(
            '{}/api/dsl.json'.format(self._url), data=q, headers=self._headers)
        if resp.status_code == 429:  # Too Many Requests
            print(
                'Too Many Requests for the Server. Sleeping for 30 seconds and then retrying.'
            )
            time.sleep(30)
            return self.query(q)
        elif resp.status_code == 403:  # Forbidden:
            print('Login token expired. Logging in again.')
            self._login()
            return self.query(q)
        elif resp.status_code == 200 or resp.status_code == 400:  # OK or Error
            #   Display raw result
            if rich_display or (rich_display is None and self._rich_display):
                result = Result(resp.json())
                if show_result or (show_result is None and self._show_results):
                    IPython.display.display(result)
            else:
                result = resp.json()
                if show_result or (show_result is None and self._show_results):
                    print(json.dumps(result, indent=4, sort_keys=True))
            return result
        else:
            if retry > 0:
                print('Retrying in 30 secs')
                time.sleep(30)
                return self.query(
                    q,
                    show_result=show_result,
                    rich_display=rich_display,
                    retry=retry - 1)
            else:
                resp.raise_for_status()


def chunks_of(data, size):
    it = iter(data)
    chunk = list(islice(it, size))
    while chunk:
        yield chunk
        chunk = list(islice(it, size))
