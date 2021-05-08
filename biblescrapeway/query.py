"""Look up a bible verse, range, or list
"""

from pathlib import Path

from .reference import Reference, parse_reference_string
from .scraper import scrap
from .cache import BibleCacher

def query( query_string, version = "ESV", cache = False, cache_fp = None ):
    """Look up a bible verse, range or list

    Parameters
    ----------
    query_string : string
        A string of bible verses and ranges. Ranges should be
        '-' delimited, and lists should be ',' delimited. E.g.
        'john 3:16' or 'john 3:16-20' or 'John 1:1, 10:4'.

    version : string
        The bible version abbreviation to use. E.g. 'ESV' or 'NIV'
    
    cache : bool
        If true, queries result will be cached at `~/.bsw_cache.json`
        and subsequently look up, rather than re-queried

    cache_fp : string or None
        A file path to where the cache file should be saved, only relevent
        if `cache` is true. If `None`, the default is `~/.bsw_cache.json`

    Return
    ------
    list of `scraper.Verse` objects
    """

 
    range_string = parse_reference_string(query_string)
    
    path = (Path.home() / ".bsw_cache.json") if (cache_fp is None) else (cache_fp)
    _cache = BibleCacher(path if cache else None)

    verses = []
    for _range in range_string:
        
        # First try to lookup the verse (will always fail if _cache=None)
        _verses = _cache.look_up(_range, version)
        
        # If the lookup fails, run a query
        if _verses is None:
            if _range.is_single_verse:
                _verses = [scrap(_range.start,version)]
            else:
                # If the range is contains more than one verse, query all
                #  chapters. Necessary, since some versions exclude some
                #  verses (i.e. the longer ending of Mark), and since
                #  if a query spans multiple chapters, there is no way
                #  to know (without hardcoding) how many verses each 
                #  chapter should contain.
                chaps = [
                    Reference(_range.start.book,c)\
                    for c in range(_range.start.chapter, _range.end.chapter+1)
                ]
                _verses = []
                for ref in chaps:
                    _verses += scrap(ref,version)
                _verses = [v for v in _verses if _range.contains(v)]
        
        # Cache the verses
        _cache.cache( _range, _verses ) 

        verses += _verses

    return verses
