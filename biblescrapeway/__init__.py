"""`biblescrapeway` tool for scraping bible verses from the web
"""

from .src import scraper
from .src import errors
from .src import reference
from . import cli
from .src.query import query
from .version import __version__


__author__ = "Jonathan D B Van Schenck"
