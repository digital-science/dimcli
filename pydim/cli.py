#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import click
from pprint import pprint
from .core.lib import *
from .core import repl
from .core import credentials

from .VERSION import *


# HOW TO SET UP A CONFIGURATION FILE:

# Add a '.pydim.config.json' file to your home folder ('~').
# The file should have the following structure:

#     {
#         "usr": "your-username",
#         "psw" : "your-password",
#         "service" : "https://app.dimensions.ai/api/"   # default
#     }


def help_interpret_args(args):
    if len(args) == 1:
        return args[0]
    else:
        return " ".join([x for x in args])


@click.command()
@click.argument("args", nargs=-1)
@click.option(
    "--register",
    is_flag=True,
    help="Store Dimensions user and password on this computer",
)
@click.pass_context
def main_cli(ctx, args=None, register=False):
    """
    pydim: client for the dimensions.ai
    More info: https://docs.dimensions.ai/dsl/index.html
    """

    click.secho("PyDim " + VERSION, dim=True)
    click.secho("------------", fg="white")

    data = credentials.get_credentials()
    if not data or register:
        click.secho(
            "Please set up a Dimensions account (this data will be stored in a hidden file in your home folder)",
            fg="green",
        )
        credentials.register_credentials()
        data = credentials.get_credentials()

    # unique functionality > launch REPL
    repl.main()


if __name__ == "__main__":
    main_cli()
