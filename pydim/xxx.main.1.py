#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import click
from pprint import pprint
from .lib import *
from .VERSION import *

CMD_LINE_EXAMPLES = """EXAMPLES:
$ pydim -q 'search publications for "napoleon" return publications'

NOTE: watch the inner double quotes!

MORE ?
=> https://docs.dimensions.ai/dsl/index.html
"""

HOW_TO_INIT = """HOW TO SET UP A CONFIGURATION FILE:

Add a '.pydim.config.json' file to your home folder ('~'). 
The file should have the following structure:

    {
        "usr": "your-username",
        "psw" : "your-password", 
        "service" : "https://app.dimensions.ai/api/"   # default
    }

"""



def help_interpret_args(args):
    if len(args) == 1:
        return args[0]
    else:
        return " ".join([x for x in args])




@click.command()
@click.argument('args', nargs=-1)
@click.option('-q', '--query', help='Issue a DSL query')
@click.option('-d', '--doi', help='Search a DOI')
@click.option('-i', '--issn', help='Search a ISSN')
@click.option(
    '-s', '--settings', is_flag=True, help='Show current profile settings')
@click.option('-e', '--examples', is_flag=True, help='Show some examples')
# @click.option('--verbose', is_flag=True, help='Verbose logs')
@click.pass_context
def main_cli(ctx,
             args=None,
             query=None,
             doi=None,
             issn=None,
             settings=False,
             examples=False):
    """
    pydim: client for the dimensions.ai API\n
    $ pydim 'search publications for "napoleon" return publications'\n
    More info: https://docs.dimensions.ai/dsl/index.html
    """

    click.secho("pydim " + VERSION, bold=True)
    click.secho("------------", fg='white')

    account_details = get_init()
    if not account_details:
        click.secho(
            "**Account details not available or partially missing**\n",
            fg="red")
        click.secho(HOW_TO_INIT)
        return

    if settings:
        click.secho("ACTIVE SETTINGS:\n", dim=True)
        for k, v in account_details.items():
            if k == "psw":
                click.secho("%s: %s" % (k, "*" * len(v)), dim=True)
                # print k, ": ", "*" * len(v)
            else:
                click.secho("%s: %s" % (k, v), dim=True)
                # print k, ": ", v
        print("\n")
        click.secho(HOW_TO_INIT, dim=True)
        return

    if examples:
        click.secho(CMD_LINE_EXAMPLES, fg="green")
        return


    if not (query or doi or issn):
        if args:
            query = args[0]
        else:
            click.echo(ctx.get_help())
            return

    client = DimensionsClient(**account_details)
    # print s.usr, s.psw, s.service

    res = None
    if query:
        res = client.query(query)
    elif doi:
        res = client.search_doi_issn(doi=doi)
    elif issn:
        res = client.search_doi_issn(issn=issn)
    if res:
        pprint(res)


if __name__ == '__main__':
    main_cli()