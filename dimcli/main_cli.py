#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import click
from pprint import pprint
import webbrowser

from .VERSION import *

from .core.auth import USER_DIR, USER_CONFIG_FILE_PATH, USER_HISTORY_FILE
from .core.api import *
from .core.utils import open_multi_platform, init_config_folder, print_warning_prompt_version, preview_contents, print_dimensions_url
from .core.version_utils import print_dimcli_report, is_dimcli_outdated

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
    help="Create a configuration file with your API credentials.")
@click.option(
    "--settings",
    is_flag=True,
    help="Show the local configuration file.")
@click.option(
    "--vcheck",
    is_flag=True,
    help="Check online if your dimcli version is the latest.")
@click.option(
    "--history", is_flag=True, help="Open history file with default editor.")
@click.option(
    "--id", "-id", help="Resolve a Dimensions ID to its public URL.")
@click.option(
    "--websearch", "-w", help="Search a quoted string in Dimensions web.")
@click.pass_context
def main_cli(ctx, instance_name=None, init=False, settings=False, vcheck=False, history=False, id=None, websearch=None):
    """
    Python client for the Dimensions Analytics API.
    More info: https://github.com/digital-science/dimcli
    """
    click.secho("Dimcli - Dimensions API Client (" + VERSION + ")", dim=True)

    if init:
        init_config_folder(USER_DIR, USER_CONFIG_FILE_PATH)
        return

    if vcheck:
        print_dimcli_report()
        return

    if id:
        print_dimensions_url(id)
        return 

    if websearch:
        url = dimensions_url_search(websearch)
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
