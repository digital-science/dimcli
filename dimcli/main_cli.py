#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import click
from pprint import pprint

from .VERSION import *

from .core.auth import USER_DIR, USER_CONFIG_FILE_PATH, USER_HISTORY_FILE
from .core.api import *
from .core.utils import open_multi_platform, init_config_folder, print_warning_prompt_version, preview_contents
from .core.version_utils import print_dimcli_report, is_dimcli_outdated

try:
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.shortcuts import CompleteStyle
    from prompt_toolkit import PromptSession
    from prompt_toolkit.styles import Style
    PROMPT_TOOLKIT_VERSION_OK = True
except:
    PROMPT_TOOLKIT_VERSION_OK = False # => repl disabled


@click.command()
@click.argument("instance_name", nargs=1, default="live")
@click.option(
    "--init", "-i",
    is_flag=True,
    help="Initialize the configuration file with your Dimensions account details.")
@click.option(
    "--config", "-c",
    is_flag=True,
    help="Show configuration file.")
@click.option(
    "--versioncheck", "-v",
    is_flag=True,
    help="Check online if your dimcli version is the latest.")
@click.option(
    "--history", "-h", is_flag=True, help="Open history file with default editor.")
@click.pass_context
def main_cli(ctx, instance_name=None, init=False, config=False, versioncheck=False, history=False):
    """
    Python client for the Dimensions DSL.
    More info: https://github.com/digital-science/dimcli
    """
    click.secho("Dimcli - Dimensions API Console (" + VERSION + ")", dim=True)

    if init:
        init_config_folder(USER_DIR, USER_CONFIG_FILE_PATH)
        return

    if versioncheck:
        print_dimcli_report()
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

    if config:
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
            click.secho("====\nHeads up: there is a newer version of Dimcli available at https://pypi.org/project/dimcli/.\n====", bold=True)
        # launch REPL
        repl.run(instance_name)
    else:
        print_warning_prompt_version()



if __name__ == "__main__":
    main_cli()
