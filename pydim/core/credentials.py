import requests
import click
import os
import json


DEFAULT_SERVICE = "https://app.dimensions.ai/api/"
USER_CONFIG_FILE = os.path.expanduser("~") + "/.pydim.config.json"


def register_credentials():
    usr = click.prompt("Username")
    psw = click.prompt("Password")
    data = {"usr": usr, "psw": psw, "service": DEFAULT_SERVICE}
    with open(USER_CONFIG_FILE, "w") as f:
        f.write(json.dumps(data))
        f.close()
    print(json.dumps(data), " => ", USER_CONFIG_FILE)


def get_credentials():
    """
    Get init details. These have to be manually added in a file in the home folder: '~/.pydim.config.json'
    
    This is the source file structure:

    {
        "usr": "spam",
        "psw" : "spam", 
        "service" : "https://app.dimensions.ai/api/"   # optional
    }

    Returns a dict:

    {'usr': usr, 'psw': psw, 'service': service}
    
    """

    try:
        with open(USER_CONFIG_FILE) as f:
            data = json.load(f)
    except:
        return None

    if data:
        try:
            usr = data["usr"]
            psw = data["psw"]
        except:
            return None
        try:
            service = data["service"]
        except:
            service = DEFAULT_SERVICE
        return {"usr": usr, "psw": psw, "service": service}
    else:
        return None

