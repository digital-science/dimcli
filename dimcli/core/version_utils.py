#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
from packaging import version
# try:
    
#     from packaging.version import parse
# except ImportError:
#     from pip._vendor.packaging.version import parse

from ..VERSION import __version__ as VERSION  # strip out the 'v'

URL_PATTERN = 'https://pypi.python.org/pypi/{package}/json'


def get_version(package, url_pattern=URL_PATTERN):
    """Return version of package on pypi.python.org using json."""
    req = requests.get(url_pattern.format(package=package))
    the_version = version.parse('0')
    if req.status_code == requests.codes.ok:
        j = json.loads(req.text.encode(req.encoding or "utf-8"))
        releases = j.get('releases', [])
        for release in releases:
            ver = version.parse(release)
            if not ver.is_prerelease:
                the_version = max(the_version, ver)
    return the_version

def print_dimcli_report(this_version=VERSION):
    try:
        latest = get_version("dimcli")
        print("====\nThe latest Dimcli version is ", latest.base_version )
        print("You have installed: ", VERSION)
        if version.parse(latest.base_version) > version.parse(this_version):
            print("====\nPlease upgrade: `pip install dimcli -U`")
        else:
            print("====\nYou're up to date.")
    except:
        print("Couldn't connect to the pypi server. Are you online?")


def is_dimcli_outdated(this_version=VERSION):
    try:
        latest = get_version("dimcli")
        if version.parse(latest.base_version) > version.parse(this_version):
            return True
        else:
            return False
    except:
        return None

