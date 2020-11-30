"""
Utilities for working with Github Gists 
"""


import configparser
import requests
import click
import os
import json

from ..core.auth import get_settings_file, read_settings_file



class GistsHelper():
    """
    """
 
    def __init__(self):
        fpath = get_settings_file()
        config_section = read_settings_file(fpath, "gist")
        self.token = config_section['token']

    def save_gist(self, desc, files_details, verbose=False):
        """

        desc str
        files_details dict 

        {"name.md": {
                "content": "..."
                    }

        """

        url="https://api.github.com/gists"

        headers={'Authorization':'token %s'%self.token, "Accept": "application/vnd.github.v3+json"}

        payload={
            "description": desc,
            "public":   False,
            "files": files_details
            }

        #make a request
        res=requests.post(url,headers=headers,data=json.dumps(payload))

        #print response --> JSON
        if verbose: click.secho("Status: " + str(res.status_code))
        j=json.loads(res.text)
        if verbose: click.secho("Result: " + j['html_url'])
        return j['html_url']