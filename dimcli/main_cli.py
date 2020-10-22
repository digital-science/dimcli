#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import click
from pprint import pprint
import webbrowser

from .VERSION import *

from .core.auth import USER_DIR, USER_CONFIG_FILE_PATH, USER_HISTORY_FILE
from .core.api import *
from .utils.misc_utils import open_multi_platform
from .utils.repl_utils import init_config_folder, print_warning_prompt_version, preview_contents
from .utils.dim_utils import dimensions_url
from .utils.version_utils import print_dimcli_report, is_dimcli_outdated

try:
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.shortcuts import CompleteStyle
    from prompt_toolkit import PromptSession
    from prompt_toolkit.styles import Style
    PROMPT_TOOLKIT_VERSION_OK = True
except:
    PROMPT_TOOLKIT_VERSION_OK = False # => repl disabled


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("instance_name", nargs=1, default="live")
@click.option(
    "--init",
    is_flag=True,
    help="Create a local API configuration.")
@click.option(
    "--settings",
    is_flag=True,
    help="Show the local configuration.")
@click.option(
    "--checkversion",
    is_flag=True,
    help="Check if dimcli is up to date.")
@click.option(
    "--history", is_flag=True, help="Open query history file.")
@click.option(
    "--identifier", "-i", help="Open Dimensions webapp from an object ID.")
@click.option(
    "--websearch", "-w", help="Search Dimensions webapp from a quoted string.")
@click.pass_context
def main_cli(ctx, instance_name=None, init=False, settings=False, checkversion=False, history=False, identifier=None, websearch=None):
    """
    Python client for the Dimensions Analytics API.
    More info: https://github.com/digital-science/dimcli
    """
    if not (identifier or websearch):
        click.secho("Dimcli - Dimensions API Client (" + VERSION + ")", dim=True)

    if init:
        init_config_folder(USER_DIR, USER_CONFIG_FILE_PATH)
        return

    if checkversion:
        print_dimcli_report()
        return

    if identifier:
        url = dimensions_url(identifier)
        if not url: 
            click.secho("Cannot resolve automatically. Can be a patent, dataset or clinical trial ID. Falling back to search ..")
            url = dimensions_search_url(identifier)
        else:
            click.secho("Got a match: " + url)
        webbrowser.open(url)
        return 

    if websearch:
        url = dimensions_search_url(websearch)
        click.secho("Opening url: " + url)
        webbrowser.open(url)
        return 

    if not os.path.exists(USER_CONFIG_FILE_PATH):
        click.secho(
            "Credentials file not found - you can create one by typing: `dimcli --init`",
            fg="red",
        )
        click.secho(
            "More info: https://github.com/digital-science/dimcli#credentials-file",
            dim=True,
        )
        return

    if settings:
        preview_contents(USER_CONFIG_FILE_PATH)
        return

    if history:
        if os.path.exists(USER_HISTORY_FILE):
            open_multi_platform(USER_HISTORY_FILE)
        return

    if PROMPT_TOOLKIT_VERSION_OK:
        from .repl import repl
        # try online version check
        test = is_dimcli_outdated()
        if test:
            click.secho("====")
            click.secho("Heads up: there is a newer version of Dimcli available.", bold=True)
            click.secho("Update with `pip install dimcli -U` or, for more info, visit https://pypi.org/project/dimcli .\n====")
        # launch REPL
        repl.run(instance_name)
    else:
        print_warning_prompt_version()



if __name__ == "__main__":
    main_cli()
