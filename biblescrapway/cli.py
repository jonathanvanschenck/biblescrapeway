import click

from .reference import Reference, normalize_reference_string, parse_reference_string
from .scraper import scrap as _scrap

@click.command()
@click.option('--version', default='ESV', help='Bible version to query')
@click.argument('reference_list_string')
def scrap(version, reference_list_string):
    range_string = parse_reference_string(reference_list_string)
    verses = []
    for _range in range_string:
        if _range.is_single:
            _verses = [_scrap(_range.start,version)]
        else:
            chaps = [
                Reference(_range.start.book,c)\
                for c in range(_range.start.chapter, _range.end.chapter+1)
            ]
            _verses = []
            for ref in chaps:
                _verses += _scrap(ref,version)
            _verses = [v for v in _verses if _range.contains(v)]

        verses += _verses

    for v in verses:
        click.echo(v.to_string())

