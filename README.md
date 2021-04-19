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

You can also specify a version (default is ESV):
```bash
 $ bsw --version KJV John3.16
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
 $ bsw -j json John3.16
```

## Programmatic
It is also possible to get full verse objects via python, using the `scrap` function:
```python
from biblescrapeway import scrap
verse = scrap("John 3:16", version = "NIV")
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

# Set up for development
```bash
 $ python3 -m venv venv
 $ ./venv/bin/pip install -r requirements.txt
 $ ./venv/bin/pip install --editable .
```

# Known Bugs

# TODO
 - Add WAY more documentations, like some docstrings for the modules . . 
 - Add more unit tests
 - expand cli?
 - finish `string_cleaner` to convert special unicode characters into simpler characters
