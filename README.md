# Biblescrapeway
A scraping tool for pulling bible verses from the web, [check it out here!](https://github.com/jonathanvanschenck/biblescrapeway)

# Basic Usage
## Install with pip
```bash
 $ pip3 install biblescrapeway
```

## CLI
`biblescrapeway` comes with a simple cli (`bsw`) to pull specific bible passages:
```bash
 $ bsw John3.16
```

You can also specify a translation (default is ESV):
```bash
 $ bsw --translation KJV John3.16
```

Or, get multiple verses with comma delimiting:
```bash
 $ bsw John3.16,1Peter3:8
```

Or, get a range of verses using a hyphon
```bash
 $ bsw John3.16-17
```

You can specify a formatting type with the `--format/-f` option, which exposes raw json:
```bash
 $ bsw -f json John3.16
```

You can also set the `--cache/--no-cache` flag to cache the results of queries locally, so
that they can just be looked up on repeated evaluations. By default, `bsw` uses `--cache`.
```bash
 $ bsw --no-cache John3.16 # scraps the verse from the web
 $ bsw --no-cache John3.16 # scraps the verse from the web again
 $ bsw --cache John3.16    # scraps the verse, then saves it locally at '~/.bsw_cache.json'
 $ bsw --cache John3.16    # looks up the verse locally, does not re-scrape it
 $ bsw --no-cache John3.16 # scraps the verse from the web again
```

## Programmatic
It is also possible to get full verse objects via python, using the `query` function:
```python
from biblescrapeway import query
verse = query("John 3:16", version = "NIV")[0]
verse.to_dict()
```
The function returns a `scraper.Verse` object, which can be convered into a `dict` using
the `.to_dict()` method. The resulting object has the following format:
```json
{
    "book"    : "str | name of the bible book",
    "chapter" : "int | chapter number",
    "verse"   : "int | verse number",
    "version" : "str | bible version abbreviation",
    "text"    : "str | text content of the verse",
    "footnotes" : [
        {
            "str_index" : "int | index in text string of footnote location",
            "html"      : "str | html of footnote content"
        }
    ],
    "crossrefs" : [
        {
            "str_index" : "int  | index in text string of footnote location",
            "ref_list"  : "list | list of strings of cross referenced verses"
        }
    ]
}
```

The caching functionality is also accessible from the `query` function as:
```python
verse_list = query("John3.16", cache=True) # scraps from the web
verse_list = query("John3.16", cache=True) # just looks result up
```

## Development

```bash
# Create the venv
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# install for development
./venv/bin/pip install --editable .

# Test
./scripts/run_tests.sh

# Build
./scripts/build.sh

# Deploy
twine upload dist/*
```

# Known Bugs

# TODO
 - Add more than just bgw as the scraping backend
 - More carefully handle formatting (unicode, text transforms, woj, etc).
 - Add WAY more documentations, like some docstrings for the modules . . 
 - Add more unit tests
 - expand cli?
 - finish `string_cleaner` to convert special unicode characters into simpler characters
 - standardize some of the naming -- inconsisten use of `reference` to sometimes mean `Range`,
also, `scrape` is pretty overloaded.
 - Descide how to handle 'Genesis 1:3-4:5,6', does that last one mean verse 6 or chapter 6?
