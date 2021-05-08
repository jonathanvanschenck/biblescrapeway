import click
import json

from pathlib import Path

from .query import query

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def _format_line(obj, _format):
    if _format == 'refstr':
        return obj.to_string()
    if _format == 'str':
        return '`{}` ({})'.format(obj.text,obj.version)

def _formatter(obj_list, _format):
    # Handle json
    if _format == 'json':
        return json.dumps([v.to_dict() for v in obj_list],indent=4)

    # Handle everything else
    return "\n".join([_format_line(obj,_format) for obj in obj_list])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--version', '-v', default='ESV', help='Bible version to query, default is `ESV`')
@click.option('--format', '-f', '_format', default='refstr', type=click.Choice(['refstr','str','json']),
        help='Specify output format, default is `refstr`')
@click.option('--cache/--no-cache',  default=False, 
        help='Look up verses saved in a local cache first, and save new queries locally')
@click.argument('reference_string')
def scrap(version, reference_string, _format, cache):
    """Scrap bible verses

    REFERENCE_STRING a (comma delimited) list of references, e.g. `John3.16` or `1Peter3.1-5` or `Gen1,2`
    """
    
    verses = query( reference_string, version, cache )
    click.echo(_formatter(verses, _format))

