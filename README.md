# Biblescrapway
A scraping tool for pulling bible verses from the web

# Set Up
Either pip install the requirements, or set up a python virtual environment first:
```bash
 $ python3 -m venv venv
 $ ./venv/bin/pip install -r requirements.txt
```

# Basic Usage
## CLI
`Biblescrapway` comes with a simple cli to pull specific bible passages:
```bash
 $ ./venv/bin/python command.py John3.16
```

You can also specify a version (default is ESV):
```bash
 $ ./venv/bin/python command.py --version KJV John3.16
```

Or, get multiple verses with comma delimiting:
```bash
 $ ./venv/bin/python command.py John3.16,1Peter3:8
```

Or, get a range of verses using a hyphon
```bash
 $ ./venv/bin/python command.py John3.16-17
```

## Programmatic
It is also possible to get json-formatted verses via python, using the `scrap` function:
```python
from biblescrapway import scrap
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
    "version" : "str | bible version abbreviation,
    "text"    : "str | text content of the verse,
    "footnotes" : [
        "..." : "...",
        {
            "str_index" : "int | index in text string of footnote location",
            "html"      : "str | html of footnote content"
        },
        "..." : "..."
    ]
}
```

# Bugs
 - Red letters don't get captured ('woj' spans, c.f. 'John3:16')

# TODO
 - Add more unit tests
 - Add pip installation methods
 - expand cli?
