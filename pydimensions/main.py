#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import click
from .lib import *




CMD_LINE_EXAMPLES = """EXAMPLES:
$ @TODO
"""




@click.command()
@click.argument('args', nargs=-1)
@click.option('--doi', help='Search a DOI')
@click.option('--issn', help='Search a ISSN')
@click.option('--isbn', help='Search a ISBN')
@click.option('--examples', is_flag=True, help='Show some examples')
@click.option('--verbose', is_flag=True, help='Verbose logs')
@click.pass_context
def main_cli(ctx, args=None, doi=None, issn=None, isbn=None, rdf=None,  examples=False, verbose=False):
    """PyDimensions: client for dimensions.ai   
    """

    if examples:
        click.secho(CMD_LINE_EXAMPLES, fg="green")
        return

    if not (doi or issn or isbn) and not args:
        # print dir(search_cli)
        click.echo(ctx.get_help())
        return
 

    s = DimensionsClient(verbose=verbose)

    click.secho("Not implemented", fg="green")


if __name__ == '__main__':
    main_cli()