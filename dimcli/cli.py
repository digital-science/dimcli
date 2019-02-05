#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import click
from pprint import pprint
# from .console.lib import *
from .console import repl
# from .console import credentials

from .VERSION import *
from .dimensions import *

# HOW TO SET UP A CONFIGURATION FILE:

# Add a '.dimcli.config.json' file to your home folder ('~').
# The file should have the following structure:

#     {
#         "usr": "your-username",
#         "psw" : "your-password",
#         "service" : "https://app.dimensions.ai/api/"   # default
#     }


@click.command()
@click.argument("instance", nargs=1, default="live")
@click.pass_context
def main_cli(ctx, instance=None):
    """
    dimcli: client for the dimensions.ai
    More info: https://docs.dimensions.ai/dsl/index.html
    """

    click.secho("dimcli " + VERSION, dim=True)
    click.secho("------------", fg="white")

    if not USER_CONFIG_FILE:
        click.secho(
            "Please set up a Dimensions init file first (see the README)",
            fg="green",
        )
        return

    # dsl = Dsl(instance)
    # dsl.query("search grants return grants", True)
    # print(res)
    # unique functionality > launch REPL
    repl.run(instance)


if __name__ == "__main__":
    main_cli()
