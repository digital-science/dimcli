#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse

from ..VERSION import VERSION

URL_PATTERN = 'https://pypi.python.org/pypi/{package}/json'


def get_version(package, url_pattern=URL_PATTERN):
    """Return version of package on pypi.python.org using json."""
    req = requests.get(url_pattern.format(package=package))
    version = parse('0')
    if req.status_code == requests.codes.ok:
        j = json.loads(req.text.encode(req.encoding or "utf-8"))
        releases = j.get('releases', [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    return version

def print_dimcli_report(version=VERSION):
    try:
        v = get_version("dimcli")
        print("The latest Dimcli version is ", v.base_version )
        print("You have installed: ", VERSION)
        if v.base_version > VERSION:
            print("====\nPlease upgrade: `pip install dimcli -U`")
        else:
            print("====\nLooks like you're good.")
    except:
        print("Couldn't connect to the pypi server. Are you online?")
    



if __name__ == '__main__':
    print("Django==%s" % get_version('Django'))
